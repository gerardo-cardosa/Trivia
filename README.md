# Trivia
This is a trivia app - Second project of the Full Stack Web Developer Udacity nanodigree. 

This app is composed of two parts:
1. The front end
2. The back end

## The fron end 

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


