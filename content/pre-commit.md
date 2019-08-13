Title: Pre-commit hooks for Python code
Date: 2019-08-12 12:00
Category: Python
Tags: Python
Slug: pre-commit
Authors: Abhishek Pednekar
Summary: Using ```black``` and ```flake-8``` as pre-commit hooks in Python for code formatting and complying to PEP8 norms respectively
Cover: /static/images/black-gradient-article.jpg

Code reviews are great. But at the same time, they can be frustrating if the code being reviewed is not formatted uniformly. This is a common scenario in larger teams wherein multiple developers are working on the same feature branch or code base. More hours spent on fixing the formatting also results in loss of productive time which could be used to further improve code logic. Also, none of us like being that super nitpicky team member who comments on a trailing whitespace or the fact that one string has single quotes while another is enclosed within double quotes. 

Luckily, [pre-commit](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) hooks exist to alleviate these concerns by eliminating the need to manually review formatting and [PEP8](https://www.python.org/dev/peps/pep-0008/) checks. A pre-commit hook is a short script that runs before committing our code. The script can be a means to check the code formatting or its compliance to PEP8. If the script runs successfully, the code is committed to source control, else the commit is unsuccessful.

In this post, we’ll take a look at two popular Python libraries and how we can add them to a pre-commit hook. Please note that I am using a **Windows** laptop for this demo. The same commands should work on **macOS** as well.

1. [black](https://black.readthedocs.io/en/stable/) - a code formatter
2. [flake8](http://flake8.pycqa.org/en/latest/) - a PEP8 compliance checker

Please refer to this [Github repository](https://github.com/AbhishekPednekar84/codedisciples-blog-posts/tree/master/Index_1-pre-commit-hooks) for the complete code.

### Pre-commit framework 

Creating a pre-commit hook is made really simple by this [pre-commit framework](https://github.com/pre-commit) written in Python. To incorporate `pre-commit` into a project, one needs to follow these steps.

1. Create a [virtual environment](https://www.youtube.com/watch?v=APOPm01BVrk) (optional but recommended)
2. Install the pre-commit library: `pip install pre-commit`
3. Add the hooks (black and flake-8 in our case) to the `.pre-commit-config.yaml` file 
4. Run the `pre-commit install` command to install the hook in the `.git/` directory

Here is what our `.pre-commit-config.yaml` file will look like.

```
repos:
-   repo: https://github.com/ambv/black
    rev: stable
    hooks:
    - id: black
      language_version: python3.7
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.3.0
    hooks:
    - id: flake8
```

The `pre-commit` framework that we installed (step 2) includes `flake8`. Hence all we need to specify is it's id. For `back` however, we need to specify the exact path from where it needs to be sourced.

In the following sections, we'll take a look at these libraries in detail.

### Code formatter - `black` 

Black is an uncompromisingly opinionated code formatter. It has been implemented with certain design decisions that are applied to the code being formatted. By adopting `black` into your project, you are essentially letting the library take all the code formatting decisions for you. Therefore, please read through the [documentation](https://black.readthedocs.io/en/stable/) to understand what the design decisions are. Below are some of the notable one's. 

- The number of characters per line are 88 (as opposed to 79 defined in PEP8)
- Strings are always enclosed in double quotes
- A trailing comma is added to comma separated elements
- For functions with multiple arguments, each argument is wrapped per line 

If any of these decisions are not acceptable to your formatting guidelines, `autopep8` is a good alternative. Also, this is part of the `pre-commit` framework like `flake8`.   

In order to use `black` we will need to include a `pyproject.toml` file in our project folder. This file contains details of file types that are included and excluded during formatting. More importantly, if you would like to change the number of characters per line, just modify the `line-length` attribute in the TOML file.

```
[tool.black]
# Changed line-length to 80 from the default 88
line-length = 80 
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

### PEP8 checker - `flake8`

`flake8` is a great library that check's our code compliance with PEP8. In order for `black` to function smoothly with `flake8`, we need to specify some [error codes](https://flake8.pycqa.org/en/latest/user/error-codes.html) in the `.flak8` configuration file.

```
[flake8]
ignore = E203, E266, E501
max-line-length = 80
max-complexity = 10
select = B,C,E,F,W,T4,B9
```

To go over this very quickly, in the first like, we are specifying the error codes that we would like flak8 to ignore. The `max-line-length` has been set to 80 to match our `black` configuration values. `max-complexity' defines the [McCabe complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity) of a function. This is deactivated by default. The `select` attribute enables errors and warnings which are turned off by default.

That's it, with all this in place, we are ready to run the hook on our code. 

Here's some rather sloppily formatted code. Notice that there is no space prior to the equal to (=) operator, one element of the list uses double quotes while the rest are enclosed within single quotes and there is only one blank line prior to and after the function definition. There is also an additional whitespace on line 1 at the end of the (''') quotes.

![Unformatted-Code]({static}/images/Unformatted_Code.jpg)

Let's create and run or hook on this code. As indicated earlier, once we `pip install` the `pre-commit` library, we need to install it using the `pre-commit install` command.

![Pre-Commit]({static}/images/Pre-Commit.jpg)

Now, when we run our `git commit`, we see that `black` fails the commit but auto-formats the file. `flake8` fails the commit due to the whitespace on line 1. This whitespace needs to be removed manually before our next `git commit`.

![Initial-Commit]({static}/images/Initial_Commit.jpg)

Here's what our code looks like after all the formatting and the whitespace correction. Note that the list elements are now wrapped on separate lines. The spacing around the operators and the function definition is uniform. Also, all our strings are now enclosed within double quotes.

![Formatted-Code]({static}/images/Formatted_Code.jpg)

Let's go ahead and commit this. If all is good, both out hooks should pass followed by a successful `git commit`.

![Final-Commit]({static}/images/Final_Commit.jpg)