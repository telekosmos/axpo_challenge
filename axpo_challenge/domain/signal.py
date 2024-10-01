import pandas as pd
from axpo_challenge.adapter.signals_repository import load_signals

class Signal():
  source_url: str = 'https://github.com/axpogroup/hiring-challenges/raw/refs/heads/main/fullstack-time-series-challenge/data/signal.json'

  def __init__(self):
    self.signals = load_signals(self.source_url)

  def get_signal_from_asset(self, asset_id: int) -> pd.DataFrame:
    return self.signals[self.signals['AssetId'] == asset_id]
  
  def get_all_signal_ids(self) -> pd.Series:
    return self.signals['SignalId']