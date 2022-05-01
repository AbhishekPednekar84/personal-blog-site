Title: Check for empty objects in Javascript
Date: 2022-04-28 21:00
Category: Javascript
Tags: Javascript
Slug: empty-object-javascript
Authors: Abhishek Pednekar
Summary: Check if a Javascript object is empty
Description: Check if a Javascript object is empty
Cover: /static/images/gradient-texture-cubes.jpg

In this short article, we will learn how to check if a Javascript object is empty (`{}`). This is particularly useful when checking responses from API's. We will run this test using the `Object.keys()` method.

```
// Non-empty object
obj = {"a": 1, "b": 2, "c": 3}

// Will output 3
console.log(Object.keys(obj).length)

```

<br />

## Check for the empty object

```
// Empty object
obj = {}

// Will output 0
console.log(Object.keys(obj).length)

// Will output true
console.log(Object.keys(obj).length === 0)

```

<br />

## Why does this work?

`Object.keys()` returns an array containing the keys of the object passed to it. We can therefore use the `length` attribute to check the length of the resulting array.

```
obj = {"a": 1, "b": 2, "c": 3}

keysArray = Object.keys(obj)

// Will output ["a", "b", "c"]
console.log(keysArray)

// Will output 3
console.log(keysArray.length)

```

`Object.keys()` is supported across all browsers.
