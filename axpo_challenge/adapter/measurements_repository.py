import pandas as pd
import streamlit as st
from axpo_challenge.deps.logger import logger

to_float = lambda x: x.replace(',', '.')

@st.cache_data
def load_measurements(source_url: str) -> pd.DataFrame:
  logger.info('Loading measurements...')
  measurements = pd.read_csv(source_url, delimiter='|', converters={'MeasurementValue': to_float})
  measurements.rename(columns={'MeasurementValue': 'Value'}, inplace=True)
  measurements['Value'] = measurements['Value'].astype(float)
  measurements['Ts'] = measurements['Ts'].astype('datetime64[ms]')

  return measurements
