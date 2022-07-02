import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
from settings import user_name, database_name
from dotenv import load_dotenv

load_dotenv()


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}@{}/{}'.format(
            user_name, 'localhost:5432', self.database_name
        )
        setup_db(self.app, self.database_path)

        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            "question": "Who is the tallest man to ever live?",
            "answer": "King Solomon",
            "category": 4,
            "difficulty": 1
        }

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # def test_get_paginated_questions(self):
    #     res = self.client().get("/questions")
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data["questions"]))

    # def test_404_sent_requesting_beyond_valid_page(self):
    #     res = self.client().get("/questions?page=1000")
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    # def test_delete_questions(self):
    #     res = self.client().delete("/questions/5")
    #     data = json.loads(res.data)
    #     question = Question.query.filter(Question.id == 5).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 5)
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data["questions"]))
    #     self.assertEqual(question, None)

    # def test_422_if_question_does_not_exist(self):
    #     res = self.client().delete("/questions/1000")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")

    # def test_create_new_question(self):
    #     res = self.client().post("/questions", json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["created"], 25)

    # def test_405_if_question_creation_not_allowed(self):
    #     res = self.client().post('/questions/20', json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "method not allowed")    

    # def test_get_questons_by_searchTerm(self):
    #     res = self.client().post('/questions/search', json={'searchTerm': 'alive'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)

    # def test_get_questons_by_category(self):
    #     res = self.client().get("/categories/3/questions")
    #     data = json.loads(res.data)
    #     questions = Question.query.filter(Question.category == 3).all()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data["questions"]))

    # def test_404_if_question_does_not_exist(self):
    #     res = self.client().get("/categories/&%/questions")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")


    def test_play_quizzes(self):
        res = self.client().post("/quizzes")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_404_if_quizzes_not_playing(self):
        res = self.client().post("/quizzes")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")    



    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()