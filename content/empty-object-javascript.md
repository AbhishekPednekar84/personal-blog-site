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

console.log(Object.keys(obj).length) // 3

```

<br />

## Check for the empty object

```
// Empty object

obj = {}

console.log(Object.keys(obj).length) // 0
console.log(Object.keys(obj).length === 0) // true

```

<br />

## Why does this work?

`Object.keys()` returns an array containing the keys of the object passed to it. We can therefore use the `length` attribute to check the length of the resulting array.

```
obj = {"a": 1, "b": 2, "c": 3}

keysArray = Object.keys(obj)

console.log(keysArray) // ["a", "b", "c"]
console.log(keysArray.length) // 3

```

`Object.keys()` is supported across all browsers.
