Title: Deploying a React application on a Linux server
Date: 2020-05-08 21:00
Category: Linux
Tags: ReactJs, Deployment
Slug: react-deployment
Authors: Abhishek Pednekar
Summary: Deploying a React application created with the `create-react-app` package
Cover: /static/images/gradient-texture-cubes.jpg

In this post, you will deploy a React application created with the `create-react-app` package. Unlike a React application that is built from scratch, `create-react-app` does not require us to install packages like `babel` or `webpack`. It enables you to get up and running quickly with a basic React application, without a lot of setup work. You can then build on this foundation to develop a full-featured application.

Web deployments on a bare-bones server can sometimes be tricky. This post will go over all the steps that need to be followed to deploy a React application on a virtual private server. The server will be a **DigitalOcean** droplet. The same steps can be followed on servers provisioned by other providers (like Linode). At the end of this article, you will be familiar with the pre-deployment and deployment tasks for a React application.

## Pre-requisites

1. A local `git` installation (if you are planning to use the same application as this post)
2. [Node.js](https://Node.js.org/en/) to test the application locally
3. A [DigitalOcean](https://www.digitalocean.com/) account or an account with any IAAS provider
4. One virtual private server running Ubuntu 18.04, including a non-root `sudo`-enabled user and a firewall
5. A React application to deploy

## Digital Ocean and the initial setup

You can refer to the [Deploying a Flask application on a Linux server - Part I](https://www.codedisciples.in/linux-vps-deployment1.html) article for details regarding signing up for a DigitalOcean account and performing the initial setup on the server. Although the two-parter article is written for the deployment of a Flask application, part one is generic. One recommended change would be to allow port `3000` instead of `5000` while setting up the firewall (step 5).

## Our React application

This post will not go into details about the application that will be deployed. At a high level, you will deploy a single-page React application which displays a random Chuck Norris joke from a public API. Refreshing the page or clicking on the button, displays a new joke. The complete code is accessible via the [Github repository](https://github.com/AbhishekPednekar84/react-demo-app). The `readme` file documents the steps to create a local setup.

!["Chuck"]({static}/images/index21/chuck.gif)

The root folder of the application contains a directory called `client`. All the React components and modules are present in this directory. Its structure is as follows.

```
.
└── client
    ├── package-lock.json
    ├── package.json
    ├── public
    │   ├── favicon.jpg
    │   └── index.html
    └── src
        ├── App.css
        ├── App.jsx
        ├── components
        ├── context
        └── index.js
```

## Preparing for deployment

This section deals with a set of pre-deployment tasks. These include,

1. Creating the production build of the application that will be deployed on the server
2. Creating a `server.js` file using Node.js and Express. This file will contain the path to the static assets that were built along with the port information
3. Test the build locally

To build the project, you will `cd` into the `client` directory and run the `npm run build` command. This will create a folder named `build` inside the `client` directory. The `build` folder contains the static assets which will be deployed on the server.

```
cd client

npm run build
```

The next step is to a create directory called `server` in the project root folder (in the same level as the `client` directory). Within `server`, you will create a `server.js` file with the following code.

```
// server.js

const express = require("express");
const path = require("path");

const app = express();

app.use(express.static(path.join(__dirname, "../client/build")));
app.get("/*", (req, res) => res.sendFile(path.join(__dirname, "./index.html")));

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
```

The code in `server.js` uses Node.js and `express` to specify the path to the `static` assets in the `build` folder. Also, you are ensuring that when accessing the root of the site, the `index.html` file is presented to an end-user. The application is being configured to listen for requests on port `3000`.

To run `server.js` you need the `express` package. To do that, you will first `cd` into the `server` directory and run `npm install express`. Finally, the build can be tested by running it locally using the `node server.js` command. If all goes fine, the application will be accessible on `http://localhost:3000`.

```
cd server

npm install express

node server.js
```

## Deploying the application

With the server now primed for deployment and the build tested locally, you can now copy over the necessary files/folders from the local machine to the DigitalOcean droplet. There are several ways to accomplish this. One way is to use the `scp` command.

Below is the complete list of files/folders that will be copied to the server.

```
.
├── client
│   ├── build
│   ├── package-lock.json
│   └── package.json
└── server
    └── server.js
```

On the server, these files/folders will be copied to a folder named `react-demo-app` located in the home directory of the user `demo`. You can place these anywhere. Remember to change the username, IP address and path when running the below `scp` command. Assuming we are in the project's root directory on our local machine (`/mnt/c/react-demo-app/` in this case), the command will copy the `client` and `server` subdirectories to the server.

```
cd /mnt/c/react-demo-app/

scp -r * demo@139.59.4.54:~/react-demo-app/
```

Most of the next steps will need to be carried out on our DigitalOcean droplet. You will need to log in with the `sudo` user to perform the next steps.

```
ssh demo@@139.59.4.54
```

### Installing Node.js

To install the latest version of Node.js and npm on the server, the following commands should be run.

```
sudo apt-get update

curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -

sudo apt install nodejs -y

```

To verify if the installation was successful, you can run

```
node --version

npm --version
```

### Installing project dependencies on the server

With Node.js and npm installed, you can now install our project dependencies. First, navigate to the `client` directory and install the dependencies using the `npm install` command.

```
cd ~/react-demo-app/client

npm install
```

Remember, that the `server` directory in `~/react-demo-app` only contains the `server.js` file. Also, to run the application using Node.js, you need the `express` package. To install `express`, navigate to the `server` directory and run `npm install express`.

```
cd ~/react-demo-app/server

npm install express
```

At this time, you can do a quick test to see if the site works by running `node server.js`. The site should be accessible at `http://<ipaddress>:3000`. Port `3000` will work provided the firewall (`ufw`) was configured to allow it.

```
cd ~/react-demo-app/server

node server.js
```

<br />
![site]({static}/images/index21/site.jpg)

Almost there! Disconnecting from the terminal will kill the process that is running the site. To keep the site running at all times, you will next install the PM2 process manager.

### Installing PM2 to run the site

PM2 will be installed as a global dependency using the `sudo npm install -g pm2` command. Once installed PM2 can be used to start and manage the site via the `pm2 start` command.

```
// Install PM2
sudo npm install -g pm2

// Navigate to the server directory and run the site with PM2
cd ~/react-demo-app/server

pm2 start server.js
```

You should see an output similar to this -

![pm2]({static}/images/index21/pm2.jpg)

Now, the site will continue to be accessible on `http://<ipaddress>:3000` despite disconnecting from the terminal. To check the status of PM2, you can run `sudo pm2 status`. You, however, don't want your users to always specify a port number while accessing the site. To ensure this, incoming traffic will be routed through the Nginx web server.

### Installing and configuring Nginx

Nginx will act as the webserver and route incoming traffic based on the specified configuration. You will need to first install it on the server and add some configuration.

```
// Installing Nginx
sudo apt install nginx -y
```

Before creating a configuration file for Nginx, you will need to make sure that Nginx can find the configuration that you are about to create. Check the contents of the `nginx.conf` file located in `/etc/nginx` using `cat /etc/nginx/nginx.conf` and look for the line `include /etc/nginx/sites-enabled/*;` in the `http` directive. If it does not exist, you will need to add it.

To add the line, open `nginx.conf` using the `nano` (or any suitable) editor.

```
sudo nano /etc/nginx/nginx.conf

http {
    ...
    ...

    include /etc/nginx/sites-enabled/*;
}

```

Next, delete the `default` nginx configuration and create a new configuration file called `demo` (it can be named anything) in the `/etc/nginx/sites-enabled/` directory.

```
// Delete existing Nginx configuration
sudo rm /etc/nginx/sites-enabled/default

sudo nano /etc/nginx/sites-enabled/demo
```

Add the below code to the `demo` file.

```
    server {
        server_name 139.59.4.54; # Whatever is your IP or domain

        location / {
            proxy_pass http://localhost:3000; # Whatever port your app runs on
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
```

To check the syntax of the nginx configuration file, you can run `sudo nginx -t`.

This is a very basic configuration and will suffice for this demo project. Based on this current configuration, Nginx will forward any request that comes to the root `/` of the site to `http://localhost:3000`. Remember that PM2 is running our site on port `3000` on the server. This way, users will just need to enter the domain name or IP address in their browsers and Nginx will make sure that their requests are routed correctly.

The `proxy_set_header` directives in the configuration will be included in the request headers. This is by no means the most complete Nginx configuration but a bare minimum one that serves the current purpose. The Nginx documentation lists the [complete set](http://nginx.org/en/docs/http/ngx_http_proxy_module.html) of directives.

Once the configuration file is saved, you can restart Nginx.

```
// Restarting Nginx

sudo systemctl restart nginx
```

The last step will be to configure the firewall to allow traffic on the `http/tcp` port. At this point, you can also delete port `3000` from our firewall rules.

```
// Add http
sudo ufw allow http/tcp

// Delete 3000
sudo ufw delete allow 3000

// Restart ufw
sudo ufw enable

```

This is what the status of our firewall should now look like.

```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
```

That's it! The fully functioning site will now be accessible on `http://<ipaddress>`.

![site2]({static}/images/index21/site2.jpg)

## Next steps

As next steps, you can create a CI/CD pipeline for automated deployments. Please refer to the [Continuous Deployment with Travis CI and DigitalOcean](https://codedisciples.in/travis-digitalocean) post for more details.
