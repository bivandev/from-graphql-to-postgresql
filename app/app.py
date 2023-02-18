import requests
import psycopg2
import json
from time import sleep

# Download the data from the SpaceX GraphQL API
def download_data(query):
    url = "https://spacex-production.up.railway.app/"
    response = requests.post(url, json={'query': query})
    data = response.json()
    return data

# Store the data in the database
def store_data(conn, data):
    cur = conn.cursor()
    for item in data['rockets']:
        cur.execute("""
            INSERT INTO rockets (rocket_id, rocket_name, rocket_type, active, boosters,cost_per_launch, country, first_flight) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
       """, (item['id'], item['name'], item['type'], item['active'], item['boosters'], 
             item['cost_per_launch'], item['country'], item['first_flight'],))
  
    for item in data['launches']:
        cur.execute("""
            INSERT INTO launches (launch_id, launch_date_utc, launch_success, details, rocket_id) 
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (item['id'], item['launch_date_utc'], item['launch_success'], item['details'], item['rocket']['rocket']['id']))

        cur.execute("""
            INSERT INTO missions (mission_id, mission_name)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (item['mission_id'][0], item['mission_name'] ))

        conn.commit()

# Load the JSON file with config data
with open('config.json', 'r') as f:
    config = json.load(f)

# Creating tables in the database
def create_db(conn):
    cur = conn.cursor()
    cur.execute(config['ct_rockets'])
    cur.execute(config['ct_launches'])
    cur.execute(config['ct_missions'])
    conn.commit()

# Connect to the database
def connection():
    conn = None
    while conn is None:
        try:
            conn = psycopg2.connect(database=config['database'], user=config['user'], 
                                    password=config['password'], host=config['host'], port=config['port'])
        except psycopg2.OperationalError:
            sleep(5)
    return conn

# Show tables and rows
def showcases(conn):
    cur = conn.cursor()
    cur.execute(config['showcase'])
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.commit()


conn = connection()

create_db(conn)

data = download_data(config['graphql'])

store_data(conn, data['data'])

showcases(conn)

conn.close()
