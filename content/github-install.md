Title: Installing Python packages from Github
Date: 2020-07-30 12:00
Category: Python
Tags: Python
Slug: github-install
Authors: Abhishek Pednekar
Summary: `pip install` a Python package from Github
Cover: /static/images/gradient-texture-cubes.jpg

In this post, you will learn how to `pip install` a Python package from Github. Installing a package from Github instead of the Python Package Index (PyPI) is useful when the package version (latest commit for instance) on Github contains changes that you would like to use or test but are not available on the latest PyPI version. This way, as a developer, you need not wait for the next release of a package to work with a specific change or feature. As long as the change is present in the version control system (VCS), you can work with it in advance to determine whether your project will be compatible with the new features.

This post assumes that the reader is familiar with using `pip`. The examples will use a [virtual environment](https://www.youtube.com/watch?v=APOPm01BVrk). Creating a virtual environment is optional, however, recommended. This post uses the `flask` library as an example.

Although this post demonstrates installing Python packages from Github, `pip` also supports installations from Mercurial, Subversion and Bazaar. The [official documentation](https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support) has more details on VCS support.

---

## Verifying the package versions

At the time of writing this post, the `flask` version in PyPI was `1.1.2` released on April, 3rd 2020. Running the `pip install flask` command will install the `flask` package and its dependencies in the virtual environment.

```
(venv) λ pip install flask
Collecting flask
  Using cached https://files.pythonhosted.org/packages/f2/28/2a03252dfb9ebf377f40fba6a7841b47083260bf8bd8e737b0c6952df83f/Flask-1.1.2-py2.py3-none-any.whl
Collecting click>=5.1 (from flask)
...
...

Successfully installed Jinja2-2.11.2 MarkupSafe-1.1.1 Werkzeug-1.0.1 click-7.1.2 flask-1.1.2 itsdangerous-1.1.0
```

To verify the installation, you can run the `pip freeze` command.

```
(venv) λ pip freeze
click==7.1.2
Flask==1.1.2
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
Werkzeug==1.0.1
```

Now, if you verify the [repository](https://github.com/pallets/flask) for `flask` on Github, you will notice several commits to the `master` branch after April 3rd, meaning that they are not part of the version of `flask` that you just installed. If you need to incorporate any of these commits into your local `flask` installation before they are made available in PyPI, you can install the specific version of the package directly from Github as you will see in the next section.

![commits]({static}/images/index24/commits.jpg)

---

## Installing from Github

To `pip install` from a Github repository, the repository needs to have a `setup.py` file.

While installing from a VCS, it is beneficial to pass the `-e` or `--editable` argument to the `pip install` command. Including the `-e` argument will install the package in the editable mode and will help if we are creating a `requirements.txt` file as you will see later on. The `-e` argument is also useful if you are developing and testing a package locally.

Running `pip install -e git+https://github.com/pallets/flask#egg=flask` will clone and install the latest version of `flask` from Github. The `#egg=flask` specifies the name of the project.

```
(venv) λ pip install -e git+https://github.com/pallets/flask#egg=flask
Obtaining flask from git+https://github.com/pallets/flask#egg=flask
  Cloning https://github.com/pallets/flask to c:\learning\python\github-pip-demo\venv\src\flask
  Generating metadata for package flask produced metadata for project name flask. Fix your #egg=flask fragments.
Collecting Werkzeug>=0.15 (from flask)
 ...
 ...

  Running setup.py develop for flask
Successfully installed Jinja2-2.11.2 MarkupSafe-1.1.1 Werkzeug-1.0.1 click-7.1.2 flask itsdangerous-1.1.0
```

Again, you can verify the installation with the `pip freeze` command.

```
(venv) λ pip freeze
click==7.1.2
-e git+https://github.com/pallets/flask@37551e6798aabefd549340a7d3840b7648b413c7#egg=Flask
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
Werkzeug==1.0.1
```

Notice that you have now installed the latest version of `flask` from the project's Github repository. You can confirm that by comparing the hash (`flask@37551e6...`) of the installation with that on Github.

![flask-hash]({static}/images/index24/flask-hash.jpg)

As mentioned earlier, using the editable mode helps if we are creating a requirements file. To create one, you can run the `pip freeze > requirements.txt` command. Now, you can share this `requirements.txt` file with anyone who is looking to use or collaborate on your project thereby ensuring that they use the same version of `flask` as you and not the one from PyPI.

To install from a requirements file, you can run `pip install -r requirements.txt`.

```
(venv) λ pip install -r requirements.txt

...
...
Obtaining Flask from git+https://github.com/pallets/flask@37551e6798aabefd549340a7d3840b7648b413c7#egg=Flask (from -r requirements.txt (line 2))
  Cloning https://github.com/pallets/flask (to revision 37551e6798aabefd549340a7d3840b7648b413c7) to c:\learning\python\github-pip-demo\venv\src\flask
...
...
```

---

## Installing a specific version

If you would like to install a specific commit, you can do that based on the **commit hash**. For instance, to install the version of `flask` before the most recent commit, you will need the commit hash from Github.

![commit-1]({static}/images/index24/commit-1.jpg)
<br />

![commit-2]({static}/images/index24/commit-2.jpg)
<br />

Once you have the hash, you can substitute it in the following command - `pip install -e git+https://github.com/pallets/flask@<the-commit-hash>#egg=flask`.

```
pip install -e git+https://github.com/pallets/flask@36e6fc8#egg=flask

Obtaining flask from git+https://github.com/pallets/flask@36e6fc8#egg=flask
  Cloning https://github.com/pallets/flask (to revision 36e6fc8) to c:\learning\python\github-pip-demo\venv\src\flask
...
...

```

---

## Installing without the `-e` argument

If you were to install a library from a VCS without the `-e` argument and include it in the `requirements.txt` file, `pip` will throw an error while installing the library using the `pip install -r requirements.txt` command.

```
(venv) λ pip install git+https://github.com/pallets/flask#egg=flask
Collecting flask from git+https://github.com/pallets/flask#egg=flask
  Cloning https://github.com/pallets/flask to c:\users\abhi_\appdata\local\temp\pip-install-f5afsoas\flask
...
...
Successfully installed flask-2.0.0.dev0
```

Below is what the `requirements.txt` file looks like after this installation. Notice that that version of `flask` has a `.dev0`.

```
(venv) λ pip freeze
click==7.1.2
Flask==2.0.0.dev0
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
Werkzeug==1.0.1
```

Now, if you try to install from the requirements file, you will see an error as `pip` will not be able to find that specific version on Github.

```
(venv) λ pip install -r requirements.txt
Collecting click==7.1.2 (from -r requirements.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/d2/3d/fa76db83bf75c4f8d338c2fd15c8d33fdd7ad23a9b5e57eb6c5de26b430e/click-7.1.2-py2.py3-none-any.whl
Collecting Flask==2.0.0.dev0 (from -r requirements.txt (line 2))
  Could not find a version that satisfies the requirement Flask==2.0.0.dev0 (from -r requirements.txt (line 2)) (from versions: 0.1, 0.2, 0.3, 0.3.1, 0.4, 0.5, 0.5.1, 0.5.2, 0.6, 0.6.1, 0.7, 0.7.1, 0.7.2, 0.8, 0.8.1, 0.9, 0.10, 0.10.1, 0.11, 0.11.1, 0.12, 0.12.1, 0.12.2, 0.12.3, 0.12.4, 0.12.5, 1.0, 1.0.1, 1.0.2, 1.0.3, 1.0.4, 1.1.0, 1.1.1, 1.1.2)
No matching distribution found for Flask==2.0.0.dev0 (from -r requirements.txt (line 2))
```

---

## Conclusion

You should now be familiar with installing a Python package from Github. If you would like to use package features that are not in the latest version on PyPI, then installing from a VCS is the way to go.
