# Project: AWS Redshift Data Warehouse

## introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and 
data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a
directory with JSON metadata on the songs in their app.
As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, 
stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to 
continue finding insights into what songs their users are listening to. You'll be able to test your database and ETL pipeline 
by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Description

In this project, you'll apply what you've learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. To complete the project, you will need to load data from S3 to staging tables on Redshift and execute SQL statements that create
the analytics tables from these staging tables.

## Files to run project...
- [ **create_tables.py** ] (*Python 3 script*):<br>
  Connects to Redshift cluster and creates database staging, fact and dimension tables as per queries from<br>
  the *sql_queries.py* python file.
  
  

- [ **etl.py** ] (*Python 3 script*):<br>
  2 stage data processing script; 1) Loads data from S3 hosted JSON files to staging tables. 2) Loads data to fact and<br>
  dimension tables from the staging tables.
  
  

- [ **sql_queries.py** ] (*Python 3 script*):<br>
  CREATE, COPY and INSERT SQL statements used by etl.py
  
  

- [ **dwh.cfg** ] (*config text file*):<br>
  Contains user AWS credentials, S3 bucket paths, cluster details, all utilised by project Python scripts.



### Running the project
1. Download project Python scripts and config file, as listed above, to a local directory.
2. Launch a redshift cluster and create an IAM role that has read access to S3.
3. Add AWS credentials, cluster endpoint, database and IAM role details to dwh.cfg.
4. Open your system CLI and change directory to where the project files are saved.<br>
   
        C:\users\username>cd C:\users\username\path\to\project
   
5. Run first Python script to create table schema on Redshift cluster... *create_tables.py*;<br>

        C:\users\username>cd C:\users\username\path\to\project>python3 create_tables.py

6. Run second python script to process S3 hosted JSON files to staging tables and final star schema tables... *etl.py*;<br>

        C:\users\username>cd C:\users\username\path\to\project>python3 etl.py 

---
## Dataset
2No. datasets are available for ingest to the Redshift Sparkify data warehouse, required to carry out relevant<br>
song play data analysis.

    Song data: s3://udacity-dend/song_data
    Log data: s3://udacity-dend/log_data

### Song data
Song data resides in JSON format, with each file containing metadata about a specific song, and the song's artist.<br>
Within Sparkify's file storage, song files are partitioned by the first three letters of each song's track ID.

Filepath example...

    song_data/A/B/C/TRABCEI128F424C983.json
    song_data/A/A/B/TRAABJL12903CDCF1A.json

TRAABJL12903CDCF1A.json song file content...

    {
    "num_songs": 1,
    "artist_id": "ARJIE2Y1187B994AB7",
    "artist_latitude": null,
    "artist_longitude": null,
    "artist_location": "",
    "artist_name": "Line Renaud",
    "song_id": "SOUPIRU12A6D4FA1E1",
    "title": "Der Kleine Dompfaff",
    "duration": 152.92036,
    "year": 0
    }

###  Log data
User activity logs, collected via the Sparkify music streaming applications, also resides in JSON format.<br>
Each file represents a single day and contains information about each user and their session details for that day.
Within Sparkify's file storage, log files are partitioned by the month and year.

    log_data/2018/11/2018-11-12-events.json
    log_data/2018/11/2018-11-13-events.json

2018-11-12-events.json log file content...

    {
    "artist":null,
    "auth":"Logged In",
    "firstName":"Celeste",
    "gender":"F",
    "itemInSession":0,
    "lastName":"Williams",
    "length":null,
    "level":"free",
    "location":"Klamath Falls, OR",
    "method":"GET",
    "page":"Home",
    "registration":1541077528796.0,
    "sessionId":438,
    "song":null,
    "status":200,
    "ts":1541990217796,
    "userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64)<br>
                AppleWebKit\/537.36 (KHTML, like Gecko)<br>
                Chrome\/37.0.2062.103 Safari\/537.36\"",
    "userId":"53"
    }

---

