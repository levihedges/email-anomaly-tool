import numpy as np 
import pandas as pd 
import hashlib
import random as rn
import os
from collections import Counter
from sklearn.ensemble import IsolationForest

class DataAnalysis:

    def __init__(self, dataframe, repetition):
        self.dataframe = dataframe
        self.repetition = repetition

    #Method passes Pandas dataframe to an IsolationForest object and returns a new dataframe containing predicted anomalous datapoints
    def analyse(self):
        outliers_value_list = []
        rep_loop = self.repetition
        while (rep_loop > 0):
            seed = self.random_seed()
            isolation_forest = IsolationForest(n_estimators=200, contamination=0.10, random_state=seed)
            isolation_forest = isolation_forest.fit(self.dataframe)
            outliers_values = self.dataframe[isolation_forest.predict(self.dataframe) == -1]
            for index, row in outliers_values.iterrows():
                outliers_value_list.append(row)
            rep_loop -= 1
        for value in range(len(outliers_value_list)):
           outliers_value_list[value] = hashlib.md5(outliers_value_list[value].to_string().encode()).hexdigest()
        confidence_score_tally = Counter()
        for new_value in outliers_value_list:
            confidence_score_tally[new_value] += 1
        confidence_score_dict = dict(confidence_score_tally)
        for key, value in confidence_score_dict.items():
            confidence_score_dict[key] = float(round(confidence_score_dict[key] / self.repetition, 3))
        return confidence_score_dict

    #Generates random seed each time algorithm is invoked
    def random_seed(self):
        length = rn.randint(1, 3)
        rand_bytes = os.urandom(length)
        rand_bytes_int = int.from_bytes(rand_bytes, byteorder="little")
        return rand_bytes_int
