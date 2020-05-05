Title: Using a PostgreSQL database with Travis CI
Date: 2020-05-05 21:00
Category: CI
Tags: Postgres, CI
Slug: travis-postgres
Authors: Abhishek Pednekar
Summary: Adding a PostgreSQL test database as part of continuous integration with Travis CI
Cover: /static/images/black-gradient-article.jpg

In this post, we will see how one can use a PostgreSQL database to support automated tests during continuous integration (CI) with Travis CI.

Travis CI is a distributed CI service that can be integrated with a source control system like Github to automatically build a project and run tests whenever code is pushed to a remote repository.

We will be using a sample Django project as an example. The primary focus of the article will be Travis CI and PostgreSQL. Therefore, no prior knowledge of Django is needed. However, basic knowledge about PostgreSQL and Travis CI (particularly the usage of the `.travis.yml` file) is assumed.

## Updating the `.travis.yml` file

To use a PostgreSQL database during our Travis build, we will need to specify `postgres` under the `services` directive of our `.travis.yml` file.

```
services:
  - postgresql
```

Next, we will need to tell Travis to create a test database during the build. We can specify this as part of the `before_script` directive. Here, we are creating a test database called `test_postgres_db`. The database will be created by the default user (`-U`), `postgres`. The password field for this user will be empty.

```
before_script:
  - psql -c 'create database test_postgres_db;' -U postgres
```

## Environment variables and the database

Typically, all database connection details like the username, the password and the hostname are stored securely as environment variables which are maintained in `.env` files or directly added to the hosting server. Our Django application is also reading the PostgreSQL connection details from a `.env` file.

```
# settings.py

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': os.getenv("POSTGRES_HOST"),
        'PORT': '5432   '
    }
}
```

This is what our `.env` file looks like.

```
POSTGRES_USER=postgres-user
POSTGRES_PASSWORD=supersecurepassword
POSTGRES_DB=somedbname
POSTGRES_HOST=127.0.0.1
```

Now, since a `.env` file is never added to source control, our Travis build in this case will fail since it will be unable to find any database specific credentials in the remote repository. Fortunately, Travis CI lets us add environment variables as part of the build settings. Always remember that during a build, Travis CI creates a virtual machine to run our tests and then destroys it after the build is completed. We must, therefore, make use of temporary credentials and not specify production passwords or keys in the build settings.

## Adding environment variables in Travis CI

Once we provide Travis CI access to our remote repository, we will have access to the build settings page containing an **Environment Variables** section. It is here that we will add details of the test database that we specified in the `.travis.yml` file earlier.

The username, the database name and the host will be added as separate environment variables. Remember that the default password for the `postgres` user is blank/empty. Therefore, we do not need an environment variable for the password.

```
POSTGRES_DB=test_postgres_db
POSTGRES_HOST=localhost
POSTGRES_USER=postgres
```

![env_vars]({static}/images/index20/env_vars.jpg)

That's it! Travis CI will now provide us with a temporary PostgreSQL database whenever we run our tests during CI.

The full `.travis.yml` file:

```
language: python
python:
- '3.7'
install:
- pip install -r requirements.txt
services:
  - postgresql
before_script:
  - psql -c 'create database test_db;' -U postgres
script:
- pytest django_app
notifications:
  slack:
    rooms:
      - secure: xxxxxxx
```
