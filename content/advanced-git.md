Title: Advanced Git Commands
Date: 2019-09-03 12:00
Category: Git
Tags: Git
Slug: advanced-git
Authors: Abhishek Pednekar
Summary: A look at some git commands beyond the usual workflow
Cover: /static/images/black-gradient-article.jpg

In this post, we will take a look at some useful **git** commands. These commands supplement the usual git workflow and help in fixing or undoing mistakes. This post assumes that the reader already knows basic commands like `git status`, `git add`, `git commit`, `git branch`, `git push` etc...

To demonstrate the usage of the git commands, we will be using a simple code snippet in this post. The snippet will be saved in the file **calc.py**. The file itself will be present in a local git repository with two branches - **master** and **new-feature**

The `git log` command shows that we have only had one commit so far and the `git branch` command lists all the current local branches.

![initial-setup]({static}/images/index6/initial-setup.jpg)

```
# Code snippet - basic Arithematic operations - calc.py
def calc(operator, x, y):
    return {
        "Add": f"{x} + {y} = {x + y}",
        "Sub": f"{x} - {y} = {x - y}",
        "Mul": f"{x} * {y} = {x * y}",
        "Div": f"{x} / {y} = {x / y}",
        "Floor": f"{x} // {y} = {x // y}"
    }.get(operator, "Not found!")
```

### The `git checkout` command
Let's say we made some changes to our code. Now for some reason, before adding our changes to staging (`git add`), we decide not to commit them. The best way to bring our files back to their original state will be to use the `git checkout` command.

To demonstrate, we will modify **calc.py** by adding a comment after the subtract function in our code snippet - `"Sub": f"{x} - {y} = {x - y}", # Subtract function`. 

Running a `git status` and `git diff` in our repository, shows the modified file and the exact changes that were made respectively.

![checkout1]({static}/images/index6/checkout1.jpg)

To undo the changes, let's run `git checkout calc.py`. Running a `git status` or `git diff` now will no longer show any changes as the code has been reverted to its original state.

![checkout2]({static}/images/index6/checkout2.jpg)

### Fixing `git commit`'s
Providing a descriptive commit message is very important as it helps other developers get a high level of understating of the changes that were checked-in. However, there could be scenarios wherein we may provide an incorrect commit message or inadvertently make a typo in our message. These issues can be fixed using the `git commit --amend` command.

To demonstrate, I will add a new item to our dictionary - `"Exp": f"{x} ** {y} = {x ** y}" and commit the change using - `git commit -m "Updated calc function to include square root"`. Clearly, this message is incorrect as we've added an entry for *exponent* and not *square root*.

```
# Code snippet - basic Arithematic operations - calc.py
def calc(operator, x, y):
    return {
        "Add": f"{x} + {y} = {x + y}",
        "Sub": f"{x} - {y} = {x - y}",
        "Mul": f"{x} * {y} = {x * y}",
        "Div": f"{x} / {y} = {x / y}",
        "Floor": f"{x} // {y} = {x // y}",
        "Exp": f"{x} ** {y} = {x ** y}"
    }.get(operator, "Not found!")
```

Running a `git log` shows the last commit with the "bad" commit message.

![amend1]({static}/images/index6/amend1.jpg)

To fix the message, we simply run `git commit --amend -m "Updated calc function to include exponents"`. Running a `git log` now will show the updated commit message.

![amend2]({static}/images/index6/amend2.jpg)

Few **important** things to note - running a `git log` essentially shows us the *history* of commits that were made thus far. It also shows us the value of the unique hash associated with our commits. Notice that when we ran the --amend to fix our commit message, we did not add a new commit. Instead, we replaced the commit with the "bad" message, with the new commit. This is evident from the value of the hash associated with the two commits. They are not the same. What does this mean? Well, we just modified the git history by running the --amend command. This is fine as long as we are the only ones with access to the code base/repository in question or if no one else has pulled our commits before modifying the history. When working in a team wherein multiple developers are accessing the same repository, modifying the git history is risky as it could cause problems with their local repositories when they pull in our changes. Later in the post, we will look at ways to make corrections without modifying the git history.

In the previous example, we fixed a "bad" commit message. Now, what if we forgot to include an entire file before running our `git commit`? Let's say, we now create a .gitignore file in or repository and would like to include it in the previous commit. Once we add the files to staging, we can simply run `git commit --amend`. Running this command opens an interactive window that shows us the changes that will be committed. The commit message can also be modified if needed. Since we are not making any further changes, we can use `:wq` to exit. Following this, our .gitignore will be added to the last commit.

![amend3]({static}/images/index6/amend3.jpg)

Now, by running a `git log --stat` we can see the files that were part of the commit. Also, note that out commit has changed which means that we modified our git history.

![amend4]({static}/images/index6/amend4.jpg)

### Cherry picking with git
A very common issue that developers run into is making commits to an incorrect branch by forgetting to run the `git checkout <branchname>` command before committing their changes. So in our case, say we intended to make our last commit in the *new-feature* branch but accidentally ended up making the commits in *master*. Luckily, git provides a way to correct this easily.

Here's what our commit history looks like at the moment. What we want to do now is to move the "Updated calc function to include exponents" commit to the **new-feature** branch after which **master** will only have the "Initial commit".

![cp1]({static}/images/index6/cp1.jpg)

We will use the `git cherry-pick` command to copy this commit to the new branch. This command creates a new commit based on an existing one. Please note, that cherry-pick will <u>not</u> delete the original commit. 

To cherry-pick,
1. Copy the hash of the commit that needs to be copied over to the new branch (the first six characters will do)
2. Switch to the branch where the commit will be copied. In our case, we will run `git checkout new-feature` to switch from the *master* to the *new-feature* branch
3. Now, run the cherry-pick command to copy the commit - `git cherry-pick 7f5fa7`
4. Run a `git log` to confirm whether the branch was copied over

![cp2]({static}/images/index6/cp2.jpg)

Now that our commit has been copied over to the *new-feature* branch, we need to remove it from our *master* branch. To do this, we will use the `git reset` command. There are three types of reset's in git - soft, mixed (default) and hard. Let's try each one of them on our **master** branch to remove the commit. To run `git reset`, we will first need to copy the hash of the commit that was made <u>before</u> the one that needs to be deleted (The "Inital commit" in our case).

<b>Soft Reset</b>
To run a soft reset on our *master* branch, we will first need to switch to the *master* branch - `git checkout master`. Next, we will run `git reset --soft 2da509` on the branch. On running the soft reset, the *master* branch will no longer have the commit that was copied over to *new-feature*.

![reset1]({static}/images/index6/reset1.jpg)

However, if we now run a `git status` in *master*, we will see the changes from the branch that was removed, in the staging area. So, a soft reset will revert our branch to the specified commit but will keep the changes (associated with the commit that was removed), in our staging area. We, therefore, do not lose any of the changes.

![reset2]({static}/images/index6/reset2.jpg)

<b>Mixed Reset</b>
This is the default reset option provided by git. Again, we will run this command using the hash of the "Initial commit" - `git reset 2da509``. Like the soft reset, we do not lose any changes. However, the changes will now be in the working directory as opposed to the staging area.

![reset3]({static}/images/index6/reset3.jpg)

<b>Hard Reset</b>
Since our intent of running the reset was to completely get rid of the changes (in *master*) that were moved to the *new-feature* branch, neither the soft nor the mixed reset options served our purpose. We will now look at the hard reset option, which will revert tracked files (calc.py) to their original state and will leave untracked files (.gitignore) alone. So let's run `git reset --hard 2da509`. Notice that a `git status` only shows us the untracked files now.

![reset4]({static}/images/index6/reset4.jpg)

Removing an untracked file can be achieved by using the `git clean -df` command. The -df force deletes files and directories. Our *master* branch is now in its desired state.

![reset5]({static}/images/index6/reset5.jpg)

### Reverting to old commits
Let's assume that we ran the hard reset on our branch accidentally and we now need those changes back. Are we out of luck? Fortunately, no! Enter `git reflog`. The `git reflog` command shows us the entire history of all commits made in a particular branch. The commits are shown in the order of reference. Note that the reflog expiration date is 90 days by default. 

![reflog]({static}/images/index6/reflog.jpg)

Now let's say we want to revert to the changes before running our resets. We will need to copy the appropriate hash and run a `git checkout <hash>` command. Running this command on a hash as opposed to a branch name will put us in a detached HEAD state. At a hight level, this means that we are no longer checked out to the current branch (HEAD). Running a `git log` now will show both our commits.

![dhead]({static}/images/index6/d-head.jpg)

To save our changes, we will need to create a branch from the detached HEAD. So let's create one called *new-feature-backup* - `git branch new-feature-backup`. `git branch` will now show three branches. We can switch to the new backup branch and run a `git log` to confirm that our desired commits exist in the new branch.

![dhead]({static}/images/index6/d-head2.jpg)

Previously, we spoke about not modifying the git history if our commits have already been pulled by others. Let us now look at options to undo commits without changing the git history. This will ensure that when others pull in our changes, we will not be impacting their code base. We will use the `git revert` command will create a *new* commit to reverse changes from a previous commit.

Let us now undo the changes that we introduced in the "Updated calc function to include exponents" commit. To do that, copy the hash of that commit and run a `git revert <hash>`. This will open an interactive window. Since we are not making any other changes, let's save and exit using `:wq`.

![revert1]({static}/images/index6/revert1.jpg)

![revert2]({static}/images/index6/revert2.jpg)

Now, running a `git log` will show us a new commit that was created by reversing the previous commit which is exactly what we wanted. Also, notice that the hashes of the older commits are unchanged. We have therefore not modified the git history. If others were to now pull our changes, they will just be pulling in the new commit that will reverse the previous commit in their code base as well.

![revert3]({static}/images/index6/revert3.jpg)

Running a `git diff` on the two most recent branches using their hash will show us the exact changes that were undone.

![revert4]({static}/images/index6/revert4.jpg)