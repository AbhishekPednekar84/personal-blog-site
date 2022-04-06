Title: CSS ::selection Selector
Date: 2022-04-06 22:00
Category: CSS
Tags: CSS
Slug: css-selection
Authors: Abhishek Pednekar
Summary: Add a little more pizzazz to your modern website with `::selection`

In this post, we'll learn how we can change the default text selection color on a website.

By default, a browser applies a dark blue background with black text when the text on a webpage is selected.

<br />
![css-selection-default]({static}/images/index25/css-selection-default.jpg)

<br />
To change this default behavior, we can use the `::selection` CSS selector.

```
/* CSS ::selection selector */

::selection {
  color: #164e63;
  background: #cffafe;
}
```

<br />
![css-selection-default]({static}/images/index25/css-selection-new.jpg)

The usability across different browsers is good - <a href="https://caniuse.com/?search=%3A%3Aselection" target="_blank" rel="noopener noreferrer">caniuse.com</a>
