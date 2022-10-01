from crypt import methods
from email import message
import json
import os
import re
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# ==============================================
# SEE MY DOCUMENTATION IN 'DOCS.md' FILE
# ==============================================


def paginate_questions(request, all_questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in all_questions]
    new_book_list = questions[start:end]
    return new_book_list


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={f'{re.escape(r"*/api/*")}': {'origins': '*'}})
    # CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-headers',
                             'Content-Type, Accept, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        # response.headers.add('Access-Control-Allow-Origin', r'*/api/*')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/v1.0')
    def index():
        return jsonify({
            'success': True,
            'message': 'Welcome User'
        })

    @app.route('/api/v1.0/categories', methods=['GET', 'POST'])
    def get_categories():
        if request.method == 'GET':
            categories = Category.query.order_by(Category.type).all()

            if len(categories) == 0 or categories is None:
                abort(404)

            return jsonify({
                'success': True,
                # 'categories': [cat.type for cat in categories]
                'categories': [cat.format() for cat in categories]
            })

        elif request.method == 'POST':
            body = request.get_json()
            if 'type' not in body:
                abort(422)

            existing = Category.query.filter(
                Category.type.ilike(body.get('type'))).one_or_none()

            if existing is not None:  # category already existing
                return jsonify({
                    'success': True,
                    'message': f'Already existing category',
                    'id': existing.id
                }), 200

            category = Category(type=body.get('type'))
            category.insert()  # into database

            return jsonify({
                'success': True,
                'id': category.id
            }), 201

    # ------------------------------------------------------------------------
    # GET /api/v1.0/category/<cat_id>: Retrieves category <cat_id> record
    # PATCH /api/v1.0/category/<cat_id>: Performs partial update of category with id <cat_id>
    # DELETE /api/v1.0/category/<cat_id>: Deletes category <cat_id> record
    # ------------------------------------------------------------------------
    @app.route('/api/v1.0/categories/<int:cat_id>', methods=['GET', 'PATCH', 'DELETE'])
    def request_category(cat_id):
        category = Category.query.filter(
            Category.id == cat_id).one_or_none()

        if category is None:
            abort(404)

        if request.method == 'GET':
            return jsonify({
                'success': True,
                'category': category.format()
            })

        elif request.method == 'PATCH':
            body = request.get_json()
            if body is not None:
                if 'type' not in body:
                    abort(422)
            else:
                abort(400)

            cat_type = body.get('type')
            category.type = cat_type

            category.update()

            return jsonify({
                'success': True,
                'updated': category.id,
            })

        elif request.method == 'DELETE':
            category.delete()

            return jsonify({
                'success': True,
                'deleted': category.id,
            })

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
    # ------------------------------------------------------------------------------
    # GET /api/v1.0/questions?page=<val>:
    # Retrieves 10 questions per page specified for the current category
    # Query Parameters:
    # ?page: specifies which page to show, if question number spans multiple pages
    # -----------------------------------------------------------------------------
    @app.route('/api/v1.0/questions')
    def get_questions():
        # Fetch all categories order-by type
        curr_cat_id = request.args.get('currCat', 1, type=int)

        categories = Category.query.order_by(Category.type).all()

        if len(categories) == 0 or categories is None:
            abort(404)

        # Pick the first category in db in alphabetical order
        # as default category
        current_category = Category.query.filter(
            Category.id == curr_cat_id).one_or_none()

        if current_category is None:
            current_category = categories[0]

        # Fetch all questions belonging to current category
        questions = Question.query.filter(
            Question.category == current_category.type).order_by(Question.question).all()
        formatted_questions_set = paginate_questions(request, questions)

        if len(questions) == 0 or len(formatted_questions_set) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': formatted_questions_set,
            'total_questions': len(questions),
            'categories': [category.format() for category in categories],
            'current_category': current_category.format()
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    # ----------------------------------------------------------------
    # GET /api/v1.0/questions/<id>: get the details of question with id <id>
    # ----------------------------------------------------------------
    @app.route('/api/v1.0/questions/<int:que_id>', methods=['GET', 'DELETE'])
    def delete_question(que_id):
        question = Question.query.filter(
            Question.id == que_id).one_or_none()

        if question is None:
            abort(404)

        if request.method == 'GET':
            return jsonify({
                'success': True,
                'question': question.format()
            })

        elif request.method == 'DELETE':
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question.id
            })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    # ------------------------------------------------------------------------
    # POST /api/v1.0/questions: Stores a new question supplied in request body into db
    #      data: {
    #           "question":"my question",
    #           "answer": "my answer",
    #           "category": "category",
    #           "difficulty": 5
    #       }
    # E.g.
    # curl -X POST https://localhost:5000/api/v1.0/questions
    # -H "Content-Type:application/json"
    # -D '{"question":"my question", "answer": "my answer",
    # "category": "category","difficulty": 5}'
    # ------------------------------------------------------------------------
    @app.route('/api/v1.0/questions', methods=['POST'])
    def post_question():
        body = request.get_json()
        avail_fields = body.keys()

        if 'searchTerm' in avail_fields:
            searchTerm = body.get('searchTerm')
            current_cat = None
            found_questions = None

            if 'currentCategoryId' in avail_fields:
                current_cat = Category.query.filter(
                    Category.id == int(body.get('currentCategoryId'))).one_or_none()

                if current_cat is None:
                    abort(422)

                found_questions = Question.query.filter(
                    Question.category == current_cat.type, Question.question.ilike(f'%{searchTerm}%')).all()

            else:
                # If no category is specified, find all questions
                # containing term
                found_questions = Question.query.filter(
                    Question.question.ilike(f'%{searchTerm}%')).all()

            if len(found_questions) == 0 or found_questions is None:
                abort(404)

            paginated_questions_set = paginate_questions(
                request, found_questions)

            return jsonify({
                'success': True,
                'questions': paginated_questions_set,
                'total_questions': len(found_questions),
                'current_category': current_cat.format()
            })

        elif ('question' in avail_fields and 'answer' in avail_fields
                and 'category' in avail_fields and 'difficulty' in avail_fields):

            que = body.get('question')
            ans = body.get('answer')
            cat = body.get('category')
            diff = body.get('difficulty')

            question = Question(question=que, answer=ans,
                                category=cat, difficulty=diff)

            question.insert()

            return jsonify({
                'success': True,
                'id': question.id,
            }), 201  # created

        else:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    # IMPLEMENTED Together with POST /api/v1.0/questions for new post,
    # since POST /api/v1.0/questions endpoint already exist, implementing another one
    # will lead to conflicting routes.

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    # ------------------------------------------------------------------------
    # GET /api/v1.0/categories/<cat_id>/questions:
    # Retrieves all questions for category <cat_id>
    # ------------------------------------------------------------------------
    @app.route('/api/v1.0/categories/<int:cat_id>/questions')
    def get_quest_by_categpry(cat_id):
        category = Category.query.filter(Category.id == cat_id).one_or_none()

        questions = Question.query.filter(
            Question.category == category.type).all()

        if len(questions) == 0:
            abort(404)

        paginated_questions_set = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': paginated_questions_set,
            'total_questions': len(questions),
            'current_category': category.format(),
        })

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
    # -----------------------------------------------------------------------------
    # POST /api/v1.0/quizzes:
    # Retrieves a new randomized question in the current category
    # ----------------------------------------------------------------------------
    @app.route('/api/v1.0/quizzes', methods=['POST'])
    def post_quizzes():
        body = request.get_json()
        if 'previous_questions' in body and 'quiz_category' in body:
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')

            new_question_pool = None
            if quiz_category['id'] == 0:  # when 'all' is specified as category
                new_question_pool = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()

            else:  # where quiz_category is selected
                new_question_pool = Question.query.filter(
                    Question.category == quiz_category['type'], Question.id.notin_(previous_questions)).all()

            if len(new_question_pool) == 0 or new_question_pool is None:
                return jsonify({
                    'success': True,
                    'question': None
                })

            # Select a random question from list of unused questions
            new_random_question = random.choice(new_question_pool)

            return jsonify({
                'success': True,
                'question': new_random_question.format()
            })

        else:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    # -----------------------------------------------------------------------------
    # Error Handlers
    # ----------------------------------------------------------------------------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app
