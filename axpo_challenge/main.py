import pandas as pd
import streamlit as st

from axpo_challenge.domain.data_retriever import DataRetriever
from axpo_challenge.deps.logger import logger

retriever = DataRetriever()
asset_ids: pd.Series = retriever.get_all_asset_ids()
df_signal0: pd.DataFrame = retriever.get_signals_from_asset(asset_id=int(asset_ids[0]))
signal_id0 = df_signal0['SignalId'][0]
measures_signal0: pd.DataFrame = retriever.get_measurements(int(signal_id0))
logger.info(f'End getting measurements ({measures_signal0.shape[0]})')

st.title('Axpo Fullstack challenge')
st.write(f'Plotting {measures_signal0.shape[0]} measurements...')
st.line_chart(measures_signal0[::10], x="Ts", y="Value", height=600)
