Title: Deploying a Flask application on a Linux server - Part I
Date: 2019-11-20 23:00
Category: Linux
Tags: Python, Linux
Slug: linux-vps-deployment1
Authors: Abhishek Pednekar
Summary: Set up a bare-bones Virtual Private (Linux) Server from scratch
Cover: /static/images/black-gradient-article.jpg

In the [previous](https://www.codedisciples.in/flask-heroku.html) post, we deployed a Flask application on Heroku. In this post, we will deploy the [same application](https://github.com/AbhishekPednekar84/flask_demo_app) on a Virtual Private (Linux) Server (VPS). Several providers offer VPS' hosted on a cloud-based infrastructure. [Linode](https://linode.com) and [DigitalOcean](https://digitalocean.com) are the more popular ones. We will be using DigitalOcean for our deployment. However, the setup and deployment steps will be the same for Linode or any other provider. 

This is the part one of a two-part series. In this post, we will set up a bare-bones Linux server and prime it for deployment. In part two, we will deploy the Flask application with **nginx** and **gunicorn**.

The post assumes that the reader is familiar with the basics of Linux.

## Getting started with DigitalOcean

At the time of posting this article, DigitalOcean is offering a [$50 credit](https://try.digitalocean.com/python/?utm_medium=podcast&utm_source=pythonbytes&utm_campaign=DO_Dev_Signup_Cold_Python) as part of its sponsorship of the [Python Bytes Podcast](https://pythonbytes.fm). 

To get started with DigitalOcean, we will first need to [sign up](https://www.digitalocean.com/) and create an account. Once logged in, we can create and configure a droplet (VPS). Below are the steps.

1. Create a new project and provide an appropriate name (Ex: *Flask Demo App*)
2. On the project's control panel, select *Get started with a Droplet* to create a VPS
3. Choose an image. We will be using *Ubuntu 18.04.3* for our demo app. If choosing another Linux distribution, the commands in the subsequent section might vary.
4. Choose a plan - the most inexpensive (Standard / $5 per month) plan will suffice
5. Select a datacenter region. This would ideally be one closest to where a majority of our end users are located. In the present case, any region will do
6. For the authentication process, we will select *One-time password* for now and set up an SSH key later on. The password will be sent to the email address provided at the time of registration
7. Give an appropriate name (Ex: *Flask-Demo-Server*) for the server and click on *Create Droplet*  

## Setting up our server

### Step 1 - Logging in with the **root** user 

To connect to the droplet via **ssh**, we will be using the *Cmder* CLI tool and *Windows Subsystem for Linux* (WSL). Our initial login will be with the **root** user. Also, we will need to note down the public ip address of our server (which can be found in our project's control panel) as that will be used several times during the setup.

```
ssh root@206.189.132.233
```

Once we run the above command, we will need to accept the authentication warning and provide the one-time **root** password sent to the registered email. Since this is our first time logging in, we will be prompted to change the **root** password. Since **root** is an admin account with extended privileges, we will create an alternate user with slightly lesser privileges (than the **root** user) and use that for the remainder of our setup and deployment.

### Step 2 - Creating a new user

To create a new user, we will run the `adduser` command while logged in as the **root** user. We will be prompted to enter a password for the new user along with filling up some optional user-specific details.

```
root@Flask-Demo-Server:~# adduser flaskuser
```

Next, we will add the new user (*flaskuser*) to the *sudo* group. This will ensure that when we are logged in with this user, we can prepend the `sudo` keyword to our commands and execute them with superuser privileges.

```
root@Flask-Demo-Server:~# adduser flaskuser sudo
```

### Step 3 - Setting up key-based authentication

To enhance security, we will now setup an **SSH key** with a passphrase for *flaskuser*. There are several ways to do this. One way is to create the SSH keys on our local machine and then run a secure copy (`scp`) command to copy the public key to the *authorized_keys* file on the server.

As mentioned earlier, we will be using WSL to generate the key locally using the `ssh-keygen` command. When prompted, just hit enter to create the keys with their default names and set a **passphrase**. Although the passphrase is optional, it is recommended for added security.

```
abhi_ap@Abhi-Dell:~$ ssh-keygen
```

Running the above command will create the public (id_rsa.pub) and the private (id_rsa) keys in the `/home/<user>/.ssh` directory on the local machine. 

Prior to copying the key to the server, we will need to create a .ssh directory in *flaskuser*'s /home directory. So let's login with *flaskuser* and the password that we provided in the previous step and create the directory with the `mkdir .ssh` command.

```
root@Flask-Demo-Server:~# ssh flaskuser@206.189.132.233
```

```
flaskuser@Flask-Demo-Server:~$ mkdir .ssh
```

Now, from our local machine, we will run the `scp` command. We need to ensure that we are are in the local .ssh directory before running the below command.

```
abhi_ap@Abhi-Dell:/home$ cd ~
abhi_ap@Abhi-Dell:~$ cd .ssh

abhi_ap@Abhi-Dell:~/.ssh$ scp id_rsa.pub flaskuser@206.189.132.233:.ssh/authorized_keys

flaskuser@206.189.132.233's password:
id_rsa.pub
```

Hopefully, that wasn't too confusing. To complete this part of the setup, we will use the `chmod` command to change the permissions of the .ssh directory and it's contents. For those unfamiliar with `chmod`, [here's a great article](https://opensource.com/article/19/8/linux-chmod-command).

By default, the .ssh directory has 775 permissions whereas the authorized_keys file has 644 permissions. We will be changing these to 700 and 600 respectively.

```
flaskuser@Flask-Demo-Server:~$ sudo chmod 700 ~/.ssh/
flaskuser@Flask-Demo-Server:~$ sudo chmod 600 ~/.ssh/*
```

Note that using `sudo` will occasionally require us to enter the password that we set in step 2.

### Step 4 - Disallow root login
Now that *flaskuser* has been set up and primed for usage during our deployment, we do not want anyone to login to our server with **root** credentials. To prevent **root** logins, we will modify some settings in the sshd_config file using a file editor. We will be using nano throughout this deployment.

```
flaskuser@Flask-Demo-Server:/$ sudo nano /etc/ssh/sshd_config
```

In the editor, update the values of the `PermitRootLogin` and `PasswordAuthentication` keys from *yes* to *no*. Use `Ctrl + X` `Y` and `Enter` to save the file and close the editor.

Finally, we will restart the ssh daemon (sshd) to apply our changes.

```
flaskuser@Flask-Demo-Server:/$ sudo systemctl restart sshd
```

### Step 5 - Setting up a firewall
Ubuntu 18.04 servers can use an uncomplicated firewall (UFW) to permit connections only to specific services. Installing and setting up a UFW is fairly easy.

Install a UFW:
```
flaskuser@Flask-Demo-Server:/$ sudo apt install ufw
```

Setting default permissions for outgoing and incoming traffic:
```
flaskuser@Flask-Demo-Server:/$ sudo ufw default allow outgoing

flaskuser@Flask-Demo-Server:/$ sudo ufw default deny incoming
```

Allowing ssh connections to ensure that we can log in via `ssh` once the firewall is enabled:

```
flaskuser@Flask-Demo-Server:/$ sudo ufw allow ssh
```

Next, we will open port `5000` to test our Flask application after deployment

```
flaskuser@Flask-Demo-Server:/$ sudo ufw allow 5000
```

Finally, we will enable the firewall

```
flaskuser@Flask-Demo-Server:/$ sudo ufw enable

Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup
```

To check the status of the firewall and list of the allowed applications/ports, we can run `sudo ufw status`.

```
flaskuser@Flask-Demo-Server:/$ sudo ufw status

Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
5000                       ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
5000 (v6)                  ALLOW       Anywhere (v6)
```

That's it! Our set up is complete. In the [next](https://www.codedisciples.in/linux-vps-deployment2.html) post, we will deploy our Flask application.