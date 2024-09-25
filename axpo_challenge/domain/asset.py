import pandas as pd

from axpo_challenge.deps.logger import logger

class Asset():
  source_url: str = 'https://github.com/axpogroup/hiring-challenges/raw/refs/heads/main/fullstack-time-series-challenge/data/assets.json'

  def __init__(self):
    logger.info('Loading assets...')
    self.assets = pd.read_json(self.source_url)
    self.assets.rename(columns={'AssetID': 'AssetId'})

  def get_asset_from_id(self, asset_id: int) -> pd.DataFrame:
    return self.assets[self.signals['AssetID'] == asset_id] 

  def get_all_assets_id(self) -> pd.Series:
    return self.assets['AssetID']