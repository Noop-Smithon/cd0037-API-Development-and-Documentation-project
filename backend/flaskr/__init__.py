import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Question, Category
import random


QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    # CORS(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.all()
        retrieved_categories = {category.id: category.type for category in categories}
        return jsonify({
            'success': True,
            'categories': retrieved_categories,
            })
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    QUESTIONS_PER_PAGE = 10
    def paginate_questions(request, questions):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in questions]
        current_questions = questions[start:end]
        print(current_questions)
        return current_questions

    @app.route("/questions", methods=["GET"])
    def retrieve_questions():
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.type).all()
        current_questions = paginate_questions(request, questions)
        print(len(questions))

        
        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "categories":{category.id: category.type for category in categories},
                "current_category": None
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            return jsonify(
                {
                    'success': True,
                    'deleted': question_id,
                    'questions': current_questions,
                    'total_questions': len(questions)
                }
            )

        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question',None)
        new_answer = body.get('answer',None)
        new_category = body.get('category',None)
        new_difficulty = body.get('difficulty',None)

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty
            )
            question.insert()


            return jsonify(
                {
                    "success": True,
                    "created": question.id
                }
            )

        except:
            abort(405)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        
        try:
            search_term = request.get_json()['searchTerm']
            results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_result = [result.format() for result in results]


            return jsonify(
                {
                    "success": True,
                    "questions": formatted_result,
                    "total_questions": len(results),
                    "current_category": None
                }
            )

        except:
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/categories/<int:id>/questions", methods=["GET"])
    def retrieve_by_category(id):

        try:

            questions = Question.query.filter(Question.category == id).all()
            formatted_question = [question.format() for question in questions]
            
            return jsonify(
                {
                    "success": True,
                    'questions': formatted_question,
                    'total_questions': len(questions),
                    'current_category': None
                }
            )

        except:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quizzes():
        try:
            data = request.get_json()
            previous_questions = data.get('previous_questions')
            quiz_category = data.get('quiz_category')['id']

            if quiz_category:
                questions = Question.query.filter(Question.category == quiz_category).all()
            else:
                questions = Question.query.all()

            random_questions = random.choice(questions)
            
            return jsonify(
                {
                    'success': True,
                    'question': random_questions.format()
                }
            )

        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request"
            }
        ), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": "resource not found"
            }
        ), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify(
            {
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }
        ), 405


    @app.errorhandler(422)
    def unprocessable(error):    
        return jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                }
            ), 422

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

