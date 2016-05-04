# softwareDesignProject

This repository is for the GroupDeal website. It contains all files necessary for operation of the site, including front-end markups, database handling, and test files.

### DIRECTORY
#### groupdeal.mssql
  - schema for database

#### Part 1
##### static
  - contains most of the front-end code NOT including HTML. Includes CSS and AJAX files.
##### templates
  - contains HTML layouts for all sections of the GroupDeal website
##### groupdeal.py, groupdeal.pyc, tempvariables.py
  -contains Flask code used in running the site
##### groupdeal.db, schema.sql
  - GroupDeal database and SQL schema
##### groupdeal_test, groupdeal_test.py, groupdeal_test~, groupdeal_test.py~
  - files used for unit testing
  
###  TO RUN LOCALLY
GroupDeal uses Flask, a Python microframework, to run in a virtual environment. To use GroupDeal locally, you can follow these steps:
(###### 0. Install Python 2.6 or higher)
###### 1. Install virtualenv
###### 2. Use virtualenv to create your own environment (most easily done by making a new folder, then placing a *venv* folder in the new folder
###### 3. Activate the virtual environment that was just created.
###### 4. Install Flask **in your virtual environemnt**. (System-wide installation is allowed but not recommended)
###### 5. Clone this repository in the *venv* folder.
###### 6. Run Flask before opening any pages to allow for server use.
