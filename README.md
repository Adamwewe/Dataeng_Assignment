# Introduction

Dear Data Engineering team,

Welcome to the solution repository for the data engineering assignment. Solving this was a lot of fun! However please bear in mind the end result could have been more elaborate if I had more time, as my thesis deadline is close I could only invest so much time into the task meaning only rudimentary tests were performed, I did however comment my code on where things could be improved from a computational cost and flexibility perspective. 

# Contents

You can find an overview of code base below:

<p> - <b> cred (fodler): </b> contains .env files to be used for parsing login credentials (currently only containing a single .env file (pw.env))
<p> - <b> container_builder (.sh file): </b> bash helper used to spin up container and install required python libraries (bear in mind pip might not be supported in your linux release, in that case please run the: `sudo easy_install pip` command)
<p> - <b> data (.py file): </b> main class used for the data extraction, transformation and loading 
<p> - <b> main (.py file): </b> entry point to run the loading and transformation process, instanciates the data class object and contains queries to be parsed in the data class
<p> - <b> utils (.py file): </b> helper functions to be used for various tasks such as the credentials parser and the temporary I/O function ensemble for testing purposes
<p> - <b> test (.py file): </b> very simple test case for checking the correct insertion of the data

# How to run

## Running 

Once inside the src folder, spin up the container and install required libraries:

```
bash container_builder.sh
```

Once done, simply run the script from the entry point:

```
python main.py
```

## Testing

After running the script, a <b>results</b> folder will be created where a verification output (one row from the updated table) will be parsed as a pickle file. Currently only one very trivial test case has been run and passed, once again due to the time at hand, I could not conduct more robust tests. You can run the test by executing the following command:

```
pytest test.py 
```


Please let me know if you have any questions and thank you for making and sharing this fun assignment with me!

Kind regards, <br>
Adam 
