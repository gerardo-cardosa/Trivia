import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @Complete: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*":{"origins":"*"}})

  '''
  @Complete: Use the after_request decorator to set Access-Control-Allow
  '''
# SO - https://stackoverflow.com/a/27939619
# Udacity - https://classroom.udacity.com/nanodegrees/nd0044/parts/838df8a7-4694-4982-a9a5-a5ab20247776/modules/afbae13a-a91a-4d5e-9f98-4fe13c415f7a/lessons/37cec828-a108-4013-96e7-645495aed9a0/concepts/56008375-e597-42db-92e9-60e40b0c99b9?bounced=1584417281829
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Controll-Allow-Headers','Content-Type, Authorization')
    response.headers.add('Access-Controll-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  @Complete: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories') # default GET method
  def categoriesGet():
    response = {
      "success": True,
      "categories": []
    }

    categories = Category.query.all()

    for category in categories:
      response['categories'].append(category.type)
    return jsonify(response)


  '''
  @Complete: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def questionsGet():
    page = request.args.get('page', 1, type=int)
    try:
      response = questionsHelper(page=page, category=None)
      return jsonify(response)
    except:
      abort(422)
        
  # This method will be used by other Question related endpoints. 
  def questionsHelper(page=1, category=None, search=None):
    page_zise = 10
    start = (page - 1)* page_zise
    end = start + page_zise

    response ={
      "success":True,
      "status": 200,
      "questions": [],
      "totalQuestions": 0,
      "categories" : [ category.type for category in Category.query.all()],
      "currentCategory" : ''
    }

    query = Question.query

    # Filter by category
    if not category == None:
      query = query.filter(Question.category == '{}'.format(category))
      response['currentCategory'] = category
    
    if not search == None:
      query = query.filter(Question.question.ilike('%{}%'.format(search)))

    questions = query.order_by(Question.id).all()
    response['totalQuestions'] = len(questions)

    formatted_questions = [question.format() for question in questions]
    response['questions'] = formatted_questions[start: end ]
    
    return response

  '''
  @Complete: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def questionDelete(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()

    if question == None:
      abort(404)

    try:
      question.delete()
      return jsonify({
        "success":True,
        "question": question_id
      })

    except:
      abort(422)
    
  '''
  @Complete: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def questionsPOST():
    body = request.get_json()

    searchTerm = body.get('searchTerm', None)
    question = body.get('question', None)
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)

    if searchTerm:
      try:
        return jsonify(questionsHelper(page=1, search=searchTerm ))
      except:
        abort(422)
      

    else:
      newQuestion = Question(
        question = question,
        answer = answer,
        category = category,
        difficulty = difficulty
      )

      try:
        newQuestion.insert()
        return jsonify({"success": True})
      except:
        abort(422)
      

  '''
  @complete: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # Complete, this is part of the questionsPOST method a both adding a new questions
  # and searching for a question send a POST request. Both send the same result format

  '''
  @Complete: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def categoriesGetQuestions(category_id):
    page = request.args.get('page', 1, type=int)

    try:
      response = questionsHelper(page=page, category=category_id)
      return jsonify(response)
    except:
      abort(422)
    

  '''
  @Complete: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    try:
      body = request.get_json()
      previous_questions = body.get('previous_questions', None)
      quiz_category = body.get('quiz_category', None)
      quiz_category_id = None
      quiz_category_type = None

      if quiz_category:
        quiz_category_id = quiz_category.get("id", None)
        quiz_category_type = quiz_category.get("type", None)

      question_query = Question.query
      category = Category.query.filter(Category.type == quiz_category_type).one_or_none()

      if category:
        question_query = question_query.filter(Question.category == '{}'.format(category.id))


      questions = question_query.filter(~Question.id.in_(previous_questions)).all()

      if len(questions) == 0 or len(previous_questions) >= 5:
        return {}

      random_id = random.randint(0, len(questions)-1) 
      response = {
        "question": questions[random_id].format()
      }
      return jsonify(response)
    except:
      abort(422)
    

  '''
  @Complete: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(422)
  def unable_to_process(error):
    return jsonify({
      "success": False,
      "error" : 422,
      "message": "Something went wrong"
    }),422

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Item not found"
    }),404
  
  return app

    