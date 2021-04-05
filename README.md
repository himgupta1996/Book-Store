# Book-Store

This repository contains implementation of the Lab 2 Project of COMPSCI 677 course at UMass Amherst. <br>
Contributors - <br>
Abhishek Lalwani (alalwani@umass.edu) <br>
Himanshu Gupta (hgupta@umass.edu) <br>
Kunal Chakrabarty (kchakrabarty@umass.edu) <br>

Following are the source file descriptions

# Source File Descriptions
1. `Catalog/catalog.py` implements the catalog server with the relevant GET and PUT methods.
2. `frontend/front_end.py` implements the front end server with the buy, search and lookup methods.
3. `order/main.py` implements the order server with the buy method. 
4. `Docs` contains the design documentation and the test case documentation
5. `requirements.txt` contains the python libraries required
6. `client.py` is a single script to automatically run tests
7. `const.py` contains information about the IP and Node for all the servers


Please find the instructions below for testing the implementation.

# Instructions 

1. Define the ports of order, catalog and front end server by editing the `const.py` file
2. Run `python client.py -n <number of iterations>`. For example, if you want the service to run for 20 iterations (where each iteration contains one instance of search,lookup and buy method) you use `python client.py -n 20` OR `python client.py 20`. Default value is 5 iterations. Please note that the servers keep running even after the completion of all iterations.
3. You can observe the results of this run in the log files. Client.log will contain the logs of all the servers. For server specific logs, you can refer to the logs inside the specific folder for a server.

sudo yum install python3
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
pip install flask
pip install gunicorn
gunicorn -b 0.0.0.0:8010 front_end:app
pip install requests
