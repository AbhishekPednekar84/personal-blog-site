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

```
// Empty object

obj = {}

console.log(Object.keys(obj).length) // 0
console.log(Object.keys(obj).length === 0) // true

```

`Object.keys()` is supported across all browsers.
