import requests
import psycopg2
from time import sleep

def download_data(query):
    url = "https://spacex-production.up.railway.app/"
    response = requests.post(url, json={'query': query})
    data = response.json()
    return data

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

def create_db(conn):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS rockets (
                    rocket_id VARCHAR(255) PRIMARY KEY,
                    rocket_name VARCHAR(255) NOT NULL,
                    rocket_type VARCHAR(255),
                    active BOOLEAN,
                    boosters INT,
                    cost_per_launch INT,
                    country VARCHAR(150),
                    first_flight DATE
                  );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS launches (
                    launch_id VARCHAR(255) PRIMARY KEY,
                    launch_date_utc VARCHAR(255),
                    launch_success BOOLEAN,
                    details TEXT,
                    rocket_id VARCHAR(255),
                    CONSTRAINT fk_rocket_id
                      FOREIGN KEY (rocket_id)
                      REFERENCES rockets(rocket_id)
                  );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS missions (
                    mission_id VARCHAR(255) PRIMARY KEY,
                    mission_name VARCHAR(255) NOT NULL,
                    launch_id VARCHAR(255),
                    CONSTRAINT fk_launch_id
                      FOREIGN KEY (launch_id)
                      REFERENCES launches(launch_id)
                  );""")

    conn.commit()

# Set the parameters
host = 'db'
port = '5432'
user = 'username'
password = 'secret'
database = 'spacexdb'

graph_query = """
{
    launches {
      id
      launch_date_utc
      launch_success
      details

      mission_id
      mission_name
      
      rocket {
        rocket {
          id
        }
      }
    }
    rockets {
      active
      boosters
      cost_per_launch
      country
      first_flight
      id
      name
      type
    }
}
"""

showcase_query="""
        SELECT relname AS table_name, n_live_tup AS row_count
        FROM pg_stat_user_tables
        ORDER BY n_live_tup DESC;
    """

# Connect to the database
def connection():
    conn = None
    while conn is None:
        try:
            conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        except psycopg2.OperationalError:
            sleep(5)
    return conn

def showcases(conn):
    cur = conn.cursor()
    cur.execute(showcase_query)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.commit()

conn = connection()

# Creating database
create_db(conn)

# Download the data from the SpaceX GraphQL API
data = download_data(graph_query)

# Store the data in the database
store_data(conn, data['data'])

# Data showcases
showcases(conn)

# Close the connection
conn.close()
