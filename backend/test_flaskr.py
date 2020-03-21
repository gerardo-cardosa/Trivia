import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

# References:
# 1.- Postgres Dialect: https://github.com/zzzeek/sqlalchemy/blob/master/test/dialect/postgresql/test_dialect.py


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_user = 'postgres'
        self.database_password = "#Palomis1"
        self.database_path = "postgres://{}:{}@{}/{}".format(self.database_user,self.database_password,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.newQuestion = {
            'question' : 'This is a new question',
            'answer' :'this is an answer',
            'category' :1,
            'difficulty' :'5'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # Test for the questions endpoints
    def test_get_questions(self): 
        res = self.client().get('/questions')
        data = json.loads(res.data)

        questions =  Question.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertTrue(data['categories'])
        self.assertFalse(data['currentCategory'])
        self.assertEqual(data['currentCategory'], '')
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(data['totalQuestions'], len(questions))

    def test_pagination_get_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertLessEqual(len(data['questions']), 10)

    def test_400_pagination_get_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'Tom'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertLessEqual(len(data['questions']), 10)

    def test_search_non_existent_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'asdffdsa'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)        

    def test_get_questions_category(self):
        # Science category
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertEqual(data['questions'][0]['category'], 1)

    def test_get_questions_category_page(self):
        # Science category
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)



    def test_add_question(self):
        questionsBefore = len(Question.query.all())
        res = self.client().post('/questions', json=self.newQuestion)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        questionsAfter = len(Question.query.all())
        self.assertEqual(questionsBefore + 1, questionsAfter)

    def test_400_add_question(self):
        self.newQuestion['category'] = 2002
        questionsBefore = len(Question.query.all())

        res = self.client().post('/questions', json=self.newQuestion)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

        questionsAfter = len(Question.query.all())
        self.assertEqual(questionsBefore, questionsAfter)

    def test_delete_question(self):
        questions = Question.query.all()
        total_questions_before = len(questions)
        latest_question = questions[total_questions_before -1]
        res = self.client().delete('/questions/{}'.format(latest_question.id))   
        data = json.loads(res.data)
        total_questions_after = len(Question.query.all()) 

        # assertions
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['question'], latest_question.id)
        self.assertEqual(total_questions_before - 1, total_questions_after)

    
    
    def test_400_delete_question(self):
        total_questions_before = len(Question.query.all())
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)
        total_questions_after = len(Question.query.all())

        # assertions
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(total_questions_before, total_questions_after)


    # Test for categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        categories = Category.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), len(categories))


    # Test for quizzes
    def test_get_quizz_all(self):
        post_data = {
            "previous_questions" : [],
            "quiz_category" :{
                "id" : 1,
                "type" : "" 
            }
        }
        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)

        # assertions
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])


    def test_get_quizz_category(self):
        post_data = {
            "previous_questions" : [],
            "quiz_category" :{
                "id" : 1,
                "type" : "Science" 
            }
        }
        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)

        # assertions
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])


    # Reference - https://treyhunner.com/2016/04/how-to-loop-with-indexes-in-python/
    def test_get_quizz_second_question(self):
        science_questions =  Question.query.filter(Question.category == '1').all()
        science_questions.pop()
        # Will add all the science questions with the exception of the last one. 
        # The quizzes method should return a new question different from the "previous_questions"
        post_data = {
            "previous_questions" : [question.id for idx, question in enumerate(science_questions)  ],
            "quiz_category" :{
                "id" : 1,
                "type" : "Science" 
            }
        }

        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)

        # assertions
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertTrue( data['question']['id'] not in post_data['previous_questions'] )

    def test_no_more_questions(self):
        science_questions =  Question.query.filter(Question.category == '1').all()
        # Will add all the science questions with the exception of the last one. 
        # The quizzes method should return a new question different from the "previous_questions"
        post_data = {
            "previous_questions" : [question.id for idx, question in enumerate(science_questions)  ],
            "quiz_category" :{
                "id" : 1,
                "type" : "Science" 
            }
        }

        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)

        # assertions
        self.assertEqual(res.status_code, 200)
        self.assertFalse(data.get('question', False))


    # This test should return a value as it will ignore the wrong category
    def test_get_quizz_wrong_category(self):
        post_data = {
            "previous_questions" : [],
            "quiz_category" :{
                "id" : '1000000',
                "type" : "Not a Category" 
            }
        }
        res = self.client().post('/quizzes', json=post_data)
        data = json.loads(res.data)

        # assertions
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()