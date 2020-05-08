Title: Deploying a React application on a Linux server
Date: 2020-05-08 21:00
Category: Linux
Tags: ReactJs, Deployment
Slug: react-deployment
Authors: Abhishek Pednekar
Summary: Deploying a React application created with the `create-react-app` package
Cover: /static/images/gradient-texture-cubes.jpg

In this article, we will deploy a React application created with the `create-react-app` package. This article assumes that the reader has a basic understanding of Node.js and the React framework. We will therefore not be looking into any of the application-specific code. The focus will be on the steps to deploy the application on a virtual private (Linux) server (VPS). For this demo, we will be using a virtual server provisioned by **DigitalOcean**.

## Pre-requisites

1. A Linux server with `root` / `sudo` access
2. [Node.js](https://Node.js.org/en/) to test locally

## Digital Ocean and the initial setup

Please refer to the [Deploying a Flask application on a Linux server - Part I](https://www.codedisciples.in/linux-vps-deployment1.html) for details regarding signing up for a Digital Ocean account and performing the initial setup on the server. Although the two-parter article is written for the deployment of a Flask application, part one is generic. One recommended change would be to allow port `3000` instead of `5000` while setting up the firewall (step 5).

## Our React application

The application that we will deploy is a simple single-page React application. It displays a random Chuck Norris joke from a public API. Refreshing the page or clicking on the button, displays a new joke. The complete code is accessible via the [Github repository](https://github.com/AbhishekPednekar84/react-demo-app).

!["Chuck"]({static}/images/index21/chuck.gif)

As indicated earlier, the application is created using the `create-react-app` package. In other words, we did not install `babel`, `webpack` or any of the other goodies that go into creating a React application from scratch. At the root of our application, we have a directory called `client` which contains our React components and modules. Here is what the `client` directory structure looks like.

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

We will be using Node.js to run our application on the server. However, before we start deploying, we will need to perform a set of tasks locally -

1. Build our project to create the binaries that will be deployed on our server
2. Create a `server.js` file with information for Node.js on how to find our site's static assets and port information
3. Use Node.js to test the build locally

To build our project, we will `cd` into the `client` directory and run the `npm run build` command. This will create a directory named `build` inside `client`. The `build` directory will contain the static assets which we will later copy over to our server.

Next, we will create a directory called `server` in the project root folder, within it, we will create a file called `server.js` and add the below code to the file.

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

The code in `server.js` uses `express` to specify the path to the `static` assets in our `build` directory. Also, we are ensuring that when accessing the root of our site, we are loading the `index.html` file and that the application will run on port `3000`.

To run `server.js` we need the `express` package. To do that, we will first `cd` into the `server` directory and run `npm install express`. Finally, we can test our build by running it locally using the `node server.js` command. If all goes fine, our application will be accessible on `http://localhost:3000`.

```
cd server

npm install express

node server.js
```

## Deploying the application

With our server now primed for deployment and our build tested locally, we can now copy over the necessary files/folders from our local machine to our DigitalOcean droplet. There are several ways to this. To keep things simple, we will use the `scp` command.

For the deployment, we will be copying the `server.js` file from the `server` directory. From the `client` directory, we will only be copying the entire `build` folder along with the `package.json` and `package-lock.json` files.

```
.
├── client
│   ├── build
│   ├── package-lock.json
│   └── package.json
└── server
    └── server.js
```

We will be moving our project files to a directory called `react-demo-app` located in the home directory of the user `demo`. Remember to change the username, IP address and path when running the below command. Assuming we are in the project root directory on our local machine (`/mnt/c/Learning/Live/react-demo-app/` in this case), the command will copy the `client` and `server` subdirectories to the server.

```
cd /mnt/c/Learning/Live/react-demo-app/

scp -r * demo@139.59.4.54:~/react-demo-app/
```

Most of the next steps will need to be carried out on our DigitalOcean droplet. So let's login with our `sudo` user - `ssh demo@139.59.4.54`.

### Installing Node.js

To install the latest version of Node.js and npm, we will run the following commands.

```
sudo apt-get update

curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -

sudo apt install nodejs -y

```

To verify if the installation was successful, we can run

```
node --version

npm --version
```

### Installing project dependencies on the server

With Node.js and npm now installed, we can install our project dependencies. We will first navigate to the `client` directory and install the dependencies.

```
cd ~/react-demo-app/client

npm install
```

Remember, that our `server` directory in `~/react-demo-app` only contains the `server.js` file. Also, to run our application using Node.js, we need the `express` package. To install express, we will `cd` into the `server` directory and run `npm install express`.

```
cd ~/react-demo-app/server

npm install express
```

At this time, we can do a quick test to see if our site works by running `node server.js`. The site should be accessible at `http://<ipaddress>:3000`. Port `3000` will work provided we configured the firewall to `allow` it during the initial setup

```
cd ~/react-demo-app/server

node server.js
```

<br />
![site]({static}/images/index21/site.jpg)

We are almost there! Disconnecting from the terminal will kill the process running our site. We will, therefore, install the PM2 process manager to run our site.

### Installing PM2 to run the site

We will be installing PM2 as a global dependency using the `sudo npm install -g pm2` command. Once installed we can use PM2 to start and manage our application using the `pm2 start` command.

```
cd ~/react-demo-app/server

pm2 start server.js
```

We should see an output similar to this -

![pm2]({static}/images/index21/pm2.jpg)

Now, the site will continue to be accessible on `http://<ipaddress>:3000` despite disconnecting from the terminal. To check the status of PM2, we can run `sudo pm2 status`. Well, we are close now. We don't want our users to always specify a port number while accessing our site. We will, therefore, route our traffic using a web server called Nginx.

### Installing and configuring Nginx

Nginx will act as our webserver and route incoming traffic based on some configuration. We will need to first install it on our server and add some configuration.

To install Nginx, we will run `sudo apt install nginx -y`. Before we create a configuration file for Nginx, we will need to make sure that Nginx can find the configuration that we are about to create. Check the contents of the `nginx.conf` file located in `/etc/nginx` using `cat /etc/nginx/nginx.conf` and look for the line `include /etc/nginx/sites-enabled/*;` in the `http` directive. If it does not exist, we will need to add it.

To add the line, we will open `nginx.conf` using the `nano` (or any suitable) editor.

```
sudo nano /etc/nginx/nginx.conf

http {
    ...
    ...

    include /etc/nginx/sites-enabled/*;
}

```

Next, we will delete the `default` nginx configuration by running `sudo rm /etc/nginx/sites-enabled/default`. Once deleted, we will create a new configuration file called `demo` (it can be named anything) in the `/etc/nginx/sites-enabled/` directory.

```
sudo nano /etc/nginx/sites-enabled/demo
```

We will add the following code to the `demo` file.

```
    server_name 139.59.4.54; # Whatever is your IP or domain

    location / {
        proxy_pass http://localhost:3000; # Whatever port your app runs on
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
```

To check the syntax of our nginx configuration file, we can run `sudo nginx -t`.

This is a very basic configuration and will suffice for this demo project. We are telling nginx to forward any request that comes to the root `/` of our site to `http://localhost:3000` which is our application running on the server. This way, users will just need to enter the domain name or ipaddress in their browsers and Nginx will make sure that their requests are routed correctly.

We have also added some `proxy_set_header` directives that will be included in the request headers. This is by no means the most complete Nginx configuration but a bare minimum one that serves the current purpose. The Nginx documentation lists the [complete set](http://nginx.org/en/docs/http/ngx_http_proxy_module.html) of directives.

We will now restart Nginx using `sudo systemctl restart nginx`

The last step will be to configure our firewall to allow traffic on the `http/tcp` port. At this point, we can also delete port `3000` from our firewall rules.

```
sudo ufw allow http/tcp

sudo ufw delete allow 3000

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

That's it! Our site will now be accessible on `http://<ipaddress>`.

![site2]({static}/images/index21/site2.jpg)
