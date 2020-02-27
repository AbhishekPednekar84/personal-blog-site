Title: Iterools
Date: 2020-02-27 12:00
Category: Python
Tags: Python
Slug: itertools
Authors: Abhishek Pednekar
Summary: A look at the `itertools` module in Python 3
Cover: /static/images/black-gradient-article.jpg


In this post, we will dive into the `itertools` module in Python. The `itertools` module contains a truckload of functions to operate on Python iterators effeciently. Depending on the use case, these functions can make our code leaner and more effecient.

The post assumes that the reader is familiar with iterators and iterables in Python. For a quick refresher, [this is a great video turoria](https://www.youtube.com/watch?v=jTYiNjvnHZY). Please be aware that the post does not discuss all the functions in `itertools`. We will only look at a select subset which should be good enough to solve most common problems.

At the end of this post, the reader will be familiar with the usage of some common functions from the `itertools` module.

The `itertools` module is built into the Python standard library and therefore does not need to be installed separately. The `import itertools` statement will give us access to all the functions contained in the module. On that note, we will be skipping the  `import` statement in all but the first code snippet to avoid redundancy and keep the examples consice. 

## `count`
The `itertools.count()` function returns an iterator that can be used as a counter. It takes optional `start` and `step` arguments.

`counter = itertools.count()` returns an interator called `counter`. Looping over this `counter` will result in an infinate loop. However, we can use the `next` method to iterate over the values of our counter.

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

Note that the counter starts from `0` by default. To start it from something other than `0`, we can specify a value for the `start` argument.

```
>>> counter = itertools.count(start=8)
>>> print(next(counter))
8
>>> print(next(counter))
9
>>> print(next(counter))
10
```

To increment in steps greater than or less than `1`, we can pass the `step` argument.

```
>>> counter = itertools.count(start=7, step=-2)
>>> print(next(counter))
7
>>> print(next(counter))
5
>>> print(next(counter))
3
```

## `cycle`
The `itertools.cycle()` function can be used to iterate continuously over a collection. Fot instance, if we use `cycle` to iterate over a list containing two values, the function will **not** terminate the iteration once we have reached the end of the list. It will instead go back to the start of the list and resume a new round of iteration. 

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

## `zip_longest`
Before we look at the `itertools.zip_longest()` function, let's quickly go over Python's `zip()` function. Let's say we have two lists of varying lengths. The `zip()` function will let us combine the two lists by grouping elements based on their positions. In other words, element 0 of the first list will be grouped with element 0 of the second list and so on. The key point in the below example is that the `zip()` function grouped the elements based on the smaller `alphabets` list. Once we reached the end of the `alphabets` list, `zip()` did not attempt to group the last element of the `numbers` list. Our result therefore does not include `4` from `numbers`.

```
>>> numbers = [1, 2, 3, 4]
>>> alphabets = ["A", "B", "C"]

>>> result = zip(numbers, alphabets)

>>> list(result)
[(1, 'A'), (2, 'B'), (3, 'C')]
```

`itertools.zip_longest()` reverses this behavior. Instead of grouping based on the smaller list, the function uses the larger list. Note that in this case, `4` is grouped with `None` as `alphabets` does not contain any element at it's third index.

```
>>> result = itertools.zip_longest(numbers, alphabets)
>>> list(result)
[(1, 'A'), (2, 'B'), (3, 'C'), (4, None)]
```

## `repeat`
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

Another example is to use `repeat()` with Python's `map()` function. In the example below, we are computing the squares of numbers in a list using the `pow` function. Here, `map` takes the value of each element in the first iterable ([0, 1, 2, 3, 4]) and applies the `pow` function by raising each element to the power of `2` as specified in the `repeat()` function.

```
>>> squares = map(pow, range(5), itertools.repeat(2))
>>> list(squares)
[0, 1, 4, 9, 16]
```

## `starmap`
The `itertools.starmap()` function accepts a function and computes it using the arguments specified in the iterable. For instance the previous example can be re-written using `starmap()` as follows. Here our iterable is a list of tuples. Here, `starmap()` takes the `pow` function as input and raises the first element of the tuple to the power of the second element.

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

## `permutations`
The `itertools.permutations()` function takes an iterable and length as input and returns tuples of the specified length using the elements of the iterable.

For instance passing a string `"AB"` to the `permutations()` function will return the permutations `("A", "B")` and `("B", "A")`. Note that the function does not allow repeated values in the result. Hence we do not see `("A", "A")` and `("B", "B")`. 

```
>>> perm = itertools.permutations("AB", 2)
>>> list(perm)
[('A', 'B'), ('B', 'A')]
```

The length of each resulting permutation will need to be specified by passing an integer length as argument.

```
>>> letters = ["A", "B", "C"]
>>> letter_perm = itertools.permutations(letters, 3)
>>> list(letter_perm)
[('A', 'B', 'C'), ('A', 'C', 'B'), ('B', 'A', 'C'), ('B', 'C', 'A'), ('C', 'A', 'B'), ('C', 'B', 'A')]
```

## `combinations`
The `itertools.combinations()` function is similar to `permutations()`. However, there will be no repeat values in the result.

So, passing the string `"AB"` to the `combinations()` function will only result in `("A", "B")` as it considers both `("A", "B")` and `("B", "A")` to be the same. Also, note that `combinations()` does not allow repeated values in the result. Hence we do not see `("A", "A")` and `("B", "B")` here either. 
 
```
>>> combination = itertools.combinations("AB", 2)
>>> list(combination)
[('A', 'B')]
```

Like `permutations()`, we ill need to specify a length as argument.

```
>>> letters = ["A", "B", "C"]
>>> letter_combination = itertools.combinations(letters, 3)
>>> list(letter_combination)
[('A', 'B', 'C')]
```

## `combinations_with_replacement`
The `itertools.combinations_with_replacement()` function allows repeated values in the result.

```
>>> letter_combinations = itertools.combinations_with_replacement("AB", 2)
>>> list(letter_combinations)
[('A', 'A'), ('A', 'B'), ('B', 'B')]
```

## `product`
The `itertools.product()` function returns a Cartesian product of the input iterables.

```
>>> product = itertools.product("ABC", "xy")
>>> list(product)
[('A', 'x'), ('A', 'y'), ('B', 'x'), ('B', 'y'), ('C', 'x'), ('C', 'y')]
```

The function also takes an optional `repeat` argument which specifies the length of each resulting tuple.

```
>>> product = itertools.product("AB", repeat=2)
>>> list(product)
[('A', 'A'), ('A', 'B'), ('B', 'A'), ('B', 'B')]
```

## `chain`
The `itertools.chain()` function is used to chain iterables together and iterate over them simultaneously.

```
>>> countries = ["India", "Italy", "Ireland"]
>>> more_countries = ["United States", "United Kingdom", "Uruguay"]

>>> countries_list = itertools.chain(countries, more_countries)

>>> list(countries_list)
['India', 'Italy', 'Ireland', 'United States', 'United Kingdom', 'Uruguay']
```

## `islice`
The `itertools.islice()` function is used to slice an interable and return only the selected values. `islice()` takes optional `start`, `stop` and `step` arguments.

In the below example, we are slicing the iterable to return only the first 5 elements.
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

## `dropwhile`
The `itertools.dropwhile()` function will drop values from an iterable as long as a pre-defined condition is met. Once the condition fails, it returns **all** the remaining elements of the iterable.

In the following example, `dropwhile()` will drop elements from the iterable as long as the `x < 2` condition is met. As a result, the first three elements of the list are dropped. Once the condition fails on the fourth element, all the remaining elements are retured irrespected of whether they meet the condition or not.

```
>>> results = itertools.dropwhile(lambda x: x < 2, [0, 1, 1.5, 2, 1, 0, 5])
>>> list(results)
[2, 1, 0, 5]
```

## `takewhile`
The `itertools.takewhile()` function will return values from an iterable as long as they satisfy a pre-defined condition. Once the condition fails, all remaining elements are dropped.

In the below case, `takewhile()` will return elements from the list as long as the `x < 2` condition is met. Once the condition fails on the fourth element, all elements starting from the fourth element are dropped irrespective of whether they meet the condition or not.

```
>>> results = itertools.takewhile(lambda x: x < 2, [0, 1, 1.5, 2, 1, 0, 5])
>>> list(results)
[0, 1, 1.5]
```

## `compress`

## `accumulate`

## `groupby`

## `tee`