Title: Iterools
Date: 2020-02-28 12:00
Category: Python
Tags: Python
Slug: itertools
Authors: Abhishek Pednekar
Summary: A look at the `itertools` module in Python 3
Cover: /static/images/black-gradient-article.jpg


In this post, we will dive into the `itertools` module in Python. The `itertools` module contains a truckload of functions to operate on Python iterators. Depending on the use case, these functions can make our code cleaner and more efficient.

The post assumes that the reader is familiar with the concept of iterators and iterables in Python. At the end of this post, the reader will be familiar with the usage of some common functions from the `itertools` module.

The `itertools` module is built into the Python standard library and therefore does not need to be installed separately. The `import itertools` statement will give us access to all the functions contained in the module. On that note, we will be skipping the  `import` statement in all but the first code snippet to avoid redundancy and keep the examples concise. 

Here is the list of functions that will be discussed in this post -

1. [count](#count)
2. [cycle](#cycle)
3. [zip_longest](#zip_longest)
4. [repeat](#repeat)
5. [starmap](#starmap)
6. [permutations](#permutations)
7. [combinations](#combinations)
8. [combinations_with_replacement](#combinations_with_replacement)
9. [product](#product)
10. [chain](#chain)
11. [islice](#islice)
12. [dropwhile](#dropwhile)
13. [takewhile](#takewhile)
14. [compress](#compress)
15. [accumulate](#accumulate)
16. [groupby](#groupby)
17. [tee](#tee)
<br />

## <a name="count"></a>`count`
The `itertools.count()` function returns an iterator that can be used as a counter. It takes optional `start` and `step` arguments.

`counter = itertools.count()` returns an iterator called `counter`. Looping over this `counter` will result in an infinite loop. However, we can use the `next()` method to iterate over the values of our counter.

```
>>> import itertools
>>> counter = itertools.count()
>>> print(next(counter))
0
>>> print(next(counter))
1
>>> print(next(counter))
2
>>> print(next(counter))
3
```

Note that the counter starts from `0` by default. To start it from something other than `0`, we can specify a value for the `start` keyword argument.

```
>>> counter = itertools.count(start=8)
>>> print(next(counter))
8
>>> print(next(counter))
9
>>> print(next(counter))
10
```

To increment in steps greater than or less than `1`, we can pass the `step` keyword argument.

```
>>> counter = itertools.count(start=7, step=-2)
>>> print(next(counter))
7
>>> print(next(counter))
5
>>> print(next(counter))
3
```

## <a name="cycle"></a>`cycle`
The `itertools.cycle()` function can be used to iterate continuously over a collection. For instance, if we use `cycle()` to iterate over a list containing two values, the function will **not** terminate the iteration once we have reached the end of the list. It will instead go back to the start of the list and resume a new round of iteration. 

```
>>> frameworks = ["flask", "django"]
>>> result = itertools.cycle(frameworks)
>>> print(next(result))
flask
>>> print(next(result))
django
>>> print(next(result))
flask
>>> print(next(result))
django
>>> print(next(result))
flask
>>> print(next(result))
django
```

## <a name="zip_longest"></a>`zip_longest`
Before we look at the `itertools.zip_longest()` function, let's quickly go over Python's `zip()` function. Let's say we have two lists of varying lengths. The `zip()` function will let us combine the two lists by grouping elements based on their positions. In other words, element 0 of the first list will be grouped with element 0 of the second list and so on. The key point in the below example is that the `zip()` function grouped the elements based on the smaller `alphabets` list. Once we reached the end of the `alphabets` list, `zip()` did not attempt to group the last element of the `numbers` list. Our result, therefore, does not include the value `4` from `numbers`.

```
>>> numbers = [1, 2, 3, 4]
>>> alphabets = ["A", "B", "C"]

>>> result = zip(numbers, alphabets)

>>> list(result)
[(1, 'A'), (2, 'B'), (3, 'C')]
```

`itertools.zip_longest()` reverses this behavior. Instead of grouping based on the smaller list, the function uses the larger list. Note that in this case, `4` is grouped with `None` as `alphabets` does not contain any element at its third index.

```
>>> result = itertools.zip_longest(numbers, alphabets)
>>> list(result)
[(1, 'A'), (2, 'B'), (3, 'C'), (4, None)]
```

## <a name="repeat"></a>`repeat`
The `itertools.repeat()` function takes an input and repeats it indefinately.

```
>>> result = itertools.repeat(5)

>>> print(next(result))
5
>>> print(next(result))
5
>>> print(next(result))
5
```

One example is to use `repeat()` with Python's `map()` function. In the example below, we are computing the squares of numbers in a list using the `pow()` function. Here, `map()` takes the value of each element in the first iterable (`[0, 1, 2, 3, 4]`) and applies the `pow()` function by raising each element to the power of `2` as specified in the `repeat()` function.

```
>>> squares = map(pow, range(5), itertools.repeat(2))
>>> list(squares)
[0, 1, 4, 9, 16]
```

## <a name="starmap"></a>`starmap`
The `itertools.starmap()` function accepts a function and computes it using the arguments specified in the iterable. For instance the previous example can be re-written using `starmap()` as follows. Here, the iterable is a list of tuples. `starmap()` takes the `pow()` function as input and raises the first element of the tuple to the power of the second element.

```
>>> squares = itertools.starmap(pow, [(0, 2,), (1, 2,), (2, 2,), (3, 2,), (4, 2,)])
>>> list(squares)
[0, 1, 4, 9, 16]
```

Below is a similar example which multiples the elements of each tuple.

```
>>> import operator
>>> product = itertools.starmap(operator.mul, [(1, 2, ), (4, 5, ), (7, 8, )])
>>> list(product)
[2, 20, 56]
```

## <a name="permutations"></a>`permutations`
The `itertools.permutations()` function takes an iterable and a length value as input and returns tuples of the specified length using the elements of the iterable.

For instance passing a string `"AB"` to the `permutations()` function will return the permutations `("A", "B")` and `("B", "A")`. Note that the function does not allow repeated values in the result. Hence we do not see `("A", "A")` and `("B", "B")`. 

```
>>> perm = itertools.permutations("AB", 2)
>>> list(perm)
[('A', 'B'), ('B', 'A')]
```

The length of each resulting permutation will need to be specified by passing an integer length as an argument.

```
>>> letters = ["A", "B", "C"]
>>> letter_perm = itertools.permutations(letters, 3)
>>> list(letter_perm)
[('A', 'B', 'C'), ('A', 'C', 'B'), ('B', 'A', 'C'), ('B', 'C', 'A'), ('C', 'A', 'B'), ('C', 'B', 'A')]
```

## <a name="combinations"></a>`combinations`
The `itertools.combinations()` function is similar to `permutations()`. However, there will be no repeat values in the result.

So, passing the string `"AB"` to the `combinations()` function will only result in `("A", "B")` as it considers both `("A", "B")` and `("B", "A")` to be the same. Also, note that `combinations()` does not allow repeated values in the result. Hence we do not see `("A", "A")` and `("B", "B")` here either. 
 
```
>>> combination = itertools.combinations("AB", 2)
>>> list(combination)
[('A', 'B')]
```

Like `permutations()`, we will need to specify a length as an argument.

```
>>> letters = ["A", "B", "C"]
>>> letter_combination = itertools.combinations(letters, 3)
>>> list(letter_combination)
[('A', 'B', 'C')]
```

## <a name="combinations_with_replacement"></a>`combinations_with_replacement`
The `itertools.combinations_with_replacement()` function allows repeated values in the result.

```
>>> letter_combinations = itertools.combinations_with_replacement("AB", 2)
>>> list(letter_combinations)
[('A', 'A'), ('A', 'B'), ('B', 'B')]
```

## <a name="product"></a>`product`
The `itertools.product()` function returns a Cartesian Product of the input iterables.

```
>>> product = itertools.product("ABC", "xy")
>>> list(product)
[('A', 'x'), ('A', 'y'), ('B', 'x'), ('B', 'y'), ('C', 'x'), ('C', 'y')]
```

The function also takes an optional `repeat` keyword argument which specifies the length of each resulting tuple.

```
>>> product = itertools.product("AB", repeat=2)
>>> list(product)
[('A', 'A'), ('A', 'B'), ('B', 'A'), ('B', 'B')]
```

## <a name="chain"></a>`chain`
The `itertools.chain()` function is used to chain iterables together and iterate over them simultaneously.

```
>>> countries = ["India", "Italy", "Ireland"]
>>> more_countries = ["United States", "United Kingdom", "Uruguay"]

>>> countries_list = itertools.chain(countries, more_countries)

>>> list(countries_list)
['India', 'Italy', 'Ireland', 'United States', 'United Kingdom', 'Uruguay']
```

## <a name="islice"></a>`islice`
The `itertools.islice()` function is used to slice an iterable and return only the selected values. `islice()` takes optional `start`, `stop` and `step` arguments.

In the below example, we are slicing the iterable defined by the `range(10)` function to return only the first 5 elements.
```
>>> sliced_results = itertools.islice(range(10), 5)
>>> list(sliced_results)
[0, 1, 2, 3, 4]
```

We can also pass a starting value to the function as indicated below.

```
>>> sliced_results = itertools.islice(range(10), 1, 5)
>>> list(sliced_results)
[1, 2, 3, 4]


# Incrementing in steps

>>> sliced_results = itertools.islice(range(10), 1, 5, 2)
>>> list(sliced_results)
[1, 3]
```

Note that `islice()` does not support negative values for `start`, `stop` and `step`.

## <a name="dropwhile"></a>`dropwhile`
The `itertools.dropwhile()` function will drop values from an iterable as long as a pre-defined condition is met. Once the condition fails, it returns **all** the remaining elements of the iterable.

In the following example, `dropwhile()` will **drop** elements from the iterable as long as the `x < 2` condition is met. As a result, the first three elements of the list are dropped. Once the condition fails on the fourth element (`2`), all the elements starting from the fourth element are returned irrespective of whether they meet the condition or not.

```
>>> results = itertools.dropwhile(lambda x: x < 2, [0, 1, 1.5, 2, 1, 0, 5])
>>> list(results)
[2, 1, 0, 5]
```

## <a name="takewhile"></a>`takewhile`
The `itertools.takewhile()` function will **return** elements from an iterable as long as they satisfy a pre-defined condition. Once the condition fails, all remaining elements are dropped.

In the below case, `takewhile()` will return elements from the list as long as the `x < 2` condition is met. Once the condition fails on the fourth element, all elements starting from the fourth element are dropped irrespective of whether they meet the condition or not.

```
>>> results = itertools.takewhile(lambda x: x < 2, [0, 1, 1.5, 2, 1, 0, 5])
>>> list(results)
[0, 1, 1.5]
```

## <a name="compress"></a>`compress`
The `itertools.compress()` function takes two arguments - `data` and `selectors`. The function returns those elements from `data` that have a corresponding elements in `selectors` that evaluate to `True`.

```
>>> filtered_results = itertools.compress("ABCD", [1, 1, 0, 0])
>>> list(filtered_results)
['A', 'B']

>>> filtered_results = itertools.compress("ABCD", [True, True, False, False])
>>> list(filtered_results)
['A', 'B']
```

## <a name="accumulate"></a>`accumulate`
The `itertools.accumulate()` function returns accumulated results. These could be accumulated sums (default behaviour) or accumulated results of other operations. The function takes optional `func` and `initial` arguments. If we are trying to generate accumulated results of operations other than addition, then we will need to specify a value for the `func` argument.

In the example below, we are adding numbers from 1 through 10 specified in the list input. `accumulate()` returns a running total.

```
>>> running_sum = itertools.accumulate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
>>> list(running_sum)
[1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
```

If we would instead like to find the running product, we can pass `operator.mul` as the value of the `func` argument.

```
>>> import operator
>>> running_product = itertools.accumulate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], operator.mul)
>>> list(running_product)
[1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
```

## <a name="groupby"></a>`groupby`
The `itertools.groupby()` function groups values based on a key. The function returns tuples of two elements.

1. The first element will be the `key`
2. The second will be an iterator that consists of all the items grouped by the `key`

To explain this clearly, we will use a list of dictionaries called `teams` containing the names of teams and countries that they are from. We will then use `groupby()` to group teams based on countries. Note that `groupby()` requires the list to be sorted. We, therefore, have the English teams listed first followed by the Spanish teams.

```
teams = [
    {
        "team": "Manchester United",
        "country": "England"
    },
    {
        "team": "York",
        "country": "England"
    },
    {
        "team": "Alaves",
        "country": "Spain"
    },
    {
        "team": "Racing Santander",
        "country": "Spain"
    }
]
```

Next, we will write a custom function that accepts our list as a parameter and returns the value of `country` which will be our `key` value.

```
def get_country(team):
	return team["country"]
```

Finally, we will use `groupby()` on our list and pass our custom function as the key. By looping over the resulting iterator, we see that the results are tuples containing the `key` (`country`) and an iterator.

```
>>> results = itertools.groupby(teams, get_country)
>>> for result in results:
	print(result)

	
('England', <itertools._grouper object at 0x032B0F30>)
('Spain', <itertools._grouper object at 0x00A49D30>)
```

We can loop over the resulting iterator using a nested `for - in` loop to return the items contained within it.

```
>>> for key, group in results:
	print(key)
	for team in group:
		print(team)
	print()

	
England
{'team': 'Manchester United', 'country': 'England'}
{'team': 'York', 'country': 'England'}

Spain
{'team': 'Alaves', 'country': 'Spain'}
{'team': 'Racing Santander', 'country': 'Spain'}
```

## <a name="tee"></a>`tee`
The `itertools.tee()` function is used to replicate iterators. In other words, create copies of an existing iterator. The key thing to note is that once we create a copy, we should no longer use the original iterator as it could result in the iterable getting advanced without the copies getting notified.

```
>>> results = itertools.groupby(teams, get_country)
>>> copy_of_results = itertools.tee(results)
```