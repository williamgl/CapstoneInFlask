## CS467 Capstone Project Using Flask

### Run it locally
1. run ```pip3 install --user virtualenv```
2. run ```python3 -m venv .``` or ```python3 -m venv ./venv``` to set up virtual environment
3. run ```source ./bin/activate``` or ```source ./venv/bin/activate``` to start the virtual environment (```deactivate``` to close)
4. run ```pip3 install flask-mysqldb``` and ```pip3 install mysql``` to install database packages
5. run ```pip3 install flask``` and ```pip3 install mysql-connector```
6. run ```pip3 install flask-bootstrap```
7. install all packages in requirements.txt
8. run ```python3 app.py``` to view current result.



### Database
1. change the database option in app.py
2. if you are running it using AWS RDS, no further actions needed
3. if you are running it locally, install mysql in your laptop
4. cd to the database folder
5. access to your local mysql server, 
6. ```CREATE DATABASE quiz;```
7. ```USE DATABASE quiz;```
8. ```source DDL.sql;```


### Run it on OSU server
1. upload everything on the server
2. run ```pip3 install gunicorn```
3. run ```pip3 install mysql-connector```
4. run ```gunicorn -b 0.0.0.0:28571 -D app:app```


### To view my current result
1. connect OSU VPN
2. access website: http://flip1.engr.oregonstate.edu:28571/
