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

### Requirements


## API Documentation

### Questions
General Path:  "/questions"

#### GET
This will return all the questions in set of 10 items. 

To paginate, a 'page=int' query parameter may be added to get other pages. 
"/questions?page=2"

##### Returned value
This method will return a json with the following structure:
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


#### POST

##### Search
When sending a json payload containing the property "searchTerm", this method will return a list of questions
based on the searched term. If no questions were found, the returned object will contained an empty "questions" list. 

##### Add
If the method is called and instead contains the below payload, a new question will be added. 
{
    "question" = "Who completed this quizz?"
    "answer" = "Me"
    "category" = "1"
    "difficulty" = "4"
}

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