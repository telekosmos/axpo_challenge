import pandas as pd
from typing import List
from axpo_challenge.adapter.measurements_repository import load_measurements

class Measurements():
  source_url: str = 'https://github.com/axpogroup/hiring-challenges/raw/refs/heads/main/fullstack-time-series-challenge/data/measurements.csv'

  def __init__(self):
    self.measurements = load_measurements(source_url=self.source_url)

  def get_measurements_from_signalid(self, signal_id: List[int]) -> pd.DataFrame:
    return self.measurements[self.measurements['SignalId'] == signal_id]
  