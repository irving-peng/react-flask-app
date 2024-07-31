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


package, library, and dependencies listed in requirement.txt
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

For Deployment to Heroku:
    1. heroku login
    2. git init
    3. heroku create
    4. git status
    5. rm -Force .git (in react-directory)
    6. git add .
    7. git commit
    8. git push heroku master(main)

    (For the first time)
    1*. change the proxy in package,json to the url for the heroku webiste
    2* repeat the commit and push process

    view webiste with the URL shown in the output from heroku
