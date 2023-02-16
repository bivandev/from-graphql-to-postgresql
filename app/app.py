import requests
import psycopg2
import json

def download_data(query):
    url = "https://spacex-production.up.railway.app/"
    response = requests.post(url, json={'query': query})
    data = response.json()
    return data

def store_data(conn, data):
    cursor = conn.cursor()
    for item in data:
        cursor.execute("INSERT INTO spacexdb (field1, field2, ...) VALUES (%s, %s, ...)", (item['field1'], item['field2'], ...))
    conn.commit()

# Connect to the database
conn = psycopg2.connect(dbname="spacexdb", 
                        user="username",
                        password="secret",
                        host="db",
                        port="5432")


# Download the data from the SpaceX GraphQL API
queryL = """
{
   launches {
    id
    launch_date_utc
    launch_success
    details
    upcoming

    mission_id
    mission_name
    
    rocket {
      rocket_name
      rocket_type
    }
  }
}
"""

dataL = download_data(queryL)
dataR = download_data(queryR)
dataM = download_data(queryM)

# Store the data in the database
store_data(conn, dataL['data']['launches'])

# Close the connection
conn.close()
