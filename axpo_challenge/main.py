from axpo_challenge.domain.data_retriever import DataRetriever
from axpo_challenge.app.main import App

retriever = DataRetriever()
App(retriever=retriever)
