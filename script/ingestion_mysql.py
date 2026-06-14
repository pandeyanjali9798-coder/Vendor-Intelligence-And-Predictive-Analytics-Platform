import pandas as pd
from sqlalchemy import create_engine
import os
import time
import logging

logging.basicConfig(
    filename = "logs/ingestion_mysql.log",
    level = logging.DEBUG,
    format = "%(asctime)s-%(levelname)s-%(message)s",
    filemode = "a"
)


engine = create_engine("mysql+pymysql://root:Anjali%409798@127.0.0.1:3306/inventory_dataset_db")
def load_raw_data():
    """"" the function will load csv file as Dataframe and ingested into mysql"""""
    start = time.time()
    for file in os.listdir('data'):
      if '.csv' in file:
          df = pd.read_csv('data/'+file)
          logging.info(f"Ingestion {file} in mysql")
          ingest_mysql(df,file[:-4],engine)

    end = time.time()
    total_time = (end-start)/60
    logging.info("------Ingestion Completed------")


    logging.info(f"total time taken: {total_time} min")
     



def ingest_mysql(df,TABLE_NAME,engine):
   """ this function ingested Dataframe into mysql"""
   df.to_sql(TABLE_NAME, con=engine, if_exists='replace', index=False)
if __name__ == "__main__":
   load_raw_data()