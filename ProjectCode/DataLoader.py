import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd
import numpy as np

class DataLoader:

    def __init__(self, index, size, node):
        self.index = index
        self.size = size
        self.node = node

    def fetch_data(self):
        try:
            elastic_node = Elasticsearch(self.node)
            search_response = elastic_node.search(
                index = self.index,
                body={},
                size = self.size
            )
        except elasticsearch.exceptions.NotFoundError:
            print("The specified index could not be found on the Elasticsearch instance. Please check that the index was entered properly and that the instance is running then re-attempt.")
            exit()
        except elasticsearch.exceptions.ConnectionError:
            print("The specified URI could not be connected to. Please check that the URI was entered properly, that the Elasticsearch instance is running and that you have a suitable network connection then re-attempt.")
            exit()

        return search_response

    def create_dataframe(self, response):
        documents = response["hits"]["hits"]
        es_fields = {}

        for num, doc in enumerate(documents):
            pass

            source = doc["_source"]
            for key, val in source.items():
                try:
                    es_fields[key] = np.append(es_fields[key], val)
                except KeyError:
                    es_fields[key] = np.array([val])

        es_dataframe = pd.DataFrame(es_fields)
        return es_dataframe

    def send_to_elastic(flagged_events, date):
         elastic_node = Elasticsearch(self.node)
         helpers.bulk(elastic_node, store_events(flagged_events, date))

    def store_events(flagged_events, date):
        fe_list = flagged_events.iterrows()
        for index, document in fe_list:
            yield {
                    "_index": 'flagged_events_' + date
                    "_type": 'doc'
                    "_id": f"{document['id'] + index}"
                    "_source": filterKeys(document)
            }
