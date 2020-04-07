from DataAnalysis import DataAnalysis
from DataLoader import DataLoader
import argparse
import datetime
import hashlib
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

    #Processes dataframe so that the model has numerical values to work with
    #Also targets columns more likely to be useful in analysis
    processed_df = df.drop(['@timestamp', 'ID', 'host', 'Content', '@version', 'path', 'message'], axis=1)
    processed_df[['Day', 'Time']] = df.Date.str.split(" ",expand=True,)
    processed_df = processed_df.drop(['Date'], axis=1)
    processed_df = day_update(processed_df)
    processed_df[['Hour', 'Minute', 'Second']] = processed_df.Time.str.split(":",expand=True,)
    processed_df = processed_df.drop(['Minute', 'Second', 'Time'], axis=1)
    processed_df = pd.get_dummies(processed_df, columns=['Bcc', 'Cc', 'PC', 'To', 'Attachments', 'From', 'User', 'Activity', 'Day', 'Hour'], prefix=['Bcc', 'Cc', 'PC', 'To', 'Attachments', 'From', 'User', 'Activity', 'Day', 'Hour'])
    processed_df = processed_df.apply(pd.to_numeric)

    #Hash functions so that original events can be retrieved after analysis
    for index, row in processed_df.iterrows():
        row_signature = hashlib.md5(row.to_string().encode()).hexdigest()
        df.at[index, 'Signature'] = row_signature

    values_list = []
    da = DataAnalysis(processed_df)
    values = da.analyse()
    for index, row in values.iterrows():
        row_signature = hashlib.md5(row.to_string().encode()).hexdigest()
        for index, row in df.iterrows():
            if row_signature == row['Signature']:
                values_list.append(row)

    values_df = pd.DataFrame(values_list)
    print(values_df)
    print(values_df['User'])

    curr_date = str(datetime.datetime.now())
    curr_date = curr_date.replace(" ", "")

    dl.send_to_elastic(values_df, curr_date)

def day_update(dataframe):
    for index, row in dataframe.iterrows():
        date = dataframe.at[index, 'Day']
        date = datetime.datetime.strptime(date, "%m/%d/%Y").strftime('%A')
        dataframe.at[index, 'Day'] = date

    return dataframe

#ASCII art title to display in the terminal
def create_title():
    print(" ___              _  _  ___            _           _      ___           _")
    print("| __>._ _ _  ___ <_>| || . |._ _  ___ | | _ _  ___<_> ___|_ _|___  ___ | |")
    print("| _> | ' ' |<_> || || ||   || ' |<_> || || | |<_-<| |<_-< | |/ . \/ . \| |")
    print("|___>|_|_|_|<___||_||_||_|_||_|_|<___||_|`_. |/__/|_|/__/ |_|\___/\___/|_|")
    print("                                         <___'                            \n")

def get_arguments():
    parser = argparse.ArgumentParser(prog="Email Analysis Tool")
    parser.add_argument("-i", "--index", help="Sets the Elasticsearch index that will be queried for data. Default value of 'email' will be used if no index is specified.")
    parser.add_argument("-s", "--size", type=int, help="Sets the number of Elasticsearch documents that will be requested through the API. This needs to be an integer value. Also be aware of the limitations of the system you are running the program on. Any documents that it receives back from your Elasticsearch instance will be added to an in-memory object, so if this value is set too high you will suffer a memory leak. Default value of 10 will be used if no size is specified.")
    parser.add_argument("-n", "--node", help="Sets the URI of the Elasticsearch instance that the request for documents will be sent to. Should contain the domain/IP address and port of the instance, e.g. 'http://localhost:9200' or 'http://127.0.0.1:9200'. Default value of 'http://localhost:9200' will be used if no node is specified.")

    return parser.parse_args()

main()
