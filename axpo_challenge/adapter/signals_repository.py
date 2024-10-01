import pandas as pd
import streamlit as st
from axpo_challenge.deps.logger import logger

@st.cache_data
def load_signals(source_url: str) -> pd.DataFrame:
  logger.info('Loading signals...')
  signals = pd.read_json(source_url)

  return signals