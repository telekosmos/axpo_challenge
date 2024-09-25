import pandas as pd
from axpo_challenge.deps.logger import logger

class Measurements():
  source_url: str = 'https://github.com/axpogroup/hiring-challenges/raw/refs/heads/main/fullstack-time-series-challenge/data/measurements.csv'

  def __init__(self):
    logger.info('Loading measurements...')
    to_float = lambda x: x.replace(',', '.')
    
    self.measurements = pd.read_csv(self.source_url, delimiter='|', converters={'MeasurementValue': to_float})
    self.measurements.rename(columns={'MeasurementValue': 'Value'}, inplace=True)
    self.measurements['Value'] = self.measurements['Value'].astype(float)
    self.measurements['Ts'] = self.measurements['Ts'].astype('datetime64[ms]')

  def get_measurements_from_signalid(self, signal_id: int) -> pd.DataFrame:
    return self.measurements[self.measurements['SignalId'] == signal_id]
  