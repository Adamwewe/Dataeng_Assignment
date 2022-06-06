import numpy as np
import pandas as pd
from pandas import DataFrame

import psycopg2
from psycopg2 import connect

from datetime import timezone


class Interfacer:
    def __init__(self, login: dict, db: str, query: str, col: str):
        """
        Args:
            - login (dict) : .env file transformed into k/v pairs
            - db (str) : name of database to connect to
            - query (str) : query to retrieve data 
            - col (str) : name of col to be transformed  #TODO: Refactor later into list for more flexibility
        """
        #The below connector is constructed with the class as it will be used in every class method either way

        self.login = login 
        self.db = db
        self.query_fetch = query
        self.col = col 

        try:

            self.connector = "dbname={} user={} password={}".format(self.db, 
                                                        self.login["USER"], 
                                                            self.login["PW"])  #parse db credentials into psycopg2 input string 
            
            self.conn = connect(self.connector)

            self.cur = self.conn.cursor()  #cursor object initialized globally 

        except psycopg2.DatabaseError as err:
            print(err)

    def get_data(self) -> list:

        """
        Returns list of tuples from the server response
        """
        try:
 
            self.cur.execute(self.query_fetch)
            self.resp = self.cur.fetchall()

            self.rows_fetch = self.cur.rowcount 
            
        except psycopg2.DatabaseError as err:
            print(err)

        print("Row count: {}".format(self.rows_fetch))

        return self.resp

    def timestamper(self, schema: list) -> DataFrame:
        
        # I called it the schema although I am only referring to the table cols, the naming is for future reference

        """
        Args:
            - schema (list): contents of the schema to be unpacked for dict keys
        Returns:
            - self.df (object) : Returns the dataframe solving the exercise
        """
        
        self.df =  {key : [] for key in schema}  #To retrieve column names

        #Loop to retrieve list of tuples

        for i in self.resp:  #TODO: Refactor with itertools or with pyspark's functional style to optimize processing speed, this nested loop needs to go away although flexible
            for x, k in enumerate(self.df.keys()):
                self.df[k].append(i[x])

        self.df = DataFrame(self.df)

        #Typecasting:

        self.df[schema[1::]] = self.df[schema[1::]].apply(pd.to_datetime) 

        for i in schema[1::]:
            self.df[i] = self.df[i].apply(lambda x: x.replace(tzinfo=None))  #timezone info removal

        print(self.df.info())

        #Formatting missing values pythonically:

        self.df.fillna(value=np.nan, 
                        inplace=True)  #inplace to avoid copying


        self.df[self.col] = self.df[schema[1::]].min(axis=1, skipna=True)  #fast row-wise minimization to append earliest contact to column


        return self.df 


    def send_data(self, query) -> list:
        
        """
        Args:
            - query (list): query to update table
        Returns:
            - self.result (list) : Returns the response list
        """
        

        self.first_resp = self.df[self.col].dt.to_pydatetime() #Mask to retrieve only the transformed column and cast back to pydatetime for postgres compatibility
        self.first_resp = [x.replace(tzinfo=timezone.utc) for x in self.first_resp]  #to put back timezone information 
        self.cand_id = self.df["candidate_id"]

        [self.cur.execute(query, (r, c)) for r, 
                            c in zip(self.first_resp, self.cand_id)]  #list comp. updating table

        self.conn.commit()  #commit changes
        
        try:
            [self.cur.execute(self.query_fetch, (r, c)) for r, 
                                c in zip(self.first_resp, self.cand_id)]  #running select query again to test
            self.result = self.cur.fetchone()  #to output result 
        
        except psycopg2.ProgrammingError as err:
            print("A '{}' error was raised with the below status message \n".format(err))
            print(self.cur.statusmessage)
            self.result = False  #For testing

        self.cur.close()
        self.conn.close()        

        return self.result  #For testing
        
        