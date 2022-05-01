Title: Swapping Variables in Python - How & Why
Date: 2022-05-01 21:00
Category: Javascript
Tags: Javascript
Slug: variable-swapping-python
Authors: Abhishek Pednekar
Summary: How and why does Python's succinct variable swapping syntax work
Description: How and why does Python's succinct variable swapping syntax work
Cover: /static/images/gradient-texture-cubes.jpg

In today's article, we will see how to swap the values of two variables in Python. More importantly, we will understand why this works.

Traditionally, variable swapping in any language involves the introduction of a temporary variable to hold a value.

```
x = 1
y = 2

temp = x
x = y
y = temp

# Will output x = 2
print(f"x = {x}")

# Will output y = 1
print(f"y = {y}")

```

Python can do this in one line.

```
x, y = y, x
```

The output will be as expected.

```
# Will output x = 2
print(f"x = {x}")

# Will output y = 1
print(f"y = {y}")
```

<br />

## Why does this work?

To understand why this works, we need to delve into the world of tuples. Tuples are immutable data structures in Python. Traditionally, a tuple is represented as x = (1, 2). Its elements can be accessed using the index values.

```
x = (1, 2)

# Will output 1
print(x[0])

# Will result in an error
# 'tuple' object does not support item assignment

x[0] = 2

```

While we usually represent tuples using `()` brackets, a tuple can also be written as `x = 1, 2`.

```
x = 1, 2

# Will output <class 'tuple'>
print(type(x))
```

In addition to using the index values, we can extract values from tuples by using the **unpacking** syntax.

```
x, y = 1, 2

# Will output x = 1, y = 2
print(f"x = {x}, y = {y}")

x, y, *z = 1, 2, 3, 4

# Will output x = 1, y = 2, z = [3, 4]
print(f"x = {x}, y = {y}, z = {z}")

```

We can, therefore, use the unpacking method to swap variables as well.

```
x, y = 1, 2

# Will output y, x = 2, 1
print(f"y, x = {y}, {x}")

# Variables are swapped!
x, y = y, x

```
