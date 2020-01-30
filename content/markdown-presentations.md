Title: Presentations with Markdown
Date: 2020-01-30 12:00
Category: Markdown
Tags: Markdown
Slug: markdown-presentations
Authors: Abhishek Pednekar
Summary: Creating presentation slides with Markdown, Pandoc and LaTeX
Cover: /static/images/black-gradient-article.jpg


For several years, Microsoft Powerpoint has been the industry's goto software for creating presentation slides. While Powerpoint is great and comes with a lot of features out of the box, there is a bit of a learning curve for beginners. Today, however, several other options make creating slides a lot easier and therefore a lot less time-consuming. One of them is to use Markdown to create slide decks. In this post, we will be using simple Markdown syntax and convert it to a presentation with Pandoc and LaTeX.

The post assumes that the reader is familiar with basic Markdown syntax (if not, [this](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) is a nice cheatsheet).

At the end of this post, the reader will be able to install all the pre-requisite software and create presentation slides using Markdown.

## Software Installation
As touched upon already, we will need to install some software before we start writing our Markdown code.

### Pandoc
Pandoc will allow us to convert files from one format to another. In our case, that will be Markdown to PDF. Pandoc can be installed from the [official website](https://pandoc.org/installing.html). Installers are available for different platforms. The installation process will add Pandoc to the system `PATH`. 

### LaTeX
To install LaTeX, we will install **MiKTeX** which is a free distribution for LaTeX. Installing LaTeX will allow us to use the `beamer` class which is needed to create our slides and will also enable us to download the `PdfLaTeX` package, which we will use to convert our Markdown file to a PDF output.

The MiKTeX installer can be downloaded from the [official website](https://miktex.org/download). If there are any issues with downloading the Windows installer, using the `wget` package on Windows Subsystem for Linux is a good alternative. Simply start a shell and run `wget https://miktex.org/download/ctan/systems/win32/miktex/setup/windows-x64/basic-miktex-2.9.7269-x64.exe`.

Once the installation is complete, we will have access to the MikTex console on our computer and the path to the binary file will be added to the system `PATH`. First, we will open the `Tasks` menu and click `Refresh file name database`.  Next, in the `Packages` section of the console, we will select the `beamer`, `pdftex` and `pdftexcmds` packages and install them.

<br />
![miktex]({static}/images/index17/miktex.jpg)

# Writing our Markdown
With all our pre-requisite software now installed, we can write some Markdown. The following code is written in a file named `demo.md`.

```
---
title: 
- Create slides in Markdown
author:
- Abhishek Pednekar
---


# Text
### Basic text formatting
| Markdown Syntax | Output |
| ---------------|--------- |
| `**Bold**` | **Bold** |
| `*Emphasis*` | *Emphasis* |
| `~~Strikethrough~~` | ~~Strikethrough~~|


# Lists
### Markdown syntax:
<pre>
+ Item1
+ Item2
+ Item3
</pre>

### Output:
+ Item1
+ Item2
+ Item3
```

+ The first section (enclosed within `---`) is the introduction and will be the first slide in our deck. Here we can specify the topic, author, date etc..
+ Each section that starts with a Markdown heading (`#` in this case) will correspond to a distinct slide in our deck. It is critical to note that the headings here follow a hierarchical structure. We have used the Markdown `#` to specify the title of our first slide. Any smaller heading Markdown's like `##` or `###` on the slide will therefore just be sub-sections on the slide. Until the next `#` is encountered, all the content will be on the first slide itself. Had we used `##` to specify the title of the first slide, then `###`, `####` etc.. would have been subsections on the slide. Also, each section starting with `##` would have then corresponded to a distinct slide in our deck.

The content of each slide is written in Markdown syntax. In the next section, we will convert our Markdown file into a PDF slide deck.

## Generating the slides
To generate the slides, navigate to the folder containing the `demo.md` file in the command prompt / terminal and run the command `pandoc demo.md -t beamer -o presentation.pdf`. 

By running this command, we are telling `pandoc` to (`-t`) use the `beamer` class and generate an output (`-o`) file called `presentation.pdf` using the contents of `demo.md`.

That's it! We should now see a PDF file called `presentation.pdf` in the same folder as `demo.md`.

<br />
![slide1]({static}/images/index17/slide1.jpg)

![slide2]({static}/images/index17/slide2.jpg)

![slide3]({static}/images/index17/slide3.jpg)

## Adding themes
While our presentation looks okay, it would be good to add a nice theme and make it look a lot better. Luckily for us, `beamer` comes with some built-in themes and colors to choose from. The [Beamer theme gallery](http://deic.uab.es/~iblanes/beamer_gallery/) website lists all the available themes and color schemes.

To specify a theme, we just need a small change to our introduction section.

```
---
title: 
- Create slides in Markdown
author:
- Abhishek Pednekar
theme:
- Madrid
---
```

Here's how we can specify both, a theme and a color scheme.

```
---
title: 
- Create slides in Markdown
author:
- Abhishek Pednekar
theme:
- Madrid
colortheme:
- lily
---
```

To generate our new slide deck, we can again run `pandoc demo.md -t beamer -o presentation.pdf`.

<br />
![theme1]({static}/images/index17/theme1.jpg)

![theme2]({static}/images/index17/theme2.jpg)

![theme3]({static}/images/index17/theme3.jpg)