from utils import get_cred, write_result  #.env helper and result output helper import 

from data import Interfacer  #main class import


################## Query declaration section ##################

query_fetch = """SELECT candidate_id, 
                hired_timestamp, 
                invited_timestamp, 
                shortlisted_timestamp, 
                first_response_timestamp
                FROM candidates_status_transitions
                WHERE 
                (invited_timestamp IS NOT NULL
                OR 
                shortlisted_timestamp IS NOT NULL 
                OR 
                first_response_timestamp IS NOT NULL 
                );
                """ 


query_push = """UPDATE candidates_status_transitions 
                    SET first_response_timestamp = %s
                    WHERE candidate_id = %s;
            """


optimizer =  """ OPTIMIZE TABLE first-response_timestamp;"""  #For future use, ran out of time for optimization tasks

################## Parameter declaration section ##################


path = "cred" #path to dir containing login creds
db = "postgres"  #db type to parse in connector
login = get_cred(path)  #helper function to decode .env files

schema = ["candidate_id", "hired_timestamp", "invited_timestamp", 
            "shortlisted_timestamp", "first_response_timestamp"]  #Table columns 
transform = "first_response_timestamp"  #Result column to be transformed 

################## Main Program ##################


I = Interfacer(login=login, 
                db=db, 
                query=query_fetch, 
                col=transform)
I.get_data()
I.timestamper(schema=schema)
result = I.send_data(query_push)




