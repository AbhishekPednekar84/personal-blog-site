Title: Deploying a Flask application on a Linux server - Part II
Date: 2019-12-10 23:00
Category: Linux
Tags: Python, Linux, Deployment
Slug: linux-vps-deployment2
Authors: Abhishek Pednekar
Summary: Deploying a Flask application on a Virtual Private (Linux) Server
Cover: /static/images/black-gradient-article.jpg

In the [part one](https://www.codedisciples.in/linux-vps-deployment1.html) of this two-parter, we performed the initial set up to deploy a Flask application on a bare-bones virtual private server (VPS). In this post, we will deploy a Flask application and get it up and running with **nginx** and **gunicorn**.

The post assumes that the reader is familiar with the basics of Linux and Flask.

[Click here](https://github.com/AbhishekPednekar84/flask_demo_app) to download the source code of the Flask application that will be deployed. An important thing to note is that we will be using a `.env` file to configure our environment variables (see `.env.example` in the repository). So these variables will need to be configured before deploying the application on the server. Since the application uses reCAPTCHA during login, we will need to register on [Google reCAPTCHA](ttps://www.google.com/recaptcha/) to obtain the public and private keys. Also, for the database, we are using a Postgres database provisioned by [ElephantSQL](https://www.elephantsql.com/). The `DATABASE_URL` variable in the `.env` file will need to be modified depending on the database in use.

```
# Environment Variables

SECRET_KEY=
DATABASE_URL=
RECAPTCHA_PUBLIC_KEY=
RECAPTCHA_PRIVATE_KEY=
```

## Deploying the Flask application

### Step 1 - Copying the source code to the server

To being our deployment, we need to have our source code on the server. There are several ways to do this. For instance, we can install `git` on the server and run a `git clone`. However, to keep things simple, we will be copying the relevant files from our local computer to the server using the `scp` command.

The current git repository contains some directories (like tests) and configuration files that are not really needed to run our application in its current state. We will, therefore, be excluding those. Here is the list of directories and files that will be copied over.

```
# Structure of the flask_demo folder

.
├── app.py
├── commands.py
├── config.py
├── db.py
├── forms
│   ├── feedback.py
│   ├── login.py
│   └── register.py
├── lm.py
├── models
│   └── models.py
├── requirements.txt
├── static
│   ├── css
│   └── images
├── templates
│   ├── feedback
│   ├── home
│   ├── shared
│   └── user
├── views
│   ├── feedback_views.py
│   ├── home_views.py
│   ├── login_views.py
│   └── register_views.py
└── wsgi.py
```

The below `scp` command will be run on our local computer. The command will copy the folder named _flask_demo_ from the local drive to the _flaskuser_'s home directory on the server. We will need to be in the local directory containing _flask_demo_ before running the command.

```
scp -r flask_demo flaskuser@206.189.132.233:~/
```

### Step 2 - Setting up a virtual environment on the VPS

To verify if **Python 3** is installed on the server, execute the `python3` command on the terminal. If installed, we will see a Python REPL. If not, run `sudo apt install python3` to install Python.

We will need to create a virtual environment and install the application dependencies from the _requirements.txt_ file. The first step in this process will be to install `pip` and `venv`. Note that we can use any preferred packages like `virtualenv` or `pipenv` to create a virtual environment.

```
sudo apt install python3-pip
sudo apt install python3-venv
```

To create the virtual environment, we will use `python3 -m venv flask_demo/venv` and to activate the virtual environment, we will `cd` into the _flask_demo_ directory and run `source venv/bin/activate`.

Finally, we will install the packages specific to our application from the requirements file using `pip install -r requirements.txt`.

With the virtual environment now set up, let's perform a quick test to see if our flask application runs without any errors. We will do this by first setting the `FLASK_APP` environment variable and then using `flask run` to run the application. To check if everything is working as expected, we can access the url [http://206.189.132.233:5000](http://206.189.132.233:5000). This should render the application in the browser. However, as mentioned above, this is simply a test. We will be disabling port `5000` in a later step.

```
(venv) flaskuser@Flask-Demo-Server:~/flask_demo$ export FLASK_APP=app.py
(venv) flaskuser@Flask-Demo-Server:~/flask_demo$ flask run --host=0.0.0.0
 * Serving Flask app "app.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Testing the application this way assures us that we will not run into any code related issues later on. For instance, say we missed copying a file or did not configure an environment variable correctly, then this test will help us identify such issues.

### Step 3 - Configuring nginx

To serve the static content (HTML, CSS, JavaScript) of our website, we will be using **nginx** as our webserver.

To install nginx, we will run `sudo apt install nginx`.

To configure nginx for our application, we will need to create a configuration file which will allow the web server and our application to talk to each other. Depending on the version of nginx that was installed, nginx could be looking for an application configuration file in different locations. To ensure that nginx will look for the configuration file in the location that we expect, `cat` the `nginx.conf` file located in `/etc/nginx/` and verify if it contains the line `include /etc/nginx/sites-enabled/*;`. If not, open the file using `sudo nano nginx.conf` and add the line. This way nginx will look for our config in the `sites-enabled` directory.

Now, we will delete the default nginx configuration file that was created in the `sites-enabled` directory during the installation process.

```
(venv) flaskuser@Flask-Demo-Server:~$ sudo rm /etc/nginx/sites-enabled/default
```

Next, we will use the _nano_ text editor to create and save a new application configuration file.

```
(venv) flaskuser@Flask-Demo-Server:~$ sudo nano /etc/nginx/sites-enabled/flask-demo
```

We can now add the below code to the configuration file.

```
server {
        listen 80;
        server_name 206.189.132.233;

        location /static {
                alias /home/flaskuser/flask_demo/static;
        }

        location / {
                proxy_pass http://localhost:8000;
                include /etc/nginx/proxy_params;
                proxy_redirect off;
        }
}
```

Once we add this code, we can hit `Ctrl + X`, `Y` and `Enter` to save and close the file.

Let's go over the contents of this configuration file -

1. First, we are instructing nginx to listen for our application traffic on http port 80 of our VPS
2. Next, we are telling nginx where to look for the static content of our Flask application by providing the path to the `/static` directory as an alias
3. With the static content taken care of, nginx will act as a reverse proxy and pass any request processed at the root ([http://206.189.132.233](http://206.189.132.233)) of our application to the location specified in the `proxy pass` directive. This in our case is `gunicorn` which is running on the default port `8000`

Although we have set up nginx to listen on port 80, our firewall has not been opened for that port. To allow traffic on port 80, we will run `sudo ufw allow http/tcp`.

```
flaskuser@Flask-Demo-Server:~$ sudo ufw allow http/tcp

Rule added
Rule added (v6)
```

Next, we will no longer allow application traffic on port 5000 which we previously used for testing by running `sudo ufw delete allow 5000`.

```
flaskuser@Flask-Demo-Server:~$ sudo ufw delete allow 5000

Rule deleted
Rule deleted (v6)
```

Finally, we will run `sudo ufw enable` to persist the firewall related changes.

```
flaskuser@Flask-Demo-Server:~$ sudo ufw enable

Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup
```

`sudo ufw status` will show us the current ports allowed by the firewall.

```
flaskuser@Flask-Demo-Server:~$ sudo ufw status

Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
```

We will now restart nginx to make sure all the changes made in this section are saved and enabled.

```
flaskuser@Flask-Demo-Server:~$ sudo systemctl restart nginx
```

### Step 4 - Configuring gunicorn

While nginx serves the static content of our application, `gunicorn` handles the Python code. To install `gunicorn`, we will run `pip install gunicorn` on the server with the virtual environment activated.

To run `gunicorn` we need to specify the exact module name where the Flask application is created. Our code uses the `create_app` factory method which returns the Flask application. Also included in our code is the `wsgi.py` module that calls the factory method and stores the application instance in a variable named `app`.

```
# wsgi.py

from app import create_app
from config import Config

app = create_app(config_class=Config)
```

The command `gunicorn -w 3 wsgi:app` will start `gunicorn` on our server. We need to make sure that we are in the application folder while running this command.

```
(venv) flaskuser@Flask-Demo-Server:~/flask_demo$ gunicorn -w 3 wsgi:app

[2019-12-11 09:20:43 +0000] [14100] [INFO] Starting gunicorn 19.9.0
[2019-12-11 09:20:43 +0000] [14100] [INFO] Listening at: http://127.0.0.1:8000 (14100)
[2019-12-11 09:20:43 +0000] [14100] [INFO] Using worker: sync
[2019-12-11 09:20:43 +0000] [14103] [INFO] Booting worker with pid: 14103
[2019-12-11 09:20:43 +0000] [14104] [INFO] Booting worker with pid: 14104
[2019-12-11 09:20:43 +0000] [14105] [INFO] Booting worker with pid: 14105
```

The `-w` parameter specifies the number of worker processes which is 3 in our case. The general rule of thumb is to use the formula `(2 x number of CPU cores) + 1`. The command `nproc --all` will give us the number of CPU cores on our server.

At this point, we can access our application on [http://206.189.132.233](http://206.189.132.233).

<br />
![site]({static}/images/index16/site.jpg)

However, note that `gunicorn` is running in the foreground. In other words, if we were to close the terminal, our site would no longer be accessible. To avoid this, we will install a package called `supervisor` which will monitor `gunicorn` and keep it running as a daemon process.

### Step 5 - Configuring supervisor and logging

To install `supervisor` on the server, we will run `sudo apt install supervisor`.

Next, we will create a configuration file that will tell `supervisor` to run `gunicorn` and start it back up in case it stops for some reason. The file will also contain the paths to our standard output and error logs.

Once again, we will create this file (flask-demo.conf) using `nano` and add the lines of code indicated below - `nano /etc/supervisor/conf.d/flask-demo.conf`. To save the file - `Ctrl + X`, `Y` and `Enter`.

```
[program:flask_demo]
directory=/home/flaskuser/flask_demo
command=/home/flaskuser/flask_demo/venv/bin/gunicorn -w 3 wsgi:app
user=flaskuser
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/flask_demo/flask-demo.err.log
stdout_logfile=/var/log/flask_demo/flask-demo.out.log
```

The final steps in our deployment will be to create the log files that we configured in the`supervisor` configuration file followed by restarting `supervisor`.

```
(venv) flaskuser@Flask-Demo-Server:/$ sudo touch /var/log/flask_demo/flask-demo.err.log
(venv) flaskuser@Flask-Demo-Server:/$ sudo touch /var/log/flask_demo/flask-demo.out.log
```

To restart supervisor run `sudo supervisorctl reload`.

```
(venv) flaskuser@Flask-Demo-Server:/$ sudo supervisorctl reload
Restarted supervisord
```

We will now be able to access our website in spite of disconnecting from our terminal.

That's it! We now have a fully functional Flask site running in production. As next steps, we can add a custom domain and secure our site with `https`. Those, however, are out of scope for this series of posts.

Please be aware that the DigitalOcean droplet used in this post will be destroyed in the near future. So the URL [http://206.189.132.233](http://206.189.132.233) may not be accessible depending on when you are reading this post.
