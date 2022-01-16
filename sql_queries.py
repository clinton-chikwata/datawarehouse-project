import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# S3 PATH
LOG_DATA = config.get('S3', "LOG_DATA")
LOG_JSONPATH = config.get('S3', "LOG_JSONPATH")
SONG_DATA = config.get('S3', "SONG_DATA")

# ROLE
ARN = config.get('IAM_ROLE', "ARN")

# DROP TABLES
staging_events_table_drop = "drop table if exists staging_events;"
staging_songs_table_drop = "drop table if exists staging_songs;"
songplay_table_drop = "drop table if exists songplays;"
user_table_drop = "drop table if exists users;"
song_table_drop = "drop table if exists songs;"
artist_table_drop = "drop table if exists artists;"
time_table_drop = "drop table if exists time;"

# CREATE TABLES

staging_events_table_create= ("""
create table if not exists staging_events
(
artist          varchar,
auth            varchar, 
firstName       varchar,
gender          varchar,   
itemInSession   integer,
lastName        varchar,
length          float,
level           varchar, 
location        varchar,
method          varchar,
page            varchar,
registration    bigint,
sessionId       integer,
song            varchar,
status          integer,
ts              TIMESTAMP,
userAgent       varchar,
userId          integer
);
""")

staging_songs_table_create = ("""
create table if not exists staging_songs
(
song_id            varchar,
num_songs          integer,
title              varchar,
artist_name        varchar,
artist_latitude    float,
year               integer,
duration           float,
artist_id          varchar,
artist_longitude   float,
artist_location    varchar
);
""")

songplay_table_create = ("""
create table if not exists songplays(
    songplay_id integer identity(0,1),
    start_time timestamp not null,
    user_id varchar not null,
    level varchar,
    song_id varchar,
    artist_id varchar,
    session_id varchar not null,
    location varchar,
    user_agent varchar
)diststyle even;
""")

user_table_create = ("""
create table if not exists users(
    user_id integer not null,
    first_name varchar, 
    last_name varchar, 
    gender varchar, 
    level varchar 
)
diststyle all;
""")

song_table_create = ("""
create table if not exists songs(
   song_id varchar not null,
   title varchar not null,
   artist_id varchar not null,
   year integer not null,
   duration integer not null
)diststyle all;
""")

artist_table_create = ("""
create table if not exists artists(
   artist_id varchar not null, 
   name varchar(255) not null, 
   location varchar(255),
   latitude double precision, 
   longitude double precision
)diststyle all;
""")

time_table_create = ("""
create table if not exists time(
   start_time timestamp not null,
   hour smallint not null,
   day smallint not null,
   week smallint not null,
   month smallint not null,
   year smallint not null,
   weekday smallint not null
)diststyle all;
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events FROM {}
    CREDENTIALS 'aws_iam_role={}'
    COMPUPDATE OFF region 'us-west-2'
    TIMEFORMAT as 'epochmillisecs'
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
    FORMAT AS JSON {};
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
COPY staging_songs FROM {}
    CREDENTIALS 'aws_iam_role={}'
    COMPUPDATE OFF region 'us-west-2'
    FORMAT AS JSON 'auto' 
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;
""").format(SONG_DATA, ARN)


# Load table in the star schema
songplay_table_insert = ("""
insert into songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT se.ts        AS start_time,
    se.userid       AS user_id,
    se.level        AS level,
    ss.song_id      AS song_id,
    ss.artist_id    AS artist_id,
    se.sessionid    AS session_id,
    se.location     AS location,
    se.useragent    AS user_agent
FROM staging_events se
LEFT OUTER JOIN staging_songs ss ON (se.song = ss.title)
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
insert into users (user_id, first_name, last_name, gender, level)
select distinct se.userid   AS user_id,
    se.firstname            AS first_name,
    se.lastname             AS last_name,
    se.gender               AS gender,
    se.level                AS level
FROM staging_events se
WHERE se.userid IS NOT NULL;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
select distinct ss.song_id  AS song_id,
    ss.title                AS title,
    ss.artist_id            AS artist_id,
    ss.year                 AS year,
    ss.duration             AS duration
FROM staging_songs ss;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT ss.artist_id    AS artist_id,
    ss.artist_name              AS name,
    ss.artist_location          AS location,
    ss.artist_latitude          AS latitude,
    ss.artist_longitude         AS longitude
FROM staging_songs ss;
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT start_time                   AS start_time,
    EXTRACT (hour FROM start_time)      AS hour,
    EXTRACT (day FROM start_time)       AS day,
    EXTRACT (week FROM start_time)      AS week,
    EXTRACT (month FROM start_time)     AS month,
    EXTRACT (year FROM start_time)      AS year,
    EXTRACT (dayofweek FROM start_time) AS weekday
FROM songplays;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
