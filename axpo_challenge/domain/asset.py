import pandas as pd

from axpo_challenge.adapter.asset_repository import load_assets

class Asset():
  source_url: str = 'https://github.com/axpogroup/hiring-challenges/raw/refs/heads/main/fullstack-time-series-challenge/data/assets.json'

  def __init__(self):
    self.assets = load_assets(source_url=self.source_url)

  def get_asset_from_id(self, asset_id: int) -> pd.DataFrame:
    return self.assets[self.signals['AssetId'] == asset_id] 

  def get_all_assets_id(self) -> pd.Series:
    return self.assets['AssetId']
  