Title: Running PostgreSQL in a Docker Container
Date: 2019-09-18 23:00
Category: Docker
Tags: Docker, Postgres
Slug: docker-postgres
Authors: Abhishek Pednekar
Summary: Running PostgreSQL and pgAdmin 4 in Docker containers
Cover: /static/images/black-gradient-article.jpg

Containers have revolutionized the way we code, build and ship software. They also provide a means wherein we no longer need to mandatorily install software but run the software in a container instead. In this post, we will run **PostgreSQL** (postgres) and **pgAdmin 4** in seprate **Docker Containers** on a **Windows** machine using Docker Toolbox. We will then connect to the postgres database from pgAdmin.

**PostgreSQL** is a free and open-source relational database management system<br/>
**pgAdmin 4** is an open-source database management tool for postgres

## Creating the Docker containers
To create the postgres and pgAdmin Docker containers, we will use a **docker-compose.yml** file. 

```
version: '3.2'
services:

  postgres:
    image: postgres:latest
    ports:
      - '5432:5432'
    container_name: postgres
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres-pass'
      POSTGRES_DB: 'postgres'
    volumes:
      - type: bind
        source: .
        target: /var/lib/postgres/data

  pgAdmin4:
    image: dpage/pgAdmin4
    container_name: pgAdmin4
    depends_on:
      - postgres
    ports:
      - '8080:80'
    environment:
      pgAdmin_DEFAULT_EMAIL: 'admin@pgAdmin.com'
      pgAdmin_DEFAULT_PASSWORD: 'pgAdmin-pass'  
```

Let's go over the attributes in the file.<br/>

**version** is the version of the Compose file format<br/>
**services** provides configuration for the containers that will be started<br/>
**image** is the application image that will be downloaded from [Docker Hub](https://hub.docker.com/)<br/>
**ports** are the exposed host and container ports<br/>
**environment** contains the environment variables for the services defined in the yaml file<br/>
**volume** signifies the location of the persistent data stored in the container

To create the containers, we will run the command `docker-compose -f docker-compose.yml up` and to verify whether the containers were created and are running, we will run `docker container ls`.

<br/>
![docker1]({static}/images/index9/docker1.jpg)

## Running pgAdmin 4
First, we will run pgAdmin. Note that the docker-compose.yml specifies 8080 as the port for the Docker host. However, since we are running on Windows, we cannot access pgAdmin using http://localhost:8080. Instead, we will need to use the ip address of our virtual machine that is running Docker Toolbox. To get the ip address run `docker-machine ls`. The ip address, in this case, is 192.168.99.101. Therefore our url for pgAdmin will be http://192.168.99.101:8080.

To log in, we will use the default email and password specified in the yaml file.

<br/>
![pgAdmin1]({static}/images/index9/pgAdmin1.jpg)

## Connecting to a postgres database
Once logged into pgAdmin, we will select the **Add New Server** option to connect to our postgres database.

<br/>
![postgres1]({static}/images/index9/postgres1.jpg)

<br/>
The database name, username and password will be as specified in the yaml file. The hostname will once again be the ip address of our virtual machine.

<br/>
![postgres2]({static}/images/index9/postgres2.jpg)

<br/>
![postgres3]({static}/images/index9/postgres3.jpg)

## Creating database objects with psql
To create database objects, we can either use pgAdmin or the **psql** command line. To run psql, we will first need to run **bash** in the container, then connect to our database and finally run our SQL statements. As an example, here is how we can create a new table.

<br/>
![psql]({static}/images/index9/psql.jpg)

<br/>
![postgres4]({static}/images/index9/postgres4.jpg)

<br/>
Here is a link to official postgres [tutorial](https://www.postgresql.org/docs/11/tutorial.html).