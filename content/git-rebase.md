Title: git rebase - a cautious alternative to git merge
Date: 2019-09-27 17:00
Category: Git
Tags: Git
Slug: git-rebase
Authors: Abhishek Pednekar
Summary: An overview of the rebase workflow for git repositories
Cover: /static/images/black-gradient-article.jpg

In this post, we will look at `git rebase` and scenarios where it can and should not be used as an alternative to `git merge`. For those unfamiliar with the concept of merging - at a super high-level, when you are done developing and testing on your *feature* branch and are ready to merge those changes with *master*, `git merge` performs the merge operation by creating a **new** commit for the merge. With that said, let's look at what happens during a *rebase* operation.

We will start by initializing an empty local repository called **rebase-demo**. Note that we are in the *master* branch.

```
c:\rebase-demo
git init
Initialized empty Git repository in c:/rebase-demo/.git/

c:\rebase-demo (master -> origin)
```

Now, we will add an index.html file directly in the master branch and commit it.

```
c:\rebase-demo (master -> origin)
touch index.html

c:\rebase-demo (master -> origin)
git add -A

c:\rebase-demo (master -> origin)
git commit -m "Initial Commit"
[master (root-commit) 8ef361a] Initial Commit
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 index.html
```

Next, we will create a feature branch called *new-feature*.

```
c:\rebase-demo (master -> origin)
git branch new-feature

c:\rebase-demo (master -> origin)
git checkout new-feature
Switched to branch 'new-feature'

c:\rebase-demo (new-feature -> origin)
```

While in *new-feature*, let's add a text file and commit the change.

```
c:\rebase-demo (new-feature -> origin)
git commit -m "Added text.txt"
[new-feature 5a1cabb] Added text.txt
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 text.txt
``` 

Now let's add an image in *new-feature* and commit the change again.

```
c:\rebase-demo (new-feature -> origin)
git commit -m "Added image.jpg"
[new-feature 100152d] Added image.jpg
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 image.jpg
```

So at this point, we have two commits in the *new-feature* branch that do not exist in master. This is what our commits look like at the moment.

           O-------O new-feature
           |
           |
           O master

Now, let's say someone on our team added a new commit to the *remote master* branch which we then pulled into our *local master*. In our example, let's say a .py file was added as part of the new commit in the *master* branch. So now, our commits would look something like this.

           O------O new-feature
           |
           |
           O------O master

Before we perform the `git rebase`, let's quickly summarize the values of our commit hashes.

1. Initial commit - 8ef361a (master, new-feature)
2. Added text.txt - 5a1cabb (new-feature)
3. Added image.jpg - 100152d (new-feature)
4. Added python.py - 257bc71 (master)

We will also run `git log` on both our branches.

<br/>
![log-master]({static}/images/index10/log-master.jpg)

<br/>
![log-feature]({static}/images/index10/log-feature.jpg)

Finally, let's run `git rebase` on our *new-feature* branch. 

```
c:\rebase-demo (new-feature -> origin)
git rebase master
First, rewinding head to replay your work on top of it...
Applying: Added text.txt
Applying: Added image.jpg
```

By rebasing *new-feature* onto *master*, we are telling Git to find the most recent commit (Initial commit in our case) that is common to both branches. Git will then put all the commits from *master* down and add the *new-feature* commits one by one. This is what our commits look like now.

           O------O------O------O
               master        new-feature

Note that if there are any conflicts during the rebase, Git will call those out so that we can address them manually. Now let us once again run `git log`. Notice that after the `git rebase`, Git has moved the two commits in *master* down and then added the two commits from *new feature*. This, although the "Added python.py" commit was done after the two commits in *new-feature*. Another crucial thing is that unlike `git merge`, no new commit was created. Just the existing commits were realigned linearly. In other words, our *new-feature* branch is now a fast forward from *master*.

Also, did you notice the commit hash values? Other than the one for the "Initial Commit", all the hash values changed while Git moved our commits around during the `git rebase`. So essentially Git created new commit objects thereby modifying the Git history. My previous [post](https://www.codedisciples.in/advanced-git.html) on Git briefly talked about modifying the Git history. This is a bad idea if we are planning to push changes that modified the Git history, to a remote repository from where others will pull in our changes. Modifying Git history is ideal if we are working on projects that do not involve a large scale sharing of the codebase. 

<br/>
![git-log-rebase]({static}/images/index10/git-log-rebase.jpg)

To further highlight the difference between `git rebase` and `git merge`, here is a screenshot of a `git log` after the two branches were merged. Notice the additional commit created by the merge operation. Also, the git history remains unchanged.

1. Initial commit - ed4bee2 (master, new-feature)
2. Added text.txt - 88ea609 (new-feature)
3. Added image.jpg - f9a52da (new-feature)
4. Added python.py - 38fa1e0 (master)

<br/>
![git-log-merge]({static}/images/index10/git-log-merge.jpg)

Our commits would now look something like this.

                                     master
           O------O------O------O------O
                                  new-feature  