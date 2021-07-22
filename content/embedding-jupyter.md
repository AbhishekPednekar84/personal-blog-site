Title: Embedding Jupyter Notebooks in a website
Date: 2019-08-19 12:00
Category: Python
Tags: Python, Jupyter
Slug: embedding-jupyter
Authors: Abhishek Pednekar
Summary: Embed Jupyter Notebooks in your website using Github and NBInteract
Cover: /static/images/black-gradient-article.jpg

In this post, we will learn how to embed a Jupyter Notebook in a website. The great thing about being able to embed notebooks is that either all or a subset of the notebook content, whether static or interactive can be made available directly on a website or a blog post. This is especially helpful for static sites (like **[Code Disciples](https://codedesiples.in)**) since the content can be added directly to the markdown. Readers therefore do not need to navigate to a notebook server or a repository to explicitly view the notebook.

This post assumes that the reader has some experience of working with Github and is familiar with Python and pip.

To start, we will create a **[Github Gist](https://gist.github.com/)** by uploading a Jupyter Notebook (a file with extension `.ipynb`). To keep it simple, we will be using a notebook containing some Math formulae written in markdown. We can use a repository instead of a gist. However, since we are dealing with just a few lines of code, a gist seems more appropriate.

Once our gist is in place, we will be using a tool called **NBInteract** to generate an html file corresponding to our notebook. After a few modifications to the html file, we will embed the content in this blog post using an `iframe` tag. Agreed, that there might be other and no doubt better ways to achieve the same results. However, this is one of the simplest methods to achieve our result.

At the end of the post, the reader will be aware of how one can add a Jupyter Notebook to a website using an `iframe`.

<br />

## Creating the gist

To create a gist, one needs to have a [Github](https://github.com/) account. Assuming we already have one, we can create a new gist by navigating to [https://gist.github.com/<Your github username>](https://gist.github.com/<Your github username>) and clicking on the `+` icon on the top right.

Before we proceed, we will need a Jupyter Notebook to work with. The one used for this blog is available in this _[Github repository](https://github.com/AbhishekPednekar84/codedisciples-blog-posts/tree/master/Index_2-embed-jupyter)_.

With our notebook now in place, we can simply drag and drop it on the page to create a new gist. If there are any dependencies (third-party packages) that are needed in order for the code in our notebook to run, we will need to add those as well. Dependencies if any, will need to be added to either a `requirements.txt` file (for pypi) or an `environment.yml` file (for Conda / pypi). These files will also need to be added to the gist. Finally, to create the gist click either of the **Create gist** buttons. Our gist will be public in this case.

<br/>
![Gist]({static}/images/index2/gist.jpg)

<br />

## Creating the iframe

As mentioned earlier, we will be using the `iframe` tag in html to embed our notebook. Before we can do that, our notebook will need to be converted to an html file. This will be achieved via a third-party package called _[nbinteract](https://www.nbinteract.com/)_. So let's first create a _[virtual environment](https://www.youtube.com/watch?v=APOPm01BVrk)_ in the directory containing our notebook. Creating a virtual environment is optional but is a good practice as it isolates all our project dependencies.

Once the virtual environment is activated, we will run the `pip install nbinteract` command to install the library. `nbinteract` is a command-line application (CLI). To use it, we will first navigate to the directory containing the `.ipynb` file and then run the below command.

```
nbinteract <notebook_filename>.ipynb -s <GitHub_Username>/<Gist_ID>
```

<br/>
![NBInteract]({static}/images/index2/nbinteract.jpg)

This will create an html file with the same name as our Jupyter Notebook. Now before creating the `iframe`, we will need to make a couple of changes to the html file.

In the embedded JavaScript at the end of the file, we will change the provider from `gh` to gist. Had we used a Github repository instead of a gist, no change was needed.

```
  <!-- Loads nbinteract package -->
  <script src="https://unpkg.com/nbinteract-core" async></script>
  <script>
    (function setupNbinteract() {
      // If NbInteract hasn't loaded, wait one second and try again
      if (window.NbInteract === undefined) {
        setTimeout(setupNbinteract, 1000)
        return
      }

      var interact = new window.NbInteract({
        spec: '<GitHub_Username>/<Gist_ID>/master',
        baseUrl: 'https://mybinder.org',
        // provider: 'gh',
        provider: 'gist',
      })
      interact.prepare()

      window.interact = interact
    })()
  </script>
```

Also, `nbinteract` inserts a whole bunch of Bootstrap and Font-Awesome CSS in the file. So we can keep as much or as little of it. Finally, some sections of the notebook can be excluded if needed by simply removing the corresponding `div` tags.

For example, to exclude this cell,

<br/>
![delete-nb]({static}/images/index2/delete-nb.jpg)

we can remove this block from the html file

<br/>
![delete-html]({static}/images/index2/delete-html.jpg)

Now, let's embed an `iframe` tag in our blog that links to the html file created by `nbinteract`. we will be adding the below iframe tag directly to the markdown of this blog post.

```
<iframe src="https://codedisciples.in/Index_2-Embed_Jupyter.html"></iframe>
```

Just like in a Jupyter notebook, we can view the underlying code (markdown in our case) by right-clicking on any of the formulae and viewing the plain text source.

<br/>
<iframe style="height: 500px" src="https://codedisciples.in/Index_2-Embed_Jupyter.html"></iframe>

<br/>
In conclusion, one of the best use cases for embedding a notebook is interactive content. If a notebook contains plots which have interactive `IPython widgets`, then those can be embedded into a website. Users can then interact with the plot on the website using the widgets. Some great examples have been provided in the [NBInteract documentation](https://www.nbinteract.com/examples/examples_intro.html).

<br />

## Further Reading

**Ezequiel Leonardo Castaño** goes over some of the topics discussed here in further detail. Please check out his excellent article [Embed Interactive Jupyter Notebooks in Static Websites for Free](https://elc.github.io/posts/embed-interactive-notebooks/).
