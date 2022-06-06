#TODO: refactor I/O for cleaner testing module
#TODO: implement a conftest file to be able to pass in different indexes through cli 
from .utils import read_result

def test_result():

    """
    returns assertion of the result being True
    """
    result = read_result()

    result = result[4] != None 

    assert result == True
