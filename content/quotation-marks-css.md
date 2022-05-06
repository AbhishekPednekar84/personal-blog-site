Title: Easy quotation marks with CSS
Date: 2022-05-06 22:00
Category: CSS
Tags: CSS
Slug: quotation-marks-css
Authors: Abhishek Pednekar
Summary: Add quotation marks to your blockquote's with these easy CSS properties

Today, we will see a simple way to add quotation marks around text using CSS. While there are several ways to do this, this, by far, is one of the easiest ways.
<br />

## HTML

Let's say this HTML `<blockquote>` needs to be enclosed with quotation marks.

```
<blockquote>
  Add some quotation marks around me please!
</blockquote>
```

<br />

## CSS

We will use the `::before` and `after::` pseudo elements to add the quotation marks around the text.

```
blockquote::before {
  content: open-quote;
}

blockquote::after {
  content: close-quote;
}
```

<br />

Check out the [codepen](https://codepen.io/abhishekpednekar84/pen/ZErboOb).
