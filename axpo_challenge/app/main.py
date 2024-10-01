import pandas as pd
import streamlit as st

from axpo_challenge.domain.data_retriever import DataRetriever
from axpo_challenge.deps.logger import logger


class App():
  def __init__(self, retriever: DataRetriever):
    self.retriever = retriever
    self.assets = self.retriever._assets.assets
    self.signals = self.retriever._signals.signals
    self.measurements = self.retriever._measurements.measurements

    self.assets_signals = {}
    self.assets_descri = {}
    self.all_signals = {}
    for asset in list(self.assets.itertuples()):
      print(f'{asset.descri}')
      signals_4_asset = self.signals[self.signals['AssetId'] == asset.AssetId]
      self.assets_descri[asset.AssetId] = asset.descri
      self.assets_signals[asset.AssetId] = []
      for signal in list(signals_4_asset.itertuples()):
        self.assets_signals[asset.AssetId].append((signal.SignalId, signal.SignalName))
        self.all_signals[signal.SignalId] = signal.SignalName
        print(f'{signal.SignalId}, {signal.SignalName}')


    signal_427659 = self.measurements[self.measurements.SignalId == 427659][['Ts', 'Value']].sort_values(by='Ts')
    signal_427712 = self.measurements[self.measurements.SignalId == 427712][['Ts', 'Value']].sort_values(by='Ts')
    signal_427038 = self.measurements[self.measurements.SignalId == 427038][['Ts', 'Value']].sort_values(by='Ts')
    signal_430247 = self.measurements[self.measurements.SignalId == 430247][['Ts', 'Value']].sort_values(by='Ts')
    signal_427659_resamp = self._adaptive_downsample(signal_427659, 'Ts')
    signal_427712_resamp = self._adaptive_downsample(signal_427712, 'Ts')
    signal_430247_resamp = self._adaptive_downsample(signal_430247, 'Ts')
    self._signals_resampled = {
      427659: self._adaptive_downsample(signal_427659, 'Ts'),
      427712: self._adaptive_downsample(signal_427712, 'Ts'),
      427038: self._adaptive_downsample(signal_427038, 'Ts'),
      430247: self._adaptive_downsample(signal_430247, 'Ts')
    }

    st.title('Axpo Fullstack challenge')
    self.checkboxes = {}
    self.col1, self.col2 = st.columns([1, 3], gap='large')
    self.placeholder = st.empty()
    with self.placeholder.container():
      with self.col1:
        default_signal = None
        with st.form('selections'):
          for asset_id, signal_list in self.assets_signals.items():
            asset_name = self.assets_descri[asset_id]
            st.write(f'**{asset_name}**')
            for (signal_id, signal_name) in signal_list:
              print(f'{signal_id}, {signal_name}')
              self.checkboxes[f'signal_{signal_id}'] = st.checkbox(
                signal_name,
                key=f'signal_{signal_id}',
                value=True if default_signal is None else False)
              default_signal = signal_id if default_signal is None else default_signal

            st.divider()
          
          submitted = st.form_submit_button('Plot')
          if submitted:
            self._plot()

      
      logger.info(f'############### signals_resampled keys {self._signals_resampled.keys()}')
      signal_two = pd.merge(signal_427659_resamp, signal_427712_resamp, how='outer', on='Ts')
      signal_three = pd.merge(signal_two, signal_427712_resamp, how='outer', on='Ts')
      if 'started' not in st.session_state:
        st.session_state['started'] = True
        self._plot()
      # with self.col2: #, self.placeholder.container():
      #     # asset_ids: pd.Series = retriever.get_all_asset_ids()
      #     # df_signal0: pd.DataFrame = retriever.get_signals_from_asset(asset_id=int(asset_ids[0]))
      #     # signal_id0 = df_signal0['SignalId'][0]
      #     # measures_signal0: pd.DataFrame = retriever.get_measurements(int(signal_id0))
      #     data_to_plot = self._signals_resampled[default_signal]
      #     # self.col2.write(f'Plotting measurements')
      #     # self.col2.line_chart(data_to_plot, x='Ts', height=600)
      #     st.line_chart(data_to_plot, x='Ts', use_container_width=True, height=600)
      #     logger.info(f'End getting measurements ({data_to_plot.shape[0]})')


    # st.write(f'Plotting {measures_signal0.shape[0]} measurements...')
    # st.line_chart(measures_signal0[::10], x="Ts", y="Value", height=600)

  def _adaptive_downsample(self, df, ts_field, target_points=5000):
    if len(df) <= target_points:
      return df
      
    # Calculate the total time span
    time_span = df.Ts.index[-1] - df.Ts.index[0]
    
    # Calculate the ideal time delta between points
    # ideal_delta = time_span / target_points
    my_delta = (df[ts_field].iloc[-1] - df[ts_field].iloc[0]).total_seconds() / target_points
    # Find the appropriate frequency string
    if my_delta < pd.Timedelta(seconds=1).total_seconds():
      freq = f'{int(my_delta * 1000)}L'  # milliseconds
    elif my_delta < pd.Timedelta(minutes=1).total_seconds():
      freq = f'{int(my_delta)}s'  # seconds
    elif my_delta < pd.Timedelta(hours=1).total_seconds():
      freq = f'{int(my_delta / 60)}min'  # minutes
    elif my_delta < pd.Timedelta(days=1).total_seconds():
      freq = f'{int(my_delta / 3600)}H'  # hours
    else:
      freq = f'{int(my_delta / 86400)}D'  # days
    
    # Resample and interpolate
    resampled = df.resample(freq, on=ts_field).mean().interpolate()
    resampled = resampled.assign(Ts=resampled.index)
    resampled.reset_index(drop=True, inplace=True)

    return resampled

  def _plot(self, signal = None):
    
    signals_checked = [ int(k.split('_')[1]) for (k, v) in self.checkboxes.items() if v is True ]
    print(f'plot -> signals_to_show {self._signals_resampled.keys()}\n{signals_checked}')
    data_to_plot = None
    if len(signals_checked) == 1:
      data_to_plot = self._signals_resampled[signals_checked[0]].rename(columns={'Value': self.all_signals[signals_checked[0]]})
    else:
      (df_one, df_two, rest) = (self._signals_resampled[signals_checked[0]],
      self._signals_resampled[signals_checked[1]],
      signals_checked[2:])
      data_to_plot = pd.merge(
        df_one.rename(columns={'Value': self.all_signals[signals_checked[0]]}),
        df_two.rename(columns={'Value': self.all_signals[signals_checked[1]]}),
        how='outer',
        on='Ts')
      while len(rest) > 0:
        current_signal, rest = rest[0], rest[1:]
        df = self._signals_resampled[current_signal]
        data_to_plot = pd.merge(
          data_to_plot,
          df.rename(columns={'Value': self.all_signals[current_signal]}),
          how='outer',
          on='Ts')

    # self.col2.line_chart(data_to_plot, x='Ts', height=600)
    with self.placeholder.container():
      self.col2.line_chart(data_to_plot, x='Ts', x_label='Signl', use_container_width=True, height=600)
    logger.info(f'data_to_plot ({data_to_plot.shape[0]})')

    # measures_signal0: pd.DataFrame = self.retriever.get_measurements()
    # logger.info(f'End getting measurements ({measures_signal0.shape[0]})')

    # self.col2.line_chart(measures_signal0[::10], x='Ts', y='Value', height=600)

  def _update_plot(self):
    # checked_assets = [ k.split('_')[1] for (k, v) in self.checkboxes.items() if (k.startswith('asset') is True) and (v is True) ]
    # assets_to_show = {k: v for k, v in self.assets_signals.items() if k in map(int, checked_assets)}
    # checked_signals = [ k.split('_')[1] for (k, v) in self.checkboxes.items() if (k.startswith('signal') is True) and (v is True) ]
    assets_checked = [ int(k.split('_')[1]) for (k, v) in self.checkboxes.items() if (k.startswith('asset') is True) and (v is True) ]
    signals_checked = [ int(k.split('_')[1]) for (k, v) in self.checkboxes.items() if (k.startswith('signal') is True) and (v is True) ]

    filtered_assets = sum([v for k, v in self.assets_signals.items() if k in assets_checked ], [])
    filtered_signals = [ s for s in sum(self.assets_signals.values(), []) if s[0] in signals_checked ]
    signals_to_show = set(filtered_assets + filtered_signals)
    print(f'signals_to_show {self.checkboxes}')
    for (signal_id, _) in filtered_assets:
      print(f'self.checkboxes[signal_{signal_id}] = True')
