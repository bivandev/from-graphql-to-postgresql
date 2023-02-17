import requests
import psycopg2
from time import sleep

def download_data(query):
    url = "https://spacex-production.up.railway.app/"
    response = requests.post(url, json={'query': query})
    data = response.json()
    return data

def store_data(conn, data):
    cursor = conn.cursor()
    for item in data['rockets']:
        cursor.execute("""INSERT INTO rockets (rocket_id, rocket_name, rocket_type, active, boosters,cost_per_launch, country, first_flight) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                      (item['id'], item['name'], item['type'], item['active'], item['boosters'], 
                       item['cost_per_launch'], item['country'], item['first_flight'],))
    
    for item in data['launches']:
        cursor.execute("INSERT INTO launches (launch_id, launch_date_utc, launch_success, details, rocket_id) VALUES (%s, %s, %s, %s, %s)", 
                      (item['id'], item['launch_date_utc'], item['launch_success'], item['details'], item['rocket']['rocket']['id']))

        cursor.execute("INSERT INTO missions (mission_id, mission_name) VALUES (%s, %s)", 
                      (item['mission_id'][0], item['mission_name'] ))
    conn.commit()

def create_db(conn):
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS rockets (
                    rocket_id VARCHAR(255) PRIMARY KEY,
                    rocket_name VARCHAR(255) NOT NULL,
                    rocket_type VARCHAR(255),
                    active BOOLEAN,
                    boosters INT,
                    cost_per_launch INT,
                    country VARCHAR(150),
                    first_flight DATE
                  );""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS launches (
                    launch_id VARCHAR(255) PRIMARY KEY,
                    launch_date_utc VARCHAR(255),
                    launch_success BOOLEAN,
                    details TEXT,
                    rocket_id VARCHAR(255),
                    CONSTRAINT fk_rocket_id
                      FOREIGN KEY (rocket_id)
                      REFERENCES rockets(rocket_id)
                  );""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS missions (
                    mission_id VARCHAR(255) PRIMARY KEY,
                    mission_name VARCHAR(255) NOT NULL,
                    launch_id VARCHAR(255),
                    CONSTRAINT fk_launch_id
                      FOREIGN KEY (launch_id)
                      REFERENCES launches(launch_id)
                  );""")

    conn.commit()

# Connect to the database
def connection():
  try:
      conn = psycopg2.connect(database="spacexdb", user="username", password="secret", host="db", port="5432")
  except psycopg2.OperationalError:
      sleep(5)
      connection()
  finally:
      return conn
  
conn = connection()

#Creating database
create_db(conn)
# Download the data from the SpaceX GraphQL API
query = """
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

data = download_data(query)

# Store the data in the database
store_data(conn, data['data'])

# Close the connection
conn.close()
