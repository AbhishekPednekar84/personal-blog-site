Title: Embedding Jupyter Notebooks in a website
Date: 2019-08-19 12:00
Category: Python
Tags: Python, Jupyter
Slug: embedding-jupyter
Authors: Abhishek Pednekar
Summary: Embed Jupyter Notebooks in your website using Github and NBInteract
Cover: /static/images/black-gradient-article.jpg

In this post, we will learn how to embed **Jupyter Notebooks** in a website. The great thing about being able to embed notebooks is that either all or a subset of the notebook content, whether static or interactive can be made available directly on a website or a blog post. This is especially helpful for static sites (like **[Code Disciples](https://codedesiples.in)**) since the content can be added directly to the **Markdown**. Readers do not need to navigate to a notebook server or a repository to explicitly view the notebook.

To start off, we will create a **[Github Gist](https://gist.github.com/)** by uploading a **Jupyter Notebook (.ipynb file)**. To keep it simple, we will be using a notebook containing some Math formulae in **Markdown**. We can use a repository instead of a Gist. However, since we are dealing with just a few lines of Markdown, a Gist seems more appropriate. 

Once our gist is in place, we will be using a tool called *NBInteract* to generate an **html** file corresponding to our notebook. After a few modifications to the html file, we will embed the content to this blog post using an **iframe**. 

Now, while I agree that there might be other ways to achieve the same results, this is what I have found to best suit my needs. So let's get started.

## Creating the Gist
To create a gist, one needs to have a [Github](https://github.com/) account. Assuming you already have one, click on the *New Gist* option on the top right of the page. 

Before we proceed, we will need a Jupyter Notebook to work with. The one used for this blog is available in this *[Github repository](https://github.com/AbhishekPednekar84/codedisciples-blog-posts/tree/master/Index_2-embed-jupyter)*. 

On the gist creation page, we will need to add a description and the notebook filename with the extension (.ipynb). To add the contents, we can simply drag and drop our notebook to the page. If there are any dependencies (third-party packages) that are needed in order for the code in our notebook to run, we will need to add those as well. Dependencies if any, will need to be added to either *requirements.txt* (pypi) or *environment.yml* (Conda / pypi) files. These files will also need to be added to the gist by clicking on the **Add file** button. Finally, to create the gist click either of the **Create gist** buttons. I will be creating a public gist.

<br/>
![Gist]({static}/images/index2/gist.jpg)

## Creating the iframe
To create our iframe that will eventually be embedded into the blog, we will first convert our Jupyter Notebook into an html file. This will be achieved via a third-party package called *[nbinteract](https://www.nbinteract.com/)*. So let's first create a *[virtual environment](https://www.youtube.com/watch?v=APOPm01BVrk)* in the directory containing our notebook. 

Once the virtual environment is activated, let us run the `pip install nbinteract` command to install the library.

nbinteract is a command-line application (CLI). In order to use it, first navigate to the directory containing the .ipynb file and then run the below command.

```
nbinteract <notebook_filename>.ipynb -s <GitHub_Username>/<Gist_ID>
```
<br/>
![NBInteract]({static}/images/index2/nbinteract.jpg)

<br/>
This will create an html file with the same name as your Jupyter Notebook. Now before creating the iframe, we will need to make a couple of changes to the **html** file.

In the embedded JavaScript at the end of the file, change the provider from *gh* to *gist*. No change will be needed if you are using a GitHub Repository.

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

Also, nbinteract inserts a whole bunch of **Bootstrap** and **Font Awesome CSS** in the file. So keep as much or as little of it as you need. Finally, if you would like only a subset of your notebook to be visible on the website, you can delete the unwanted cells by removing the corresponding div tags form the html file.

For example, to exclude this cell,

<br/>
![delete-nb]({static}/images/index2/delete-nb.jpg)

<br/>
remove this block from the html file

<br/>
![delete-html]({static}/images/index2/delete-html.jpg)

<br/>
Now, let's embed an iframe tag in our blog, linking to the html file. I will be adding the below iframe tag directly to the Markdown corresponding to this blog. 

```
<iframe src="https://codedisciples.in/Index_2-Embed_Jupyter.html"></iframe>
```

Just like in a Jupyter notebook, you can view the underlying code (Markdown in our case) by right-clicking on any of the formulae and viewing the plain text source. 

<br/>
<iframe style="height: 500px" src="https://codedisciples.in/Index_2-Embed_Jupyter.html"></iframe>

<br/>
In conclusion, I would like to say that the best use case for embedding a notebook is interactive content. If your notebook contains plots which have interactive IPython widgets, those can be embedded into your blog. Users can then interact with the plot on the website using the widgets. Some great examples have been provided in the NBInteract documentation. 