Title: Running Celery on Windows 10
Date: 2019-10-22 22:00
Category: Python
Tags: Celery
Slug: celery-windows
Authors: Abhishek Pednekar
Summary: Running Celery (with Redis) on Windows 10 using Windows Subsystem for Linux

Celery is an asynchronous task queue that is fairly easy to integrate with a Python application. It requires a messaging queue (also known as a broker) to send and receive messages. Popular brokers are Redis and RabbitMQ.

In this post, we will see how to install and run Celery using Windows Subsystem for Linux (WSL) on Windows 10. **Redis** will be our broker in the example.  We will also be using the **Remote-WSL** extension in VS Code to develop our Python application in a Linux environment. Finally, we will store the results of the tasks executed by Celery in a **SQLite** database.

This post assumes that the reader already has WSL setup and has installed Python and pip on WSL. If not, one can refer to the below resources before proceeding further -

1. [Setting up WSL](https://www.youtube.com/watch?v=xzgwDbe7foQ&t=533s)
2. [Python setup on WSL](https://medium.com/@rhdzmota/python-development-on-the-windows-subsystem-for-linux-wsl-17a0fa1839d)


Now that we have Python installed with WSL, we will create a virtual environment and install the required dependencies. For this demo, we are using the [cmder](https://cmder.net/) console application. The same commands can be run in Ubuntu or other Linux distros. In the current example, we will open a `WSL` window in **cmder** to run the commands. 

1. Create the virtual environment in the project folder - `python3 -m venv venv`
2. Activate the virtual environment - `source venv/bin/activate`
3. Install the celery - redis and sqlalchemy libraries - `pip3 install celery[redis] sqlalchemy` 
4. Create the requirements file - `pip3 freeze > requirements.txt`
5. Open the project folder in VS Code via explorer or by running `code .` in the console

As mentioned earlier, we will be using the [Remote-WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) extension to run our code in a Linux based environment. This plugin can be installed from the VS Code marketplace.

<br/>
![Remote-WSL]({static}/images/index11/remote-wsl.jpg)

Once installed, we will have an option to reopen our (Windows) project folder in WSL.

<br/>
![Windows-WSL]({static}/images/index11/windows-wsl.jpg)

The final thing we need to do before writing our code is to install a Redis server instance locally. Running the following commands in `WSL` will install a `Redis server` on your computer.

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install redis-server
```

Once the installation is complete, we will restart the server using `sudo service redis-server restart` to make sure that it is running.

Our simple code consists of a function that multiplies two numbers. However, rather than printing the result in a REPL, we will let `Celery` execute a task and store the result in a `SQLite` database.

```
# module name - celery_demo.py

from celery import Celery

app = Celery("celery_demo", 
             broker="redis://localhost:6379",
             backend="db+sqlite:///results.db")

@app.task
def multiply(num1, num2):
    return num1 * num2
```

Let's go over this line by line -

1. First, we import the `Celery` class from the `celery` module
2. Next, we create an instance of the class (called app) and pass our module name which is `celery_demo` in our case, the url of our redis server (running on localhost on the default port 6379) and lastly the link to our `SQLite` database which will store the task results
3. Finally, we have our function which multiplies two numbers that are passed to it as parameters and returns their product. Note that the function is decorated with `@app.task` which will enable us to execute this function/task using our Celery worker

Next, we will fire up our `Celery` worker process.We need to make sure that we are in the virtual environment when executing the below command. The command will be run in a `WSL` window. Note that we are passing our module name, the `worker` argument and setting the logging level with the `--loglevel` argument which will enable us to see results in our console.

`celery -A celery_demo worker --loglevel=info`

<br/>
![Celery]({static}/images/index11/celery.jpg)

Now, we will call our task in a Python REPL using the `delay()` method. Calling the task will return an *AsyncResult* instance, each having a unique guid. Again, we will be using `WSL` to run the REPL.

<br/>
![Calling-Task]({static}/images/index11/calling-task.jpg)

If the task is called successfully, we can see the result of the task as executed by our `Celery` worker.

<br/>
![Celery-Result]({static}/images/index11/celery-result.jpg)

At this point, our `SQLite` database is created.  The `celery-taskmeta` table will store the results of all our tasks. The tasks can be identified based on the guid of the async result instance. The results will be stored in a binary (BLOB) format. 

<br/>
![SQLite-Results]({static}/images/index11/sqlite-results.jpg)

Here is a readable version of our result BLOB.

```	
{
  "data": [
    128,
    4,
    149,
    3,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    75,
    10,
    46
  ],
  "type": "Buffer"
}
```