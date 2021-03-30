# Book-Store

This repository contains implementation of the Lab 2 Project of COMPSCI 677 course at UMass Amherst. <br>
Contributors - <br>
Abhishek Lalwani (alalwani@umass.edu) <br>
Himanshu Gupta (hgupta@umass.edu) <br>
Kunal Chakrabarty (kchakrabarty@umass.edu) <br>

Following are the source file descriptions

# Source File Descriptions
1. `Catalog/catalog.py` implements the catalog server with the item and update_by_id methods
2. `frontend/front_end.py` implements the front end server with the buy, search and lookup methods
3. `order/main.py` implements the order server with the buy method. 
4. `requirements.txt` contains the python libraries required
5. `client.py` is a single script to automatically run tests
6. `const.py` contains information about the IP and Node for all the servers

Please find the instructions below for testing the implementation.

# Instructions 

1. Define the ports of order, catalog and front end server by editing the `const.py` file
2. Run `python client.py -n <time in seconds>`. For example, if you want the service to run for 20 seconds you use `python client.py -n 20` OR `python client.py 20`
