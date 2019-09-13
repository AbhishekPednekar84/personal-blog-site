Title: Namedtuples
Date: 2019-09-13 23:00
Category: Python
Tags: Python
Slug: named-tuples
Authors: Abhishek Pednekar
Summary: An overview of the namedtuple container type in Python
Cover: /static/images/black-gradient-article.jpg

In this post, we will take a look at Python's **namedtuple** container type. Firstly, namedtuples are immutable containers just like regular tuples. However, unlike regular tuples, which can be accessed only through indices, namedtuples can be accessed via identifiers/keys as well as index values. To use namedtuples, we will need to import the **collections** module.

Below, we are defining a namedtuple called *Movie* with four fields in a list - *name*, *genre*, *year* and *director*. Notice that we are passing *Movie* as the first argument to the namedtuple method. This parameter is called the *typename* and is essentially the name of the class being created by calling the namedtuple method.

```
>>> from collections import namedtuple
>>> Movie = namedtuple("Movie", ["name", "genre", "year", "director"])
```

Below, is an alternate way to define namedtuples. Here, rather than passing the field names in a list, we are passing them as a string.

```
>>> from collections import namedtuple
>>> Movie = namedtuple("Movie", "name genre year director")
```

Using either of the above definitions, we can now create new Movie objects. This is akin to creating a Movie class and providing it with a constructor that accepts values for the four fields.

```
>>> movie_1 = Movie("The Dark Knight", "Action", 2008, "Christopher Nolan")
>>> movie_2 = Movie("It", "Horror", 2017, "Andy Muschietti")
```

### Accessing namedtuple values
Accessing values using the field identifiers. This is one of the key advantages of namedtuples as it makes the code more readable.

```
>>> movie_1.name
'The Dark Knight'

>>> movie_2.director
'Andy Muschietti'
```

Accessing values using indices.
```
>>> movie_1[3]
'Christopher Nolan'

>>> movie_2[0]
'It'
```

Accessing values using `getattr()`.
```
>>> getattr(movie_1, "year")
2008

>>> getattr(movie_2, "genre")
'Horror'
```

### Built-in methods

### `_make()`
The `_make()` method returns a namedtuple from an iterable. Let's say we have a list containing the attribute values of our Movie instance. By using `_make()`, we can convert the list to a namedtuple.

```
>>> movie_lst = ["Taxi Driver", "Thriller", 1976, "Martin Scorsese"]
>>> Movie._make(movie_lst)

Movie(name='Taxi Driver', genre='Thriller', year=1976, director='Martin Scorsese')
```

### `_asdict()`
The `_asdict()` method returns the contents of the nametuple as an **OrderedDict**.

```
>>> movie_1._asdict()

OrderedDict([('name', 'The Dark Knight'), ('genre', 'Action'), ('year', 2008), 
('director', 'Christopher Nolan')])
```

### The ` ** ` (dictionary unpacking) operator
The ` ** ` operator can be used to generate a namedtuple from a dictionary. ` ** ` unpacks the key-value pairs of a dictionary.

```
>>> movie_dict = {"name": "March of the Penguins", 
                  "genre": "Documentary", 
                  "year": 2005, 
                  "director": "Luc Jacqet"}

>>> Movie(**movie_dict)

Movie(name='March of the Penguins', genre='Documentary', year=2005, director='Luc Jacqet')
```

### `_fields`
The `_fields` property is used to return all the field names of a namedtuple.

```
>>> Movie._fields

('name', 'genre', 'year', 'director')
```

The `_fields` property is particularly useful while creating namedtuples that inherit field names from a parent namedtuple. In the example below, we are creating a new namedtuple called *NewMovie* by inheriting the fields from the original *Movie* namedtuple using the `_fields` property. At the same time, we are adding a new field called *music* to the NewMovie namedtuple.

```
>>> Movie = namedtuple("Movie", "name genre year director")

>>> NewMovie = namedtuple("NewMovie", Movie._fields + ("music",))

>>> movie_1 = NewMovie("The Dark Knight", "Action", 2008, "Christopher Nolan", "Hans Zimmer")

>>> movie_1
NewMovie(name='The Dark Knight', genre='Action', year=2008, director='Christopher Nolan', music='Hans Zimmer')
```

###  `_replace()`
The `_replace()` method is used to selectively replace the value of specific fields.

```
>>> movie_1._replace(director="C. Nolan")

NewMovie(name='The Dark Knight', genre='Action', year=2008, director='C. Nolan', music='Hans Zimmer')
```