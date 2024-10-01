import pandas as pd
import streamlit as st

from axpo_challenge.domain.data_retriever import DataRetriever # , load_assets, load_measurements, load_signals
# from axpo_challenge.deps.logger import logger
from axpo_challenge.app.main import App

retriever = DataRetriever()
App(retriever=retriever)
