import pandas as pd

from axpo_challenge.deps.logger import logger
from axpo_challenge.domain.asset import Asset
from axpo_challenge.domain.signal import Signal
from axpo_challenge.domain.measurements import Measurements

class DataRetriever():

  def __init__(self):
    self._assets = Asset()
    self._signals = Signal()
    self._measurements = Measurements()

  def get_all_asset_ids(self) -> pd.Series:
    logger.info('Getting all assets...')
    return self._assets.get_all_assets_id()
  
  def get_signals_from_asset(self, asset_id: int) -> pd.DataFrame:
    logger.info(f'Getting signals for asset {asset_id}')
    return self._signals.get_signal_from_asset(asset_id=asset_id)
  
  def get_measurements(self, signal_id: int) -> pd.DataFrame:
    logger.info(f'Getting measurements for signal {signal_id}')
    return self._measurements.get_measurements_from_signalid(signal_id=signal_id)
