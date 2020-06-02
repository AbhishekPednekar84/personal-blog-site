Title: Continuous Deployment with Travis CI and DigitalOcean
Date: 2020-06-01 21:00
Category: CI/CD
Tags: CI/CD
Slug: travis-digitalocean
Authors: Abhishek Pednekar
Summary: Setting up a CI/CD pipeline with Travis CI and DigitalOcean
Cover: /static/images/gradient-texture-cubes.jpg

In this post, you will set up a Continuous Deployment (CD) pipeline using Travis CI and DigitalOcean. CD is a release process that involves running automated tests on a piece of software followed by deployment of the software if all the tests pass. There are several tools available to run a CD pipeline. Travis CI, CircleCI and Buddy Works are few of the popular ones. Since this post aims to be language-agnostic, the focus will only be on the deployment piece of the equation and not the testing aspects.

The example in this post will involve using **Travis CI** to deploy a React.js application on a **DigitalOcean** droplet. The same techniques can, however, be extended to any language or framework with some slight tweaks. This example will be using a Windows 10 local machine.

## Pre-requisites

1. A local `git` installation (if you are planning to use the same application as this post)
2. A [GitHub](https://github.com/) account
3. A [DigitalOcean](https://www.digitalocean.com/) account or an account with any IAAS provider
4. A [Travis CI](https://travis-ci.org/) account having access to your GitHub repositories. Travis CI will let new users sign up with their GitHub credentials.
5. Windows Subsystem for Linux (WSL) enabled if using Windows. Please refer to [this video](https://youtu.be/xzgwDbe7foQ) to enable and set up WSL on your Windows 10 machine. 
6. An application to deploy

This post will not go into details of the initial setup on the DigitalOcean droplet. Please refer to the below article in case you are setting up a virtual private server for the first time. 
- [Deploying a Flask application on a Linux server - Part I](https://www.codedisciples.in/linux-vps-deployment1.html)


## The demo application

If you are planning to use the demo application, you may fork this [repository](https://github.com/AbhishekPednekar84/react-demo-app). The readme file contains steps to set up the application locally.

Alternately, you can use any application and make sure it is available in a public (if you are using the free tier of Travis CI) repository on GitHub.  

## Travis CI

Once signed up, you will need to provide Travis CI access to the GitHub repository of the application you are planning to deploy. This option is available under the account settings.

![travis]({static}/images/index22/travis.jpg)

You will also be using the Travis CI command line later on to encrypt the private key that will be used to log into the DigitalOcean droplet. To install the Travis CLI locally, you will run the following commands in WSL.

```
sudo apt install ruby
sudo apt install ruby-dev
sudo apt install libffi-dev
sudo apt install make
sudo apt install gcc

gem install travis --version '1.8.10'
```

If using OS X, you will need to install [HomeBrew](https://brew.sh/) and run the following commands in a terminal.

```
sudo brew install ruby

sudo gem install travis -v 1.8.10
```

You will use the CLI a subsequent section.

**Note**: At the time of publishing this post, the latest version of the Travis CLI is `v1.8.11`. However, there are some known issues in this version concerning the `travis encrypt-file` command on Windows. All working suggestions indicated downgrading to `v1.8.10`. However, these issues might well be fixed depending on when you are reading this post.

## Creating a new user on the Linux server

Travis CI will talk to the droplet via public key authentication. To enable that you will first need to create a new user on the droplet. 

Assuming that the initial setup on the server is done (please refer the pre-requisites section), you can log in to the droplet with the `sudo` user and create a new user called `travis`.

```
# Login with sudo user
ssh <your sudo username>@<your droplet ip address>

# Create a new user
sudo adduser --disabled-password --gecos "" travis
```

Next, you will need to create a folder on the server to which the code will be deployed via CD. The folder can be created in an accessible location on the server. In this case, it will be a folder named `demo` in the `home` directory of the `sudo` user. The `travis` user will be made the owner of the `demo` directory.

```
mkdir ~/<sudo user>/demo

sudo chown -R travis:travis ~/<sudo user>/demo
```

Once the permissions are set, you will need to log in as the `travis` user and create the pre-requisite directories and files for the public key authentication to be successful. 

```
# Switch to the travis user
sudo su travis

# Create the .ssh directory for the user
mkdir ~/.ssh

# Provide 700 permissions to the directory
chmod 700 ~/.ssh

# Create the authorized_keys file in .ssh
cd .ssh
touch authorized_keys

# Provide 600 permissions to the file
chmod 600 ~/.ssh/authorized_keys
```

Keep this terminal session open for now as the public key needs to be copied into the `authorized_keys` file.

## Travis CI configuration
Travis CI looks for a file called `.travis.yml` in the git repository before running the build. This configuration file contains all the steps that Travis CI needs to follow while running the build and should be created in the project root folder. You can use any text editor of your choice. This example uses `nano`.

```
sudo nano .travis.yml
```

Add the following code to the `.travis.yml` file.

```
language: node_js
node_js:
  - "12.16"
addons:
  ssh_known_hosts: <your droplet ip address>
before_install:
  - cd client
install:
  - npm install
script:
  - "true"
after_success:
  - npm run build
  - cd ..
  - bash ./deploy.sh
```

To save and close the file with its current name, use `Ctrl + X`, `Y` and `Enter`.

**Explanation**:

- Since this example uses a React.js project, the language will be `node_js`
- Next, you will need to specify the version of `node.js`
- The `ssh_known_hosts` key will specify the ip address of your droplet
- Since all the client dependencies of the project are in a folder named `client`, you will first `cd` into the `client` folder before installing the dependencies. 
- The `install` shared key will contain the `npm install` command that will install all the client libraries specified in `package.json`
- Travis CI looks for tests by default while executing a pipeline. To skip tests, you will need to pass a `true` value to the `script` shared key
- Once the project dependencies are installed, you can then create the production build by running the `npm run build` command. This will create a sub-folder called `build` in the `client` folder and place all the deployable binaries in the `build` folder
- Finally, you will run a bash script called `deploy.sh` to deploy the code to the server. You will create this file in a subsequent section

## Public key authentication
With the server primed for deployment and the initial `.travis.yml` ready, you will now need to ensure that Travis CI can communicate with the server. Navigate to the local folder containing the application code. Remember to use WSL if you are on Windows. Run the below command to generate the public and private keys in the folder.

```
ssh-keygen -t rsa -N "" -f travis_rsa
```

The `-N ""` argument creates the keys without a `passphrase`. Although the `passphrase` is optional, it is recommended that you specify one for added security. Now, you will see a private key - `travis_rsa` and a public key - `travis_rsa.pub` in the project folder. `cat` the contents of the public key and copy it to the `authorized_keys` file that you created in the previous section.

```
cat travis_rsa.pub
```

Using the Travis CLI that you installed earlier, you will now encrypt the private key. To do so, run the following command. 

```
travis encrypt-file travis_rsa --add
```

This will create a `travis_rsa.enc` file which is an encrypted version of the private key. It is ok to check this file into source control. You can now delete the original private key (`travis_rsa`) as that **should not** be checked into source control.

```
sudo rm travis_rsa
```

In addition to creating the `.enc` file, the above command will also modify the `before_install` shared key in `.travis.yml`. This command will decrypt the private key so that it can be used by Travis CI to connect to the droplet.

```
before_install:
  - openssl aes-256-cbc -K $encrypted_0ddd2445e49f_key -iv $encrypted_0ddd2445e49f_iv
    -in travis_rsa.enc -out travis_rsa -d
```

To complete the public key authentication setup, you will need to add some additional commands to the `before_install` shared key. These should be familiar from the earlier server setup.

This is what the final `before_install` section should look like.

```
before_install:
  - openssl aes-256-cbc -K $encrypted_0ddd2445e49f_key -iv $encrypted_0ddd2445e49f_iv
    -in travis_rsa.enc -out travis_rsa -d
  - chmod 600 travis_rsa
  - mv travis_rsa ~/.ssh/id_rsa
  - cd client
```

## Deployment script
Finally, you will need to create `bash` script called `deploy.sh` with the below code. This script should reside in the root folder of the project. Again, the example will use `nano` to create the file.

```
sudo nano deploy.sh
```

Add the following code to `deploy.sh` and use `Ctrl + X`, `Y` and `Enter` to save the file and exit.

```
set -xe

if [ $TRAVIS_BRANCH == 'master' ] ; then
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_rsa

  rsync -a client/build/ travis@<droplet ipaddress>:/home/<sudo user>/demo/client
  rsync -a server/ travis@<droplet ipaddress>:/home/<sudo user>/demo/server
else
  echo "Not deploying, since the branch isn't master."
fi
```

**Explanation**:

- The script uses an environment variable called `TRAVIS_BRANCH` provided by Travis CI to determine current branch. The script will run only if there is a `push` to the `master` branch
- Next, the script will start an `ssh-agent` instance to connect to the droplet and use the private key to authenticate into the server
- The script uses the `rsync` command to move the necessary files and folders to the server. The arguments to the `rsync` command will vary depending on how your project is structured. For more details on `rsync`, refer to [this gist](https://gist.github.com/AbhishekPednekar84/3e60603d6da8e0d296d138f69340d3f7)

## Deploying the application

You are now ready to push the changes to the remote repository. Here is what the final project structure looks like.

```
.
├── ./.travis.yml
├── ./README.md
├── ./assets
│   └── ./assets/chuck.gif
├── ./client
│   ├── ./client/package-lock.json
│   ├── ./client/package.json
│   ├── ./client/public
│   └── ./client/src
├── ./deploy.sh
├── ./server
│   ├── ./server/package-lock.json
│   └── ./server/server.js
├── ./travis_rsa.enc
└── ./travis_rsa.pub
```

However, before you do that, you will need to determine whether you would like the pipeline to run as soon as you push your changes or if you would like to trigger a manual build. You can set the desired option on the settings page of your project on Travis CI.

![travis2]({static}/images/index22/travis2.jpg)

Finally, you can `push` to the remote repository using `git push origin master` assuming you are working directly on the `master` branch.

If you set your build to start automatically on every push, you will now see a build for the project queued up on the Travis CI dashboard page.

![travis3]({static}/images/index22/travis3.jpg)

Clicking on the build number will take you to the build page where you can view the log as the build progresses. The log below shows the build progressing through each step defined in the `.travis.yml` file. If the build is successful, it will exit with a `0` code.

![travis4]({static}/images/index22/travis4.jpg)

You should now see the files in the `demo` folder that you created earlier on the server.

![demo]({static}/images/index22/demo.jpg)

## Next steps

As next steps, you can install and configure Nginx on the droplet to serve your application on the web. Please refer to the [React.js deployment](https://www.codedisciples.in/react-deployment.html) article for more details.