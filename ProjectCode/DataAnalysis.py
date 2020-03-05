import numpy as np 
import pandas as pd 
from sklearn.ensemble import IsolationForest

class DataAnalysis:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    #Method passes Pandas dataframe to an IsolationForest object and returns a new dataframe containing predicted anomalous datapoints
    def analyse(self):
        isolation_forest = IsolationForest(n_estimators=300, contamination=0.10)
        isolation_forest = isolation_forest.fit(self.dataframe)
        outliers_values = self.dataframe[isolation_forest.predict(self.dataframe) == -1]
        return outliers_values