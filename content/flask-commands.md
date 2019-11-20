Title: Custom Commands with Flask
Date: 2019-11-07 07:00
Category: Flask
Tags: Flask, Python
Slug: flask-commands
Authors: Abhishek Pednekar
Summary: Writing custom commands in Flask using the `click` library
Cover: /static/images/black-gradient-article.jpg

In this post, we will explore creating custom commands in Flask using the [Click](https://click.palletsprojects.com/en/7.x/) 
library. Click is one of the dependencies that is installed along with Flask. 

Whenever we run `pip install flask`, the `flask` command is also installed. `flask --help` lists all the options that can 
be run along with the `flask` command. For example, `flask run`, `flask shell` etc.

In the subsequent sections, we will create custom `flask` commands, starting with a simple example and then moving onto 
a more practical scenario.

## Custom Command - Example 1
In our first example, we will create a command that simply prints a message to the console. As always, we will create a 
virtual environment using `python -m venv venv`. After activating the environment - `source venv/Scripts/activate`, we will 
install flask - `pip install flask`. Next, we will create a python file (say app.py) and add the following code. 

```
import click
from flask.cli import with_appcontext
from flask import Flask

app = Flask(__name__)

@click.command(name="print_text")
@with_appcontext
def print_text():
    print("Hello from flask!")

app.cli.add_command(print_text)
```

Let's look at each line of this code. First, we import the `click` library that will be used to create our custom command. Next, we import 
the `with_appcontext` method from the `flask.cli` module. This is needed since we are using click's `command()` decorator. The execution of the 
`@click.command()` decorator requires the application context to be pushed so that our command has access to our application instance. To achieve 
this, `with_appcontext` will be used as a decorator for the `print_text()` function. In addition to these, we also import the `Flask` class to create 
our application instance - `app`.

The `command` decorator contains a parameter called `name`, using which we specify the name of the custom command - *print_text*. 
Next, we define our `print_text()` function. Note that the name of the function need not match the name of the command. 
The function contains the code we would like to execute whenever we run our command. In this case, we simply print a string 
*Hello from flask!* on the console.

Next, we will pass the `print_text` function to the `add_command` method to create our custom command. To run this command, we use the syntax `flask <custom_command_name` which in our case is 
`flask print_text`. Ensure that the virtual environment is activated before running the command.

<br/>
![flask-command]({static}/images/index14/flask-command.jpg)

## Custom Command - Example 2

In this example, we will create two custom commands. The first command will create a table called user in a SQLite database and the 
second will add records to the table.

To do this, we will first install the flask-sqlalchemy library - `pip install flask-sqlalchemy` in our virtual environment. In our code, we will add 
a class *User* that defines our database model. Finally, we will define a function called `create_tables()` to create our SQLite database called *data.db* and create the *user* table in the database using 
SQL Alchemy's `db.create_all()` command. The function will use the same decorators as the previous example. However, in this case, we will be passing the name of the command 
as `create_tables` to the `command()` decorator. Finally we will pass the `create_tables` function to the `add_command()` method to create our command.

```
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    role = db.Column(db.String(25))


@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()

app.cli.add_command(create_tables)
```

Now running `flask create_tables` in the terminal will create a database called *data.db* in the project folder. The database should contain a 
table called *user*

<br/>
![flask-command]({static}/images/index14/flask-command.jpg)

<br/>
![table]({static}/images/index14/table.jpg)

Next, we will add a couple of records to the table. The code will be similar to what we have seen thus far. However, our table has 
two columns - *name* and *role*. We will need to specify values for these columns by passing them as arguments to the custom command. 
To achieve this, we will need to specify these arguments using the `@click.argument()` decorator. One decorator will need to be 
specified per argument. We will also need to pass the *name* and *role* as parameters to the `create_user()` function. 
 
```
@click.command(name="create_user")
@click.argument("name")
@click.argument("role")
@with_appcontext
def create_user(name, role):
    u = User(name=name, role=role)
    db.session.add(u)
    db.session.commit()

app.cli.add_command(create_user)
```

To create our users using the custom command, we will run `flask create_user <name> <role>` in a terminal window.

<br/>
![flask-command2]({static}/images/index14/flask-command2.jpg)

<br/>
![table2]({static}/images/index14/table2.jpg)