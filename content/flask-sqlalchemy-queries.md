Title: Queries using Flask SQLAlchemy
Date: 2019-10-31 17:00
Category: Flask
Tags: Flask, Python
Slug: flask-sqlalchemy-queries
Authors: Abhishek Pednekar
Summary: Writing queries using the flask-sqlalchemy library
Cover: /static/images/black-gradient-article.jpg

In this post, we will go over writing database queries using the **Flask SQLAlchemy** library. The post assumes that the
 reader has some basic knowledge of flask and SQL in general.

First, we will create a simple flask application (app.py) with a SQLite backend database containing a couple of models. 
Ideally, database models should be created as a separate module or package within the project for better maintainability. 
However, for this demo application we will be writing all our python code in the same file.

As always, we will first create our virtual environment using the command `python -m venv venv`. Once the virtual 
environment is activated (`venv\Scripts\activate.bat` on Windows and `source venv/bin/activate` on Linux / OSx), we will 
install the *flask* and *flask-sqlalchemy* packages - `pip install flask flask-sqlalchemy`.

```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Folder(db.Model):

    __tablename__ = "folder"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    files = db.relationship("File", backref="files")

    def __repr__(self):
        return f"Folder({self.name})"


class File(db.Model):

    __tablename__ = "file"

    id = db.Column(db.Integer, primary_key=True)
    folder_id = db.Column(db.Integer, db.ForeignKey("folder.id"))
    name = db.Column(db.String(50))
    size = db.Column(db.Integer)

    def __repr__(self):
        return f"File({self.folder_id}, {self.name}, {self.size})"
```  

For this example, we will be using two database models / tables - **folder** and **file** that have a one to many relationship 
(one folder can contain many files). This relationship is defined by the `db.relationship` construct. 
The `__repr__` method is optional. However, it will give us a nice readable output. To create our database, 
we will open a python REPL in the activated virtual environment and run the below commands. 

```
>>> from app import db, Folder, File
>>> db.create_all()
```

At this point, we will see a SQLite database called *data.db* in our project folder. 
 
## INSERT Queries

To create / insert new records, we will first create instances (with data) of our models. Next, we will use the 
`db.session.add()` command to add objects to the session.

To add multiple objects at once, we can use `db.session.add_all()` and pass a list containing all our objects as 
shown below. Finally, we will commit our transaction using `db.session.commit()`.

```
>>> fld1 = Folder(name="images")
>>> fld2 = Folder(name="flask-project")
>>> fld3 = Folder(name="bills")
>>> db.session.add_all([fld1, fld2, fld3])
>>> db.session.commit()


>>> # Add records to the file table

>>> fl1 = File(folder_id=1, name="image1.jpg", size=1000)
>>> fl2 = File(folder_id=1, name="image2.jpg", size=2000)
>>> fl3 = File(folder_id=1, name="image3.jpg", size=1000)
>>> fl4 = File(folder_id=2, name="flask1.py", size=1000)
>>> fl5 = File(folder_id=2, name="flask2.py", size=1000)
>>> db.session.add_all([fl1, fl2, fl3, fl4, fl5])
>>> db.session.commit()
```

<hr>

## SELECT Queries

Querying all the records from a table - `all()`

```
>>> Folder.query.all()

[Folder(images), Folder(flask-project), Folder(bills)]
```

Querying specific records from a table - `filter_by()`

```
>>> Folder.query.filter_by(name="flask-project").all()

[Folder(flask-project)]

>>> Folder.query.filter_by(name="flask-project").first()

Folder(flask-project)

```

Querying records by id - `get()`

```
>>> Folder.query.get(1)

Folder(images)

>>> File.query.get(3)

File(1, image3.jpg, 1000)

```

While viewing the output delivered by the `__repr__` method might be helpful in our present case, practical scenarios 
require us to get the actual data as stored in the table. This can be done as follows.

```
>>> result = Folder.query.first()
>>> result.name

'images'

>>> result = File.query.filter_by(name="image1.jpg").first()
>>> result.size

1000
```

<hr>

## UPDATE Queries

To update data, we will first need to fetch the record that requires the update. Next. we can simply assign the new 
value to the attribute that needs the update and commit the transaction.

```
>>> # Update a specific record
>>> result = File.query
             .filter_by(name="image1.jpg")
             .first()
             
>>> result.size = 5000

>>> db.session.commit()

>>> # After update
>>> File.query.filter_by(name="image1.jpg").first()
File(1, image1.jpg, 5000)

```

To update all the records in a table, we will need to iterate over the results returned by `all()` and then apply the 
update. To persist the changes (intentionally skipped), we will need to run `db.session.commit()`

```
>>> # Updating all the records
>>> results = File.query.all()
>>> for result in results:
...     result.size = 4000
 
>>> File.query.all()

[File(1, image1.jpg, 4000), File(1, image2.jpg, 4000), 
File(1, image3.jpg, 4000), File(2, flask1.py, 4000), 
File(2, flask2.py, 4000)]

```

<hr>

## DELETE Queries

To delete a record, we will append `.delete()` to our select query. To persist the deletion, we will need to commit the transaction

```
>>> File.query
    .filter_by(name="image1.jpg")
    .delete()
1

>>> db.session.commit()

```

To delete all the records in a table, we will use the `<model_name>.query.delete()` syntax.

```
>>> File.query.delete()
4

```

<hr>

## ROLLBACK

To rollback an update, delete or insert that has <u>not</u> been committed, use `db.session.rollback()`

<hr>

## INNER JOIN

To perform an inner join between two tables, we will use the `.join()` method and specify the join attributes.
The result is a list of tuples that can be iterated over.

```
>>> db.session.query(Folder, File)
    .join(File, Folder.id == File.folder_id)
    .all()

[(Folder(images), File(1, image1.jpg, 5000)), (Folder(images), File(1, image2.jpg, 2000)), 
(Folder(images), File(1, image3.jpg, 1000)), (Folder(flask-project), File(2, flask1.py, 1000)), 
(Folder(flask-project), File(2, flask2.py, 1000))]

```

<hr>

## OUTER JOIN

The syntax for an outer join is similar to an inner join. However we will be using the `.outerjoin()` method.

Notice that in the result of the below query, the last tuple returns a *None* for the folder named *bills* as 
there are no corresponding records in the *file* table. 

```
>>> db.session.query(Folder, File)
    .outerjoin(File, Folder.id == File.folder_id)
    .all()

[(Folder(images), File(1, image1.jpg, 5000)), (Folder(images), File(1, image2.jpg, 2000)), 
(Folder(images), File(1, image3.jpg, 1000)),  (Folder(flask-project), File(2, flask1.py, 1000)), 
(Folder(flask-project), File(2, flask2.py, 1000)), 
(Folder(bills), None)]
```

Again, we can iterate over the results to pull specific attribute values. The `if` statement in the example is 
to handle the *None* condition described above.

```
>>> for result in results:
...     if result[1]:
...         print(f"The folder {result[0].name} contains the file {result[1].name} with size {result[1].size} KB")

The folder images contains the file image1.jpg with size 5000 KB
The folder images contains the file image2.jpg with size 2000 KB
The folder images contains the file image3.jpg with size 1000 KB
The folder flask-project contains the file flask1.py with size 1000 KB
The folder flask-project contains the file flask2.py with size 1000 KB
``` 

<hr>

## AGGREGATE FUNCTIONS & GROUP BY

To get the **count** of files in each folder, we will use the *count()* method along with a *group_by()*

Here, we are selecting the folder name and the file count (`db.func.count()`) using the same outer join as the previous
 examples. However, we are grouping the results by the file name.

```
 >>> db.session.query(Folder.name, db.func.count(File.folder_id))
     .outerjoin(File, Folder.id == File.folder_id)
     .group_by(Folder.name)
     .all()   
     .all()   
 
 [('bills', 0), ('flask-project', 2), ('images', 3)]
```
 
 To get the **sum** of the file sizes in each folder, we can use a similar query.
 
```
 >>> db.session.query(Folder.name, db.func.sum(File.size))
     .outerjoin(File, Folder.id == File.folder_id)
     .group_by(Folder.name).all()
     
[('bills', None), ('flask-project', 2000), ('images', 8000)]
```

<hr>

## ORDER BY

To order the results based on a specific attribute, we will use the `order_by()` method. 

```
>>> db.session.query(File.name, File.size).order_by(File.name).all()

[('flask1.py', 1000), ('flask2.py', 1000), ('image1.jpg', 5000), ('image2.jpg', 2000), ('image3.jpg', 1000)]

```

We can order results by more than one attribute.

```
>>> db.session.query(File.name, File.size)
    .order_by(File.size, File.name)
    .all()

[('flask1.py', 1000), ('flask2.py', 1000), ('image3.jpg', 1000), 
('image2.jpg', 2000), ('image1.jpg', 5000)]

```

<hr>

## LIMIT

We can limit the amount of data returned by a query using the `limit()` method. The method takes an integer as an argument.

By specifying `limit(2)` in the below example, we are limiting the amount of data returned by the query. Instead of 
returning a list with five tuples, we get a list with only two tuples.

```
>>> db.session.query(File.name, File.size)
    .order_by(File.size, File.name)
    .limit(2)
    .all()

[('flask1.py', 1000), ('flask2.py', 1000)]

```

If we specify a limit higher than the total number of records that would otherwise be returned by the query 
(without using limit()), the query will return all the data.

```
>>> db.session.query(File.name, File.size)
    .order_by(File.size, File.name)
    .limit(200)
    .all()

[('flask1.py', 1000), ('flask2.py', 1000), ('image3.jpg', 1000), 
('image2.jpg', 2000), ('image1.jpg', 5000)]

```

<hr>

## OFFSET

We can bypass a subset of our query results using the `offset()` method. This method also takes an integer as a parameter.

Specifying an offset of 2, ignores the first two records (tuples in our case) and returns the rest.

```
>>> db.session.query(File.name, File.size)
    .order_by(File.size, File.name)
    .offset(2)
    .all()

[('image3.jpg', 1000), ('image2.jpg', 2000), ('image1.jpg', 5000)]

```

<hr>

## CONDITIONALS

To filter our results with **and** / **or** conditionals, we will use the `db.and_()` / `db.or_()` methods.
To use a **not** conditional, we can simply use **!=** in place of **==** 

```
>>> # Using OR
>>> File.query.filter(db.or_(File.name == "image1.jpg", File.name == "flask1.py"))
    .all()

[File(1, image1.jpg, 5000), File(2, flask1.py, 1000)]
```

```
>>> # Using AND and NOT
>>> File.query.filter(db.and_(File.name != "image1.jpg", File.name != "flask1.py"))
.all()

[File(1, image2.jpg, 2000), File(1, image3.jpg, 1000), File(2, flask2.py, 1000)]
```