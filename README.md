# Trivia
This is a trivia app - Second project of the Full Stack Web Developer Udacity nanodigree. 

This app is composed of two parts:
1. The front end
2. The back end

## The Fronend 

The `./frontend` is a React based website. Follow the next instructions to run it

### Requirements

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

#### Running in development mode

```bash
npm start
```

### The Website

#### List of questions
 The main webpage will show the user a list of categories and the related questions. If no 
 category was selected, the list will show all the questions in difficulty order. 

#### Questions
 Each item will display the question, the difficulty, an icon related to the category and
 a button to show the answer to that question. 

#### Add
 In this page, the user can add new questions. 

#### Play
 This is a small quizz game. A user can select a topic and the game will start. 
 The quizz will consist of 5 questions related to the category select. 
 If "All" was selected, the questions can be from any category. 

 The game won't show the same question during the quizz and the questions will come in 
 random order. 


## The Backend
The `./backend` is a Flask based python app. 

### Requirements (Taken from the Udacity Full Stack Web Development Course - Project Trivia)

#### Local Database

Postgres is suggested. [Download](https://www.postgresql.org/)

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

#### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

#### Database configuration in App

Add user, password and database name to the variables located in:
`backend/models.py`


#### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

``` Windows
$env:FLASK_APP="flaskr"
$env:FLASK_ENV="development"
flask run

```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.


## API Reference

### Getting Started

Base URL: This app can be run locally and is not hosted as a base URL. The backend is 
hosted at: http://127.0.0.1:5000/ 
This is set as a proxy in the frontend configuration. 

### Error Handling

Errors are returned as JSON objest in the below format:
```
{
    "success": False,
    "eror": 404,
    "message": "Not found"
}
```
The API will return two kinds of errors:

1. 404: Not found
2. 422: Not Processable

### Endpoints

#### GET /questions

1. General

    This endpoint will return a result object containing:

        1. status
        2. success value
        3. a list of categories
        4. current category
        5. total number of questions
        6. a list of questions. 

The list of questions is paginated in groups og 10. 
The endpoint includes a request argument to choose the page number, starting from 1. 

2. Sample: curl http://127.0.0.1/5000/questions

{
    "status": 200,
    "success": true,
    "categories": ["Science" , "art"],
    "currentCategory": "",
    "totalQuestions": 1,
    "questions": [
        {
        "answer": "Escher",
        "category": "2",
        "difficulty": 1,
        "id": 16,
        "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
        }
    ]      
}


#### POST /questions

1. General

    1. This endpoint will search books when seding a JSON object containing "searchTerm". If no questions were found, the returned object will contained an empty "questions" list.
    2. Creates a new questions using the submitted question, answer, category, difficulty. 

2. Sample: curl http://127.0.0.1/5000/questions -X POST -H "Content-type: applicationjson" -d '{
    "question" = "Who completed this quizz?",
    "answer" = "Me",
    "category" = "1",
    "difficulty" = "4"
}'

If something goes wrong, like sending an invalid category, the method will return a 422 error. 

#### Delete
Path: "/questions/<int:id>"

If the deletion was successfull, the endpoint will retun a 200 with this json { "success": true}
However, if something goes wrong, it will return a 422 error. 
And if the question id doesn't exists, a 404 error will be return.

### Categories
Path "/categories"

#### Get
This endpoint will get all the available categories in a json like:
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "success": true
}

#### Questions from categories
Path: "/categories/<int:id>/questions"

This endpoint will return all the questions related to a specific category. The return object will be like what the Questions Get method returns. 
If an invalid id is given, the returned object will have an empty questions list. 

### Quizzes
Path: "/quizzes'

#### Post
This method will require a json as follows:
{
    "previous_questions": [],
    "quiz_category" : {
        "id":"1",
        "type":"Science"
    }
}

The "previous_questions" contains the id of the questions already asked. 
The "quiz_category" porperty, will be the reference for the kind of questions the endpoint will return. In this case, it would be Science. 

##### Response
This endpoint will return a random question from the category selected. If no category was selectec, this will take all the questions in consideration. 
The response will contain a question that wasn't asked before. 

The returned object has this form:
{
    "question": {
       'id': 1,
            'question': "Is this a hard question?",
            'answer': "yes",
            'category': "1",
            'difficulty': 5
        }
      }


## Reference used:
SO - https://stackoverflow.com/a/27939619
Udacity - https://classroom.udacity.com/nanodegrees/nd0044/parts/838df8a7-4694-4982-a9a5-a5ab20247776/modules/afbae13a-a91a-4d5e-9f98-4fe13c415f7a/lessons/37cec828-a108-4013-96e7-645495aed9a0/concepts/56008375-e597-42db-92e9-60e40b0c99b9?bounced=1584417281829
Python Randon numbers - https://www.geeksforgeeks.org/random-numbers-in-python/
Python in line for loop - https://stackoverflow.com/a/27411654
Python value in array - https://stackoverflow.com/a/7571665
        