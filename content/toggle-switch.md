Title: Toggle Switches
Date: 2020-02-23 12:00
Category: CSS
Tags: HTML, CSS
Slug: toggle-switches
Authors: Abhishek Pednekar
Summary: Creating toggle switches with HTML and CSS
Cover: /static/images/black-gradient-article.jpg

Modern websites no longer use vanilla checkboxes. Toggle switches built on top of checkboxes give any UI a cleaner and professional look and feel. 

In this post, we will learn how to create toggle switches using `HTML` and `CSS`.

This post assumes that the reader is familiar with basic `HTML` and `CSS`. 

## HTML

The HTML for our toggle switch consists of just three tags - `<label>`, `<input>` and `<span>`. The `<label>` will be a container and will constitute the switch while the `<span>` will constitute the slider that moves from left to right and vice versa. The `checkbox` element is what our toggle switch will be built upon. In other words, checking the box will move our slider to the `on` position and un-checking it will move the slider to the `off` position.

```
  <label class="switch">
    <input type="checkbox">
    <span class="slider"></span>
  </label>
```

## CSS

The `CSS` is what will render our simple `checkbox` into a nice looking toggle switch.

The `switch` class will have a `relative` positioning so that the position of the `slider` can be set to `absolute`. The other properties will set the `width` and `height` of the switch. We will also set the `opacity` of the checkbox` to `0`, so that the original `checkbox` element is not visible (especially for rounded toggle switches).

```
.switch {
  position: relative;
  display: block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
}
```

Next, we will style the slider. As mentioned above, the slider will have its position property set to `absolute`. Using the `before` selector, we are ensuring that the slider starts on the left side of the switch, which is the `off` position. For the rectangular switch, the slider will be a square having a `width` and `height` of `26px` with a `white` background. We will change this for the rounded switch. The `transition` property gives a nice sliding effect as the slider moves between the `on` and `off` states of the switch.

**Note**: For additional reading, the [MDN documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/::before) does a good job of explaining the 
`before` CSS selector.

```
.slider::before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  background-color: #fff;
  left: 4px;
  top: 4px;
  transition: 0.3s;
}
```

The `slider` class below sets the background of our `<span>` to a dark-gray color which in our case indicates that the switch is in an `off` state. We also set the `top`, `bottom`, `left` and `right` properties to `0` to eliminate spaces around all the edges between the `<span>` and its parent `<label>` container.

```
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #758184;
  transition: 0.3s;
}
```

When the `checkbox` is checked, we will change the `background-color` of the `<span>` from dark gray to a light green shade indicating that the switch is `on`. Also, using `transform: translateX(26px)` we will move the slider by `26px` along the positive X axis or to put it simply, from left to right. 

```
input:checked + .slider {
  background-color: #32ff6a;
}

input:checked + .slider::before {
  transform: translateX(26px);
}

```

That's it! The switch can now be toggled between the `on` and `off` states.

## A Rounded Toggle Switch

To create a rounded switch, we will add an additional `round` class to the `<span>` tag. 

```
<span class="slider round"></span>
```

Setting the appropriate values for the `border-radius` property will give the slider and the switch a rounded look.

```
.slider.round {
  border-radius: 34px;
}

.slider.round::before {
  border-radius: 50px;
}
```

Here is the complete code:

<iframe src="https://codepen.io/abhishekpednekar84/pen/bGdwRGY" style="width: 846px; height: 700px"></iframe>