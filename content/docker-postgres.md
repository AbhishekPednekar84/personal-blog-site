Title: Running PostgreSQL in a docker Container
Date: 2019-09-18 23:00
Category: Docker
Tags: Docker, Postgres
Slug: docker-postgres
Authors: Abhishek Pednekar
Summary: Running PostgreSQL and pgAdmin 4 in docker containers
Cover: /static/images/black-gradient-article.jpg

Containers have revolutionized the way software is built and shipped. They also provide a means wherein software no longer needs to be mandatorily installed since it can be directly run in the container. In this post, you will run **PostgreSQL** (postgres) and **pgAdmin 4** in separate docker containers on a **Windows** machine using docker toolbox. Once both docker containers are up, you will use pgAdmin to connect to the postgres database.

This post assumes that the reader has `docker` installed and running on a Windows machine. Installation instructions can be found in the [official documentation](https://docs.docker.com/toolbox/toolbox_install_windows/).

**PostgreSQL** is a free and open-source relational database management system<br/>
**pgAdmin 4** is an open-source database management tool for postgres

## Creating the docker containers

To create the postgres and pgAdmin docker containers, we will use a `docker-compose.yml` file.

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

`version` is the version of the Compose file format<br/>
`services` provides configuration for the containers that will be started<br/>
`image` is the application image installed from [Docker Hub](https://hub.docker.com/)<br/>
`ports` are the exposed host and container ports<br/>
`environment` contains the environment variables for the services defined in the `yaml` file<br/>
`volume` signifies the location of the persistent data stored in the container

To create the containers, you will need to run the `docker-compose -f docker-compose.yml up` command. To verify if the docker containers are running, you can use the `docker container ls` command.

<br/>
![docker1]({static}/images/index9/docker1.jpg)

## Running pgAdmin 4

The `docker-compose.yml` file specifies `8080` as the port to run pgAdmin. However, since docker is running on Windows, pgAdmin cannot be accessed using `http://localhost:8080`. Instead, you will need to use the ip address of the virtual machine that is running docker toolbox. To get the ip address, you can run the `docker-machine ls` command. The ip address, in this case, is `192.168.99.101`. Therefore the url for pgAdmin will be `http://192.168.99.101:8080`.

To log in, you will use the default email and password specified in the `yaml` file.

<br/>
![pgAdmin1]({static}/images/index9/pgAdmin1.jpg)

## Connecting to a postgres database

Once logged into pgAdmin, you will select the **Add New Server** option to connect to the postgres database.

<br/>
![postgres1]({static}/images/index9/postgres1.jpg)

<br/>
The database name, username and the password will be as specified in the `yaml` file. The hostname will once again be the ip address of the virtual machine.

<br/>
![postgres2]({static}/images/index9/postgres2.jpg)

<br/>
![postgres3]({static}/images/index9/postgres3.jpg)

## Creating database objects with psql

To create database objects, we can either use pgAdmin or the `psql` command line. To run `psql`, you will first need to run a `bash` shell in the container, then connect to our database and finally run our SQL statements. As an example, here is how you can create a new table.

<br/>
![psql]({static}/images/index9/psql.jpg)

<br/>
![postgres4]({static}/images/index9/postgres4.jpg)

<br/>
Here is a link to official postgres [tutorial](https://www.postgresql.org/docs/11/tutorial.html).
