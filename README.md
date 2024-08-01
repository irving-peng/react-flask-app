# Installation needed
## Git
install git by running this command in your terminal
```bash
winget install --id Git.Git -e --source winget
```
or visit the website
[title](https://git-scm.com/download/win)
then, clone this repository to your local directory 
```bash
git clone https://github.com/irving-peng/react-flask-app.git
```
## Python and pip libaries
install python3 or higher on this [website](https://www.python.org/downloads/windows/)
install needed package for this app through pip
```bash
pip install flask flask_cors matplotlib pandas
```
## Install React and required libraries
first, download node.js by visiting this [link](https://nodejs.org/en/)
first, navigate to the react directory
```bash
cd my-app
```
install npm
```
npm install
```




# Flask (backend) Set up
run app.py 
```bash
python app.py
```

# React (frontend) Set up

## Build and Run

navigate to my-app directory first

```bash
cd my-app
```

build command

```bash
npm run build
```

run command

```
npm start
```

# Creating virtual environment on windows:
```bash
python -m venv venv
```
For activate virtual environment
```bash
venv/Scripts/activate
```
For deactivate
```bash
deactivate
```

# For Deployment to Heroku:
    
    ```bash
    heroku login
    ```
    ```bash
    git init
    ```
    ```bash
    heroku create
    ```
    ```bash
    git status
    ```
    ```bash
    rm -Force .git (in react-directory)
    ```
    ```bash
    git add .
    ```
    ```bash
    git commit
    ```
    ```bash
    git push heroku master(main)
    ```

    # For the first time    
    1. change the proxy in package,json to the url for the heroku webiste
    2. repeat the commit and push process


    *view website with the URL shown in the output from Heroku

    *package, library, and dependencies listed in requirement.txt
