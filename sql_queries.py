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

staging_events_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist varchar,
    auth varchar,
    firstName varchar,
    gender varchar,
    itemInSession integer,
    lastName varchar,
    length double precision,
    level varchar,
    location varchar,
    method varchar,
    page varchar,
    registration timestamp,
    sessionId integer,
    song varchar,
    status integer,
    ts timestamp,
    userAgent varchar,
    userId integer
);
""")

staging_songs_table_create = ("""
 create table if not exists staging_songs (
        num_songs integer,
        artist_id varchar,
        artist_latitude double precision,
        artist_longitude double precision,
        artist_location  varchar,
        artist_name varchar,
        song_id varchar,
        title varchar,
        duration double precision,
        year smallint
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
   artist_id integer not null, 
   name varchar(100) not null, 
   location varchar(255),
   lattitude double precision, 
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
copy staging_events from {} 
credentials 'aws_iam_role={}'
""").format(LOG_DATA, ARN)

staging_songs_copy = ("""
copy staging_songs from {} 
credentials 'aws_iam_role={}'
""").format(SONG_DATA, ARN)



# FINAL TABLES
songplay_table_insert = ("""
# insert into table songplays() 
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
