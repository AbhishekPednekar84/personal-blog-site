Title: Deploying a Flask website on Heroku
Date: 2019-11-06 17:00
Category: Flask
Tags: Flask, Python, Heroku
Slug: flask-heroku
Authors: Abhishek Pednekar
Summary: Steps to deploy a Flask website using Heroku

In this post, we will be deploying a **Flask** application using [Heroku](https://www.heroku.com/). Heroku is a popular 
Platform as a Service (PaaS) that is used to deploy, manage and scale web applications. It comes with a lot of features 
built-in that abstract away most of the complications involved in traditional web-based deployments. Deployments on 
Heroku are quick and the platform ensures that you do not have to worry about the infrastructural maintenance headache's that accompany website / server maintenance.  
 
The site that we will be deploying is [https://bit.ly/flask-app](https://bit.ly/flask-app). The complete source code is 
available [here](https://github.com/AbhishekPednekar84/flask_demo_app).

This post assumes that the reader is familiar with the basics of Python and Flask. The post does not include the steps to create an account on Heroku as the process is pretty straightforward.

## Our flask application

The application that we are deploying uses some popular flask extensions like `flask-sqlalchemy`, `flask-login` etc... 
A complete list can be found in the *requirements.txt* file in the repository. It is critical to have the requirements file in our repository to not only have Heroku install the dependencies 
but also because it helps Heroku identify this as a Python project. The application is a website for a fake organic produce startup and contains a few forms wherein a new user can register or an existing user may login. Upon 
logging in, the user will be redirected to a feedback page to provide feedback of their most recent experience with the company.

Before we start deploying, let's clone the repository using `git clone https://github.com/AbhishekPednekar84/flask_demo_app`. 
As we will see later on, Heroku requires us to specify the repository url as part of the deployment process. Now, while 
I admit that this repository contains our finished code (with the Heroku specific files) and can be deployed as-is, in a real scenario, we 
will probably be working on a local repository and periodically pushing our changes to a remote repository. Since this is a demo, we will not be creating 
new branches and will be using the *master* branch itself. If you are planning to deploy the same demo application, you can push this to your remote 
repository using `git push -u <your remote repo url>`.

## Getting started with Heroku

Once logged into Heroku, we will see an option called *Create new app* on the dashboard. In Heroku nomenclature, a server 
is called as a **dyno**, We will be using a free dyno for this demo. 

The region can be the United States or Europe. This doesn't matter for our demo application. I've chosen Europe simply 
because, geographically, my current location is closer to Europe. We will not be adding a pipeline in this example.

<br/>
![heroku-create]({static}/images/index13/heroku-create.jpg)

On the subsequent page, we will be selecting our deployment method as **GitHub**. As mentioned in the previous section, 
this will trigger a build whenever we push changes to our GitHub repository. We will need to authorize Heroku to access 
GitHub repositories and specify which repository will be used in our current deployment.

<br/>
![heroku-setup]({static}/images/index13/heroku-setup.jpg)

Next, we will enable automatic deployments. At this point, I would like to point out that our repository does have continuous 
integration (CI) configured in TravisCI due to which we will be checking the *Wait for CI to pass before deploy* box. However, 
this can be skipped by simply removing the .travis.yml file from the repository. A separate article pertaining to the CI pipeline will be posted soon.

<br/>
![auto-deploy]({static}/images/index13/auto-deploy.jpg)

This completes our initial setup on Heroku.

## Creating environment variables

For the local deployment, all our environment variables were included in a `.env` file (which was deliberately excluded 
from the repository). There is however a skeleton file called `.env.example` that shows all the attributes that need to 
be configured. The values of these attributes are being read into our `Config` class in `config.py`.

On Heroku, rather than using a `.env` file, we will be creating the environment variables on the dashboard itself. The 
first of these will be a connection string to a new **Postgres** database. To do this, on the *Resources* section of our 
dashboard, we will specify **heroku-postgres** and provision the database on our free dyno.

<br/>
![postgres]({static}/images/index13/postgres.jpg)

<br/>
![postgres2]({static}/images/index13/postgres2.jpg)

Once this is complete, we can see the environment variable containing the connection string by navigating to the *Settings* 
and revealing our config variables.

<br/>
![postgres3]({static}/images/index13/postgres3.jpg)

Since we have a few more to add (see `.env.example`), we will do that as well. To obtain the *reCAPTCHA* public and private keys,
 one will need to signup for the service on [Google](https://www.google.com/recaptcha/) and follow the steps. 

Here is a final screenshot of this section.

<br/>
![env-vars]({static}/images/index13/env-vars.jpg)

## Creating the Heroku `Procfile`

Heroku requires a file named `Procfile` that contains all the commands to be executed by an app on startup. The commands 
need to be specified using the syntax `<process name>: <command>`. Before, we update this file, let's look at how we are exposing 
our flask application instance.

The `app.py` file in our project contains a `create_app` function which returns our flask application named **app**. To correctly specify 
this in our Procfile, we have a separate module called `wsgi.py` containing the following code.

```
from app import create_app
from config import Config

app = create_app(config_class=Config)
```  

The `app` instance defined here can be used in our Procfile. For this demo, we will be using `gunicorn` as our WSGI server. 
So let's first install it using `pip install gunicorn` and add it to our requirements using `pip freeze > requirements.txt`. 

This is the command that will be included in the Procfile - `web: gunicorn wsgi:app` This tells Heroku to use the Heroku **web** process run an 
application called **app** that is present in a module named **wsgi** using **gunicorn**. 

At this point, if you have worked on these changes locally, they should be pushed to the remote repository using `git push origin master` 
so that an initial build can be triggered. We can follow the build in the *Overview* section of the dashboard. Details of 
any build errors can be found in the logs - *More > View Logs*.

<br/>
![build]({static}/images/index13/build.jpg)

## Creating our database tables

The `models.py` file in our `models` package indicates that the application uses two tables - `UserModel` and `FeedbackModel`.

To create these on Heroku, we will be using a custom flask command called *create_tables* present in `commands.py`. 
The command is created in `app.py` as part of the app creation process - `app.cli.add_command(create_tables)`.

To run this command, navigate to *More > Run Console* and run the command - `flask run create_tables`. If everything runs 
as expected, we will simply see a *Process Exited* message on the console.
 
<br/>
![console]({static}/images/index13/console.jpg)

Now our app is fully set up and deployed. To run the application, click *Open App* on the dashboard. The url 
[https://flask-organic-foods-app.herokuapp.com/](https://flask-organic-foods-app.herokuapp.com/) was assigned by Heroku. 
This can be changed with a custom domain name in the application settings.

<br/>
![site]({static}/images/index13/site.jpg)
 




