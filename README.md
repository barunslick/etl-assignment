<h3 align="center">ETL Assignment</h3>

---

<p align="center">  A simple ETL flow for employees and their timesheet data.
    <br> 
</p>

## Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](#todo)

## About <a name = "about"></a>
An ETL project that takes employee and their time sheet information and store it in a Data Warehouse. This was done as a learning assignment for Data Engineering Internship.

### Folder structure
```
 ├── data 		// Contains all the raw data
 ├── docs 		// Technical Documentation
 ├── README.md
 ├── requirements.txt
 ├── run.py 		// Entry point of the application
 ├── schema		 // All the schemas for table needed
 └── src
    ├── __init__.py
    ├── config.py		 // Contains configurable constants. eg for database
    ├── pipeline		 // Contains all the pipelines code
    ├── sql 		// Contains SQL scripts used during running of pipelines
    └── utils		 // General utils

```


## Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites
```
Postgresql
Python3.9
Pip
```

### Installing
1. Clone the repo into the local machine
2. cd into the project and create a virtual environment:
```
$ python3 -m venv venv
```
3. Source the virtual environment
```
$ source venv/bin/activate
```
4. Install all the dependencies
```
$ pip install -r requirements.txt
```

### Setup Tables
Before you can run the application you need to create the database and all the tables required.
You can create the tables by going through the "schema" folder and running all the SQL scripts present there. There is no way of automatically doing this right now, so has to be done manually.

After the database and table are set update the src/config file to your database settings to allow the app to connect to that database
```
$ vim src/config.py
```
Update the constants under "# DATABASE CONNECTION CONFIG" to your database credentials.


## Usage <a name="usage"></a>

If both the database and tables are set then, you can simply run:
```
$ python run.py
```
This command runs the whole ETL flow starting by truncating all the tables, extracting the raw data and filling up dimension and fact tables.


## Built Using <a name = "built_using"></a>
- Python
- PostgreSQL
- Pandas
- Psycopg2


## TODO <a name = "todo"></a>
- Use period dimension in fact timesheet
- Number of teammates absent in fact timesheet
