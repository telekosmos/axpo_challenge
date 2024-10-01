import pandas as pd
import streamlit as st

from axpo_challenge.domain.data_retriever import DataRetriever
from axpo_challenge.deps.logger import logger

class App():
  def __init__(self, retriever: DataRetriever):
    assets = retriever._assets.assets
    signals = retriever._signals.signals

    self.assets_signals = {}
    self.assets_descri = {}
    self.all_signals = {}
    for asset in list(assets.itertuples()):
      print(f'{asset.descri}')
      signals_4_asset = signals[signals['AssetId'] == asset.AssetId]
      self.assets_descri[asset.AssetId] = asset.descri
      self.assets_signals[asset.AssetId] = []
      for signal in list(signals_4_asset.itertuples()):
        self.assets_signals[asset.AssetId].append((signal.SignalId, signal.SignalName))
        self.all_signals[signal.SignalId] = signal.SignalName
        print(f'{signal.SignalId}, {signal.SignalName}')

    measurements_sorted = lambda k: retriever.get_measurements(k)[['Ts', 'Value']].sort_values(by='Ts')
    self._signals_resampled = {
      k: self._adaptive_downsample(measurements_sorted(k), 'Ts') for k, _ in self.all_signals.items()
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

      if 'started' not in st.session_state:
        st.session_state['started'] = True
        self._plot()
      

  def _adaptive_downsample(self, df, ts_field, target_points=5000):
    if len(df) <= target_points:
      return df
      
    my_delta = (df[ts_field].iloc[-1] - df[ts_field].iloc[0]).total_seconds() / target_points
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
    
    resampled = df.resample(freq, on=ts_field).mean().interpolate()
    resampled = resampled.assign(Ts=resampled.index)
    resampled.reset_index(drop=True, inplace=True)

    return resampled

  def _plot(self, signal = None):
    signals_checked = [ int(k.split('_')[1]) for (k, v) in self.checkboxes.items() if v is True ]
    logger.info(f'signals_to_show {self._signals_resampled.keys()}\n{signals_checked}')
    data_to_plot = None
    if len(signals_checked) == 0:
      self.placeholder.empty()

    else:
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

      with self.placeholder.container():
        self.col2.line_chart(data_to_plot, x='Ts', x_label='Mesurements', use_container_width=True, height=600)
