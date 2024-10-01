import pandas as pd
import streamlit as st

from axpo_challenge.domain.data_retriever import DataRetriever # , load_assets, load_measurements, load_signals
# from axpo_challenge.deps.logger import logger
from axpo_challenge.app.main import App

retriever = DataRetriever()
App(retriever=retriever)

# assets = retriever._assets
# signals = retriever._signals

# st.title('Axpo Fullstack challenge')
# col1, col2 = st.columns([1, 3], gap='large')
# checkboxes = {}
# with col1:
#   with st.form('selections'):
#     for asset in list(assets.assets.itertuples()):
#       checkboxes[f'asset_{asset.AssetId}'] = st.checkbox(label=f'**{asset.descri}**',
#                   key=f'asset_{asset.AssetId}')
      
#       signals_4_asset = signals.signals[signals.signals['AssetId'] == asset.AssetId]
#       for signal in list(signals_4_asset.itertuples()):
#         print(f'{signal.SignalId}, {signal.SignalName}')
#         checkboxes[f'{signal.SignalId}'] = st.checkbox(label=signal.SignalName,
#                         key=signal.SignalId)
#         st.divider()
    
#     submitted = st.form_submit_button('Plot')
#     if submitted:
#       print(f'Changed signal {checkboxes}')

# asset_ids: pd.Series = assets.get_all_assets_id()
# df_signal0: pd.DataFrame = signals.get_signal_from_asset(asset_id=int(asset_ids[0]))
# signal_id0 = df_signal0['SignalId'][0]
# measures_signal0: pd.DataFrame = load_measurements().get_measurements_from_signalid(int(signal_id0))
# logger.info(f'End getting measurements ({measures_signal0.shape[0]})')

# with col2:
#   col2.write(f'Plotting {measures_signal0.shape[0]} measurements...')
#   col2.line_chart(measures_signal0[::10], x="Ts", y="Value", height=600)



# asset_ids: pd.Series = retriever.get_all_asset_ids()
# df_signal0: pd.DataFrame = retriever.get_signals_from_asset(asset_id=int(asset_ids[0]))
# signal_id0 = df_signal0['SignalId'][0]
# measures_signal0: pd.DataFrame = retriever.get_measurements(int(signal_id0))
# logger.info(f'End getting measurements ({measures_signal0.shape[0]})')

# st.title('Axpo Fullstack challenge')
# st.write(f'Plotting {measures_signal0.shape[0]} measurements...')
# st.line_chart(measures_signal0[::10], x="Ts", y="Value", height=600)
