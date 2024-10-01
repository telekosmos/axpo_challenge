import pandas as pd
import streamlit as st
from axpo_challenge.deps.logger import logger

@st.cache_data
def load_assets(source_url: str) -> pd.DataFrame:
  logger.info('Loading assets...')
  assets = pd.read_json(source_url)
  assets.rename(columns={'AssetID': 'AssetId'}, inplace=True)

  return assets