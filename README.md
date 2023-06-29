# Movie Tracking App

This project is a Movie Tracking App that allows users to keep track of the movies they have seen or want to see. It provides a set of RESTful APIs to perform CRUD operations on movies as well as user authentication.

## Backend Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).

## Installation

* Clone this repository


```bash
git clone https://github.com/MadhavWalia/movie-tracker.git
```


* Navigate to the project directory:


```bash
cd movie-tracker
```


* Create a .env file and fill in the required environment variables:


```bash
SECRET_KEY=<your_secret_key>
ALGORITHM=<your_algorithm>
ACCESS_TOKEN_EXPIRE_MINUTES=<access_token_expire_minutes>
REFRESH_TOKEN_EXPIRE_MINUTES=<refresh_token_expire_minutes>
MONGODB_CONNECTION_STRING=<mongodb_connection_string>
MONGODB_DATABASE_NAME=<mongodb_database_name>
REDIS_HOST=<redis_host>
REDIS_PORT=<redis_port>
REDIS_DB=<redis_db>
```


* Start the stack with Docker Compose:


```bash
docker-compose up -d
```


* Now you can open your browser and interact with these URLs:


Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost:8080

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost:8080/redoc


## Features

Add a movie:

```bash
POST /api/v1/movies 
```

Get a movie by its ID: 

```bash
GET /api/v1/movies/{movie_id} 
```

Get a movie by its title: (supports pagination)

```bash
GET /api/v1/movies
```

Update a movie:

```bash
PATCH /api/v1/movies/{movie_id} 
```

Delete a movie:

```bash
DELETE /api/v1/movies/{movie_id}  
```

Register a user:

```bash
POST /api/v1/auth/register
```

Log in a user:  

```bash
POST /api/v1/auth/login
```

Refresh the access token:  

```bash
POST /api/v1/auth/refresh
```

Log out a user:

```bash
POST /api/v1/auth/logout
```

Note: All endpoints, except for the login and signup endpoints, require authentication.

## License
This project is licensed under the MIT License.

