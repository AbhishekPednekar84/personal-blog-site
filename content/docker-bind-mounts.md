Title: Bind Mounting with Docker Toolbox on Windows
Date: 2019-09-18 14:00
Category: Docker
Tags: Docker
Slug: docker-bind-mounts
Authors: Abhishek Pednekar
Summary: Creating containers with bind mounting using Docker Toolbox on Windows
Cover: /static/images/black-gradient-article.jpg

If you have racked your brains trying to get Docker bind mounting to work on Windows, you certainly are not alone. Documentation for Docker on Windows is not exactly verbose, especially if you are using the Docker Toolbox. In this post, we will look at binding a local Windows folder to a directory in a Docker Container using Docker Toolbox. In the example below, we will create an *nginx* container with a bind to a local folder in "C:\Users". We will test the bind by copying over files from the local folder to the container.

An important thing to note on Windows is to use `//<drive letter>/` to reference our local drive in the `docker container run` command. For instance, to reference "C:\Users", we will use "//c/users".  

Next, we will add a shared folder on our virtual machine (VM). In this example, **Oracle VirtualBox** provides the VM to run Docker Toolbox. We can add a shared folder in the *Settings* of our VM.  

<br/>
![vm1]({static}/images/index8/vm1.jpg)  

<br/>
To add a shared folder, we will select the *Shared Folders* option. We will then need to specify the desired folder on our computer and give it an appropriate name. This name will be used in the `docker container run` command. So in the example below, by including "//c/Docker" in our command, we are simply referring to "C:\users\abhi_\Docker". Be sure to select the *Auto Mount* and *Make Permanent* options. For these settings to take effect, the VM will need to be restarted. To reboot, right-click on the VM and select *Reset*.

<br/>
![vm2]({static}/images/index8/vm2.jpg)  

<br/>
The local "Docker" folder has two files. These will get copied over to the directory (in our container) which will be bound to the local folder using the `-v` or `--volume` options.  

<br/>
![vm3]({static}/images/index8/vm3.jpg)  

<br/>
Finally, we will create our nginx container. The `-v //c/Docker:/usr/share/nginx/html` in the command, binds "C:\users\abhi_\Docker" to "/usr/share/nginx/html" on the container.  

`docker container run -d --name nginx -p 80:80 -v //c/Docker:/usr/share/nginx/html nginx`  

To verify whether the bind mounting worked, we will run *bash* on the container and look for the files in "/usr/share/nginx/html".  

<br/>
![vm4]({static}/images/index8/vm4.jpg)



