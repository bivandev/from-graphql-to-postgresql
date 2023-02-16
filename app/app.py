import requests
import psycopg2

def download_data(query):
    url = "https://spacex-production.up.railway.app/"
    response = requests.post(url, json={'query': query})
    data = response.json()
    return data

def store_data(conn, data):
    cursor = conn.cursor()
    for item in data:
        cursor.execute("INSERT INTO launches \
                      (launch_id, launch_date_utc, launch_success, details) \
                      VALUES (%s, %s, %s, %s)", 
                      (item['id'], item['launch_date_utc'], item['launch_success'], item['details'], ),
                      "INSERT INTO missions \
                      (mission_id, mission_name) \
                      VALUES (%s, %s, %s, %s)", 
                      (item['mission_id'], item['mission_name'] ),
                      "INSERT INTO rockets \
                      (rocket_id, rocket_name, rocket_type) \
                      VALUES (%s, %s, %s, %s)", 
                      (item['rocket']['rocket']['id'], item['rocket']['rocket_name'], item['rocket']['rocket_type']),
                      )
    conn.commit()

# Connect to the database
conn = psycopg2.connect(dbname="spacexdb", 
                        user="username",
                        password="secret",
                        host="db",
                        port="5432")

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
      rocket_name
      rocket_type
      rocket {
        id
      }
    }
  }
}
"""

data = download_data(query)

# Store the data in the database
store_data(conn, data['data']['launches'])

# Close the connection
conn.close()
