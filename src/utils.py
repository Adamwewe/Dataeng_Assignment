import os

import dotenv
from dotenv import dotenv_values

import pickle

def get_cred(dir: str) -> str:

    """
    Args:
        - dir (str) : path to directory containing .env file
    Returns:
        - login(str) : name of .env containing credentials 
    """

    creds = []  #extending with list for potentially accomodating multiple login files 

    for item in os.listdir(dir):
        if item.endswith(".env"):
            creds.append(dir + "/" + item)  
    print("Logging in with...{}".format(creds[0]))
    login = dotenv_values(creds[0])  #TODO: More flexible solution instead of just pointing to credentials with index


    return login


def check_dir(path: str):
    """
    Args:
        - path (str) : name of output path
    Returns:
        - path (str) : name of output path (checks created)
    """

    exists = os.path.isdir(path)  #Check if dir exists

    if exists == True:
        return path

    else:
        os.mkdir(path)
        return path 


def write_result(result: list) -> None:

    """
    Args:
        - result (list) : Result list from main program
    Returns:
        - path (str) : name pkl file with full path
    """

    path = check_dir("results") + "/results.pkl"

    with open(path, "wb") as hd:
        pickle.dump(result, hd, 
                        protocol=pickle.HIGHEST_PROTOCOL)  #protocol set to highest for backwards comp

    return path


def read_result() -> tuple:

    """
    Returns laoded pickle from path containing tuple of tuples generated or read from the check_dir and write_results helpers
    """

    path = check_dir("results") + "/results.pkl"

    with open(path, "rb") as hd:
        data = pickle.load(hd)
    print(data)

    return data

