### PUR BEURRE PROGRAM

Author : VERNHES Cyril

#### Description :

This program allows you to search for a substitute and save it in favorites.
Products are downloaded from the database Openfoodfacts.

#### Prerequisites :

To work, the program requires python 3.

#### Start program and virtual environment : 

Download the project with Git and open the command line and go to project path :

###### Create the directory of virtualenv files named venv :
`python3 -m venv venv`

###### Activate the virtual environment
`venv\Scripts\activate.bat`

###### Install the libraries
`pip install -r requirements.txt`

###### Download products
`python3 manage.py openfoodfacts`
or
`python3 manage.py openfoodfacts --delete`
for clean database

###### Start test server :
`python3 manage.py runserver`

###### Stop virtual environment :
`deactivate`
