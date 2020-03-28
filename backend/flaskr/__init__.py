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

    ''' @Complete: Set up CORS. Allow '*' for origins. Delete the sample route
        after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    ''' @Complete: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Controll-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Controll-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    ''' @Complete: Create an endpoint to handle GET requests
        for all available categories.
    '''
    @app.route('/categories')  # default GET method
    def categoriesGet():
        response = {
          "success": True,
          "categories": []
        }

        categories = Category.query.all()

        for category in categories:
            response['categories'].append(category.type)
        return jsonify(response)

    ''' @Complete: Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories.

        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of the screen
        for three pages. Clicking on the page numbers should
        update the questions.
    '''
    @app.route('/questions')
    def questionsGet():
        page = request.args.get('page', 1, type=int)
        # Calling the "questionsHelper" with page and no category
        response = questionsHelper(page=page, category=None)
        return jsonify(response)

    ''' This method will be used by other Question related endpoints.
    '''
    def questionsHelper(page=1, category=None, search=None):
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        # Creating the response object
        response = {
            "success": True,
            "status": 200,
            "questions": [],
            "totalQuestions": 0,
            "categories": [category.type for category in Category.query.all()],
            "current_category": ''
        }

        ''' Creating the query object that will be modified depending on the
            arguments passed when calling the method.
        '''
        query = Question.query

        # Filter by category
        if category is not None:
            query = query.filter(Question.category == '{}'.format(category))
            response['current_category'] = category

        # Filtering by a search term. This is case insensitive (ilike)
        if search is not None:
            query = query.filter(Question.question.ilike(
                '%{}%'.format(search)))

        questions = query.order_by(Question.difficulty).all()
        # Abort if the page is longer than the total questions
        if len(questions) < start:
            abort(404)

        response['totalQuestions'] = len(questions)

        # This line creates the question array that will be returned
        formatted_questions = [question.format() for question in questions]
        # In case of pagination, this line will select the related items
        response['questions'] = formatted_questions[start: end]

        return response

    ''' @Complete: Create an endpoint to DELETE question using a question ID.

        TEST: When you click the trash icon next to a question, the question
        will be removed. This removal will persist in the database and when
        you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def questionDelete(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        # If the id doesn't exist, the endpoint will return 404 Not Found error
        if question is None:
            abort(404)

        try:
            question.delete()
            return jsonify({
                    "success": True,
                    "question": question_id
            })

        except:
            abort(422)

    ''' @Complete: Create an endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.

        TEST: When you submit a question on the "Add" tab,
        the form will clear and the question will appear at the end of
        the last page of the questions list in the "List" tab.
    '''

    ''' This enpoint will be used for two scenarios:
            1. Searching
            2. Adding questions
    '''
    @app.route('/questions', methods=['POST'])
    def questionsPOST():
        body = request.get_json()

        searchTerm = body.get('searchTerm', None)
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        ''' If the request contains a "searchItem" element, then
            the endpoint will return the questions that contain
            that "searchItem"
        '''
        if searchTerm:
            try:
                return jsonify(questionsHelper(page=1, search=searchTerm))
            except:
                abort(422)

        # Otherwise the endpoint will handle the request as a "Create Question"
        else:
            newQuestion = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )

        try:
            newQuestion.insert()
            return jsonify({"success": True})
        except:
            abort(422)

    ''' @complete: Create a POST endpoint to get questions based on
        a search term. It should return any questions for whom the search term
        is a substring of the question.

        TEST: Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        Try using the word "title" to start.
    '''

    ''' Complete, this is part of the "questionsPOST" method a both adding a
        new questions and searching for a question send a POST request.
        Both send the same result format.
    '''

    ''' @Complete: Create a GET endpoint to get questions based on category.

        TEST: In the "List" tab / main screen, clicking on one of the
        categories in the left column will cause only questions of that
        category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def categoriesGetQuestions(category_id):
        page = request.args.get('page', 1, type=int)
        response = questionsHelper(page=page, category=category_id)
        return jsonify(response)

    ''' @Complete: Create a POST endpoint to get questions to play the quiz.
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

            # Creating the query object
            question_query = Question.query
            category = Category.query.filter(
                Category.type == quiz_category_type).one_or_none()

            ''' If the category exists, the query will filter the questions
                by that category. Otherwise, it will use all the categories.
            '''
            if category:
                question_query = question_query.filter(
                    Question.category == '{}'.format(category.id))

            ''' This line will query only the questions that are not present
                in the previous_questions array so users are not presented with
                the same question again
            '''
            questions = question_query.filter(
                ~Question.id.in_(previous_questions)).all()

            # The game will end if the aren't questions or if the user did 5.
            if len(questions) == 0 or len(previous_questions) >= 5:
                return jsonify({})

            # This line will select the next question randomnly
            random_id = random.randint(0, len(questions)-1)
            response = {
                "question": questions[random_id].format()
            }
            return jsonify(response)
        except:
            abort(422)

    ''' @Complete: Create error handlers for all expected errors
        including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Item not found"
        }), 404

    @app.errorhandler(422)
    def unable_to_process(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Something went wrong"
        }), 422

    return app
