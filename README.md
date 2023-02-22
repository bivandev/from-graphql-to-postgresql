# From-GraphQl-to-PostgreSQL
This project is a simple app that downloads data from a GraphQL API and stores it in a PostgreSQL container. The app is containerized using Docker for easy deployment and management.

## Prerequisites
To run this app, you need to have Docker and Docker Compose installed on your machine.

## Installation
- Clone this repository to your local machine.
- Navigate to the project directory in your terminal.
- Run the following command to start the app: `docker-compose up -d`
- If you want see tables and count_rows showcase use this comand: `docker-compose logs -f app`

## Usage
After starting the app, it will download data from the specified GraphQL API and store it in the PostgreSQL container.
To access the data, you can use any PostgreSQL client and connect to the spacexdb database on port 5432 by this comand: 

`docker exec -it <db-container-name>  psql -U <username> -W <db-name>`

(default= `docker exec -it py_db_1  psql -U username -W spacexdb`)

You will be prompted for the password (default=`secret`)
