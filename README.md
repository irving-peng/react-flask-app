# Installation needed(required to run the app)
## Git

install git by running this command in your terminal 
```bash
winget install --id Git.Git -e --source winget
```
you can also visit this [link](https://git-scm.com/download/win) for installation

then, clone this repository to your local directory 
```bash
git clone https://github.com/irving-peng/react-flask-app.git
```
## Python and pip libaries
install python3 or higher on this [website](https://www.python.org/downloads/windows/)

and install the needed package for this app through pip

```bash
pip install flask
```
```bash
pip install flask_cors
```
```bash
pip install matplotlib
```
```bash
pip install pandas
```
## Install React and required libraries
first, download node.js by visiting this [link](https://nodejs.org/en/)

then, navigate to the React directory
```bash
cd my-app
```
install npm
```
npm install
```
# Running the App
Running the app required running both the front end and the backend
## Flask (backend) Set up
cd to the root directory (if you are in my-app directory)
```bash
cd ..
```
run app.py 
```bash
python app.py
```
leave the app.py running
## React (frontend) Set up
open another terminal window and follow these steps:

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
Now, you should be able to see the app running on [http://localhost:3000/](http://localhost:3000/) 🎉

*Above are all the steps you need to take to run the app locally. 
# Uploading new data
for uploading new data or updating existing data, go to the public folder
```bash
cd my-app/public
```
*data.csv*: This CSV is used for generating the market demand plot

*hub_item.csv*: This CSV is used for generating all the items number in the form on Home page

*sale_price.csv*: this CSV is used for generating the price table

*sell_table*: this CSV is used for generating the sales table

# For adding data
Simply download the CSV file from the repository, and add rows to the CSV **with the same format** (E.g. Date, ItemID, Quantity).

After adding rows to the CSV, replace the existing CSV with the updated CSV file. **DO NOT CHANGE THE NAME OF THE CSV FILE**.

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

## For first time deploying:   
1. change the proxy in package.json to the URL for the Heroku app
2. repeat the commit and push process


*view the URL shown in the output from
```bash
git push heroku master(main)
```
*packages, libraries, and dependencies are listed in requirement.txt
