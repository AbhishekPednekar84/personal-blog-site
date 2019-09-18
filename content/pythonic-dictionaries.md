Title: Pythonic Dictionaries
Date: 2019-09-01 12:00
Category: Python
Tags: Python
Slug: pythonic-dictionaries
Authors: Abhishek Pednekar
Summary: An overview of some dictionary methods
Cover: /static/images/black-gradient-article.jpg

Dictionaries are one of the most helpful data structures in Python. In this post, we'll look at some methods that make dictionary usage more pythonic.

## The `get()` method
A common way to check whether a key exists in a dictionary is to iterate over the dictionary using a loop. Another way would be to use, the *"`if` key `in` dict"* syntax. While these work, they do not keep in line with the *easier to ask for forgiveness than permission* (EAFP) coding style specified in the Python documentation.

Python dictionaries provide a `get()` method that allows a *default* parameter which can be used as a fall-back value in case the key does not exist. In the below example, we use the `get()` method to look for a key a dictionary. We also provide a default parameter of *Not found* that will be returned if the key does not exist. If the key is present, then the value associated with that key will be returned.

```
>>> alter_ego = {
        "Bruce Wayne": "Batman", 
        "Clark Kent": "Superman", 
        "Peter Parker": "Spiderman"
        }
                
>>> alter_ego.get("Bruce Wayne", "Not found")
'Batman'

>>> alter_ego.get("Tony Stark", "Not found")
'Not found' 
```

## The `setdefault()` method
The `setdefault()` method is used to set a value for a key that does <u>not</u> exist in a dictionary. If the key exists, then its value remains unchanged.

Here we see that by using the `setdefault()` method on the dictionary, we are able to add a new key-value pair that did not exist in the dictionary.

```
>>> alter_ego = {
        "Bruce Wayne": "Batman", 
        "Clark Kent": "Superman", 
        "Peter Parker": "Spiderman"
        }

>>> alter_ego.setdefault("Tony Stark", "Ironman")
'Ironman'

>>> alter_ego
{'Bruce Wayne': 'Batman', 'Clark Kent': 'Superman', 'Peter Parker': 'Spiderman', 'Tony Stark': 'Ironman'}
```

Conversely, if we try to set the value of an existing key, it remains unchanged.

```
>>> alter_ego.setdefault("Bruce Wayne", "Robin")
'Batman'

>>> alter_ego
{'Bruce Wayne': 'Batman', 'Clark Kent': 'Superman', 'Peter Parker': 'Spiderman', 'Tony Stark': 'Ironman'}
```

## Sorting Dictionaries
Iterating over dictionaries may or may not return a sorted order of key-value pairs. However, if for any reason, we required either keys or values of a dictionary in a sorted order, then using the `sorted()` method in conjunction with `items()`, will serve the purpose. 

```
>>> my_dict = {"A": 4, "D": 1, "B": 3, "C": 2}

>>> # Sorting based on keys
>>> sorted(my_dict.items())
[('A', 4), ('B', 3), ('C', 2), ('D', 1)]
```

The `sorted` method also provides a `reverse` parameter (that takes a boolean value) using which the keys or values can be sorted in reverse order.

```
>>> # Sorting the keys in reverse order
>>> sorted(my_dict.items(), reverse=True)
[('D', 1), ('C', 2), ('B', 3), ('A', 4)]
```

If we need to sort based on the values rather than the keys, we can use the `key` parameter of the `sorted()` method and set its value to the below lambda function.

```
>>> sorted(my_dict.items(), 
           key=lambda x: x[1],)
[('D', 1), ('C', 2), ('B', 3), ('A', 4)]

>>> # Sorting based on values
>>> sorted(my_dict.items(), 
           key=lambda x: x[1], 
           reverse=True,)
[('A', 4), ('B', 3), ('C', 2), ('D', 1)]
```

## Merging dictionaries
Sometimes, we may need a way to combine multiple dictionaries into one so that the resulting dictionary is a combination of the key-value pairs from all the source dictionaries. Python offers multiple ways to merge dictionaries into one. One of them is using the `update()` method.

In the below example, we are combining two dictionaries, *dict1* and *dict2* into a new dictionary *dict3*. Note that both the source dictionaries contain the key *B*. The way we call `update()` on the source dictionaries determines which value of *B* will be included in the new dictionary. Since the `update()` method is being run on *dict2* last, the resulting dictionary contains `"B": 3` rather than `"B": 2`. The `update()` method can be used to merge any number of dictionaries.

```
>>> dict1 = {"A": 1, "B": 2}
>>> dict2 = {"B": 3, "C": 4}

>>> dict3 = {}
>>> dict3.update(dict1)
>>> dict3.update(dict2)

>>> dict3
{'A': 1, 'B': 3, 'C': 4}
```

Another way to merge dictionaries is to use the ** operator for unpacking objects. Again in case of repeating keys in any of the source dictionaries, the order of unpacking will determine which value is chosen for that key. The below syntax is applicable starting with Python 3.5.

```
>>> dict1 = {"A": 1, "B": 2}
>>> dict2 = {"B": 3, "C": 4}
>>> dict3 = {"D": 5, "E": 6}

>>> dict4 = {**dict1, **dict2, **dict3}

>>> dict4
{'A': 1, 'B': 3, 'C': 4, 'D': 5, 'E': 6 }
```

## Emulate a switch statement with dictionaries
Unlike languages such as C# and Java, Python does not provide a `switch` statement out of the box. A `switch` statement is essentially a cleaner representation of an `if-elif-else` block containing a "fall-through" for each block with a `break` statement. We can however, use a Python dictionary combined with a `get()` (for the `default` case in a `switch` statement) to obtain a `switch` like representation.

```
>>> def f1_teams(random_team):
	    return {
        "Mercedes": ["Ham", "Bot"], 
        "Ferrari": ["Lec", "Vet"], 
        "McLaren": ["Sai", "Nor"], 
        "Alpha": ["Rai", "Gio"]
        }.get(random_team, "No drivers")

>>> f1_teams("Mercedes")
['Ham', 'Bot']

>>> f1_teams("Redbull")
'No drivers'
```

An `if-elif-else` version of this would be as follows.

```
>>> def f1_teams(team):
	if team == "Mercedes":
		return ["Ham", "Bot"]
	elif team == "Ferrari":
		return ["Lec", "Vet"]
	elif team == "McLaren":
		return ["Sai", "Nor"]
	elif team == "Alpha":
		return ["Rai", "Gio"]
	else:
		return "No drivers"
	
>>> f1_teams("Mercedes")
['Ham', 'Bot']

>>> f1_teams("Redbull")
'No drivers'
```