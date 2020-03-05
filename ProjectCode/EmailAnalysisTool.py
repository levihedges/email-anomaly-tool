from DataAnalysis import DataAnalysis
from DataLoader import DataLoader
import argparse
import datetime
import pandas as pd

def main():
    index = "email"
    size = 10
    node = "http://localhost:9200"

    create_title()
    args = get_arguments()

    #Check if optional arguments were passed to the application
    if args.index is not None:
        index = args.index
    if args.size is not None:
        size = args.size
    if args.node is not None:
        node = args.node

    dl = DataLoader(index, size, node)
    elastic_response = dl.fetch_data()
    df = dl.create_dataframe(elastic_response)
    
    processed_df = df.drop(['@timestamp', 'ID', 'host', 'Content', '@version', 'path', 'message'], axis=1)
    processed_df[['Day', 'Time']] = df.Date.str.split(" ",expand=True,)
    processed_df = processed_df.drop(['Date'], axis=1)
    processed_df = day_update(processed_df)
    processed_df[['Hour', 'Minute', 'Second']] = processed_df.Time.str.split(":",expand=True,)
    processed_df = processed_df.drop(['Minute', 'Second', 'Time'], axis=1)
    processed_df = pd.get_dummies(processed_df, columns=['Bcc', 'Cc', 'PC', 'To', 'Attachments', 'From', 'User', 'Activity', 'Day', 'Hour'], prefix=['Bcc', 'Cc', 'PC', 'To', 'Attachments', 'From', 'User', 'Activity', 'Day', 'Hour'])
    processed_df = processed_df.apply(pd.to_numeric)

    print(processed_df.dtypes)
    print(processed_df)

    da = DataAnalysis(processed_df)
    values = da.analyse()
    print(values)


def day_update(dataframe):
    for index, row in dataframe.iterrows():
        date = dataframe.at[index, 'Day']
        date = datetime.datetime.strptime(date, "%m/%d/%Y").strftime('%A')
        dataframe.at[index, 'Day'] = date

    return dataframe


def create_title():
    print("PLACEHOLDER FOR EMAIL ANALYSIS TOOL TITLE \n")


def get_arguments():
    parser = argparse.ArgumentParser(prog="Email Analysis Tool")
    parser.add_argument("-i", "--index", help="Sets the Elasticsearch index that will be queried for data. Default value of 'email' will be used if no index is specified.")
    parser.add_argument("-s", "--size", type=int, help="Sets the number of Elasticsearch documents that will be requested through the API. This needs to be an integer value. Also be aware of the limitations of the system you are running the program on. Any documents that it receives back from your Elasticsearch instance will be added to an in-memory object, so if this value is set too high you will suffer a memory leak. Default value of 10 will be used if no size is specified.")
    parser.add_argument("-n", "--node", help="Sets the URI of the Elasticsearch instance that the request for documents will be sent to. Should contain the domain/IP address and port of the instance, e.g. 'http://localhost:9200' or 'http://127.0.0.1:9200'. Default value of 'http://localhost:9200' will be used if no node is specified.")
    
    return parser.parse_args()

main()