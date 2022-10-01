import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""

    # def tearDownClass(self):
    #     """Executed once after all tests"""
    #     self.db.drop_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # ------- CATEGORY RESOURCE TESTS HERE ------

    def test_get_categories(self):
        res = self.client().get('/api/v1.0/categories')
        data = json.loads(res.data)

        categories_count = Category.query.count()

        if categories_count > 0:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['categories'])
            self.assertGreater(len(data['categories']), 0)
        else:
            self.assertNotEqual(res.status_code, 200)

    def test_404_sent_on_get_req_when_no_category_in_db(self):
        res = self.client().get('/api/v1.0/categories')
        data = json.loads(res.data)

        categories_count = Category.query.count()

        if categories_count == 0:
            self.assertEqual(res.status_code, 404)
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], 404)
            self.assertTrue(data['message'])
            self.assertTrue('not found' in data['message'])

    def test_post_categories(self):
        count_before_post = Category.query.count()

        res = self.client().post('/api/v1.0/categories',
                                 json={'type': 'new_category'})
        data = json.loads(res.data)

        count_after_post = Category.query.count()

        if 'message' in data:  # already existing category
            self.assertEqual(count_before_post, count_after_post)
            self.assertTrue(data['message'])
            self.assertTrue('existing' in data['message'])

        else:  # if category not already existing in db
            # find database for the newly added category
            added_category = Category.query.filter(
                Category.type == 'new_category').one_or_none()

            self.assertEqual(res.status_code, 201)
            self.assertGreater(count_after_post, count_before_post)
            self.assertTrue(added_category)  # added_category not None

    def test_422_sent_on_post_categories_when_body_has_no_required_data(self):
        res = self.client().post('/api/v1.0/categories', json={'fake': 'data'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertTrue(data['message'])
        self.assertTrue('unprocessable' in data['message'])

    def test_get_categories_by_id(self):
        res = self.client().post('/api/v1.0/categories',
                                 json={'type': 'category2'})
        data = json.loads(res.data)

        id = int(data['id'])

        res2 = self.client().get(f'/api/v1.0/categories/{id}')
        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)
        self.assertTrue(data2['success'])
        self.assertEqual(data2['category']['type'], 'category2')

    def test_delete_categories_by_id(self):
        # ---- TEST PREPS ---
        res = self.client().post('/api/v1.0/categories',
                                 json={'type': 'category3'})
        data = json.loads(res.data)
        id = int(data['id'])

        count_before_delete = Category.query.count()

        res2 = self.client().delete(f'/api/v1.0/categories/{id}')
        data2 = json.loads(res2.data)

        count_after_delete = Category.query.count()

        self.assertEqual(res2.status_code, 200)
        self.assertTrue(data2['success'])
        self.assertEqual(int(data2['deleted']), id)
        self.assertLess(count_after_delete, count_before_delete)

    def test_404_sent_on_get_categories_with_non_existing_id(self):
        res = self.client().get(f'/api/v1.0/categories/-5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])
        self.assertTrue('not found' in data['message'])

    def test_404_sent_on_delete_categories_with_non_existing_id(self):
        res = self.client().delete(f'/api/v1.0/categories/-5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])
        self.assertTrue('not found' in data['message'])

    def test_404_sent_on_patch_categories_with_non_existing_id(self):
        res = self.client().patch(f'/api/v1.0/categories/-5',
                                  json={'type': 'updated_category'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])
        self.assertTrue('not found' in data['message'])

    def test_422_sent_on_patch_category_with_type_property_not_in_req_body(self):
        res_post = self.client().post(
            '/api/v1.0/categories', json={'type': 'category4'})
        data_post = json.loads(res_post.data)
        id = int(data_post['id'])

        res = self.client().patch(
            f'/api/v1.0/categories/{id}', json={'illegal': 'illegal value'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertTrue(data['message'])
        self.assertTrue('unprocessable' in data['message'])

    def test_400_sent_on_patch_category_without_req_body(self):
        res_post = self.client().post(
            '/api/v1.0/categories', json={'type': 'category4'})
        data_post = json.loads(res_post.data)
        id = int(data_post['id'])

        res = self.client().patch(
            f'/api/v1.0/categories/{id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertTrue(data['message'])
        self.assertTrue('bad request' in data['message'])

    def test_patch_category_by_id_for_proper_update(self):
        # --- TEST DATA PREPS ----
        # posting a new category to be updated later
        new_category = {'type': 'category4'}
        post_res = self.client().post(
            '/api/v1.0/categories', json=new_category)

        post_res_data = json.loads(post_res.data)
        posted_id = int(post_res_data['id'])
        # --- TEST DATA PREPS

        patch_res = self.client().patch(
            f'/api/v1.0/categories/{posted_id}', json={'type': 'updated_category4'})
        patch_res_data = json.loads(patch_res.data)
        updated_id = int(patch_res_data['updated'])

        # Fetch the record of category id sent for update
        category = Category.query.filter(
            Category.id == posted_id).one_or_none()

        if category is not None:
            self.assertEqual(posted_id, updated_id)
            self.assertEqual(category.type, 'updated_category4')

    # ------- QUESTION RESOURCE TESTS HERE ------
    def test_get_paginated_questions(self):
        # ------ TEST DATA PPREPS -------
        # create new category
        res_post_cat = self.client().post(
            '/api/v1.0/categories', json={'type': 'category5'})
        data_post_cat = json.loads(res_post_cat.data)

        # add new question for the category
        question = {
            'question': 'how are you?',
            'answer': 'fine',
            'category': 'category5',
            'difficulty': 3}

        res_post_question = self.client().post('/api/v1.0/questions', json=question)
        data_post_question = json.loads(res_post_question.data)
        # ------ End Data Preps -------

        res = self.client().get(
            f'/api/v1.0/questions?page=1&currCat={data_post_cat["id"]}')
        data = json.loads(res.data)

        cat_count = Category.query.count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), cat_count)
        self.assertEqual(data['current_category']['type'], 'category5')
        self.assertGreaterEqual(int(data['total_questions']), 1)
        self.assertTrue(len(data['questions']))

    def test_404_sent_on_get_req_when_no_question_in_db(self):
        # empty all existing questions in db first
        existing_ques = Question.query.all()
        for que in existing_ques:
            que.delete()

        # then try to get questions, expecting results to contain 404 (no question)
        res = self.client().get('/api/v1.0/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])
        self.assertTrue('not found' in data['message'])

    def test_get_question_by_id(self):
        question = {
            'question': 'What is 2 x 2?',
            'answer': '4',
            'category': 'category5',
            'difficulty': 1}
        res_post = self.client().post('/api/v1.0/questions', json=question)
        data_post = json.loads(res_post.data)
        id = int(data_post['id'])

        res2 = self.client().get(f'/api/v1.0/questions/{id}')
        data2 = json.loads(res2.data)

        self.assertEqual(res2.status_code, 200)
        self.assertTrue(data2['success'])
        self.assertEqual(data2['question']['question'], question['question'])

    def test_delete_question_by_id(self):
        question = {
            'question': 'What is 2 x 2?',
            'answer': '4',
            'category': 'category5',
            'difficulty': 1}
        res_post = self.client().post('/api/v1.0/questions', json=question)
        data_post = json.loads(res_post.data)
        id = int(data_post['id'])

        count_before_delete = Question.query.count()

        res2 = self.client().delete(f'/api/v1.0/questions/{id}')
        data2 = json.loads(res2.data)

        count_after_delete = Question.query.count()

        self.assertEqual(res2.status_code, 200)
        self.assertTrue(data2['success'])
        self.assertEqual(int(data2['deleted']), id)
        self.assertLess(count_after_delete, count_before_delete)

    def test_404_sent_on_get_question_with_non_existing_id(self):
        res = self.client().get(f'/api/v1.0/questions/-5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])
        self.assertTrue('not found' in data['message'])

    def test_post_questions(self):
        question = {
            'question': 'What is 4 x 4?',
            'answer': '16',
            'category': 'category6',
            'difficulty': 1}

        res = self.client().post('/api/v1.0/questions', json=question)
        data_res = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data_res['success'], True)
        self.assertTrue(data_res['id'])

    def test_422_sent_on_post_questions_with_missing_required_body_fields(self):
        # Required Fields: 'question', 'answer', 'category', 'difficulty'
        question_with_missing_req_fields = {
            'question': 'What is 4 x 4?',
            'answer': '16'}

        res = self.client().post('/api/v1.0/questions', json=question_with_missing_req_fields)
        data_res = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data_res['error'], 422)
        self.assertTrue('unprocessable' in data_res['message'])

    def test_get_results_on_post_questions_with_search_term(self):
        # ---- TEST DATA PREPS ----
        new_category = {
            'type': 'cat7'
        }

        question = {
            'question': 'What is 10 + 10?',
            'answer': '20',
            'category': new_category['type'],
            'difficulty': 1}

        # Post a new category
        res_cat = self.client().post('/api/v1.0/categories', json=new_category)
        res_cat_data = json.loads(res_cat.data)

        # Post a new question belonging to the newly added category
        res = self.client().post('/api/v1.0/questions', json=question)
        res_data = json.loads(res.data)
        # ------- END PREPS ---

        if 'success' in res_cat_data and 'success' in res_data:  # OnSuccess
            searchData = {'searchTerm': 'what is',
                          'currentCategoryId': res_cat_data['id']}

            search_results = self.client().post('/api/v1.0/questions', json=searchData)
            search_results_data = json.loads(search_results.data)

            self.assertEqual(search_results.status_code, 200)
            self.assertEqual(search_results_data['success'], True)
            self.assertGreater(len(search_results_data['questions']), 0)

        else:
            self.assertTrue(False)

    def test_422_sent_on_search_term_with_non_existing_currentCategoryId(self):
        searchData = {'searchTerm': 'what is',
                      'currentCategoryId': -10000}

        search_results = self.client().post('/api/v1.0/questions', json=searchData)
        search_results_data = json.loads(search_results.data)

        self.assertEqual(search_results.status_code, 422)
        self.assertEqual(search_results_data['success'], False)
        self.assertEqual(search_results_data['error'], 422)
        self.assertTrue(
            'unprocessable' in search_results_data['message'])

    def test_404_sent_on_search_term_not_found(self):
        searchData = {'searchTerm': 'kililklkllkosksoosksosk'}

        search_results = self.client().post('/api/v1.0/questions', json=searchData)
        search_results_data = json.loads(search_results.data)

        self.assertEqual(search_results.status_code, 404)
        self.assertEqual(search_results_data['success'], False)
        self.assertEqual(search_results_data['error'], 404)
        self.assertTrue(
            'not found' in search_results_data['message'])

    def test_get_all_questions_for_category_with_specified_id(self):
        # ---- TEST PREPARATIONS ---
        new_category = {
            'type': 'cat9'
        }

        question = {
            'question': 'What is 1 + 1?',
            'answer': '2',
            'category': new_category['type'],
            'difficulty': 1}

        # Post a new category
        res_cat = self.client().post('/api/v1.0/categories', json=new_category)
        res_cat_data = json.loads(res_cat.data)

        # Post a new question belonging to the newly added category
        res = self.client().post('/api/v1.0/questions', json=question)
        res_data = json.loads(res.data)
        # ------- END PREPARATIONS ---

        id = res_cat_data['id']
        res_ques = self.client().get(f'/api/v1.0/categories/{id}/questions')
        res_ques_data = json.loads(res_ques.data)

        self.assertEqual(res_ques.status_code, 200)
        self.assertEqual(res_ques_data['success'], True)
        self.assertEqual(
            res_ques_data['current_category']['type'], new_category['type'])
        self.assertGreater(res_ques_data['total_questions'], 0)
        self.assertGreater(len(res_ques_data['questions']), 0)

    def test_404_sent_on_get_all_ques_for_cat_with_non_existing_catID(self):
        id = -10000
        res_ques = self.client().get(f'/api/v1.0/categories/{id}/questions')
        res_ques_data = json.loads(res_ques.data)

        self.assertEqual(res_ques.status_code, 404)
        self.assertEqual(res_ques_data['success'], False)
        self.assertEqual(res_ques_data['error'], 404)
        self.assertTrue(res_ques_data['message'])
        self.assertTrue('not found' in res_ques_data['message'])

    def test_404_sent_on_get_all_ques_for_catID_with_no_questions(self):
        # ----- PREPS -------
        new_category = {'type': 'cat10'}

        # Post a new category
        res_cat = self.client().post('/api/v1.0/categories', json=new_category)
        res_cat_data = json.loads(res_cat.data)

        # Delete all existing questions
        existing_questions = Question.query.all()

        for que in existing_questions:
            que.delete()
        # ----- END PREPS ------

        id = res_cat_data['id']
        res_ques = self.client().get(f'/api/v1.0/categories/{id}/questions')
        res_ques_data = json.loads(res_ques.data)

        self.assertEqual(res_ques.status_code, 404)
        self.assertEqual(res_ques_data['success'], False)
        self.assertEqual(res_ques_data['error'], 404)
        self.assertTrue(res_ques_data['message'])
        self.assertTrue('not found' in res_ques_data['message'])

    def test_get_quiz_post_quizzes(self):
        # ---- TEST PREPARATIONS ---
        new_category = {
            'type': 'cat9'
        }

        question1 = {
            'question': 'What is 2 + 2?',
            'answer': '4',
            'category': new_category['type'],
            'difficulty': 1}

        question2 = {
            'question': 'What is 3 + 3?',
            'answer': '6',
            'category': new_category['type'],
            'difficulty': 1}

        # Post a new category
        res_cat = self.client().post('/api/v1.0/categories', json=new_category)
        res_cat_data = json.loads(res_cat.data)

        # Post a new question belonging to the newly added category
        res_q1 = self.client().post('/api/v1.0/questions', json=question1)
        res_q1_data = json.loads(res_q1.data)

        res_q2 = self.client().post('/api/v1.0/questions', json=question2)
        res_q2_data = json.loads(res_q2.data)
        # ------- END PREPARATIONS ---

        body_data = {
            'previous_questions': [res_q1_data['id']],
            'quiz_category': {'id': res_cat_data['id'], 'type': new_category['type']}
        }

        quiz_fetch_res = self.client().post('/api/v1.0/quizzes', json=body_data)
        quiz_fetch_res_data = json.loads(quiz_fetch_res.data)

        self.assertTrue(quiz_fetch_res.status_code, 200)
        self.assertEqual(quiz_fetch_res_data['success'], True)
        self.assertTrue(quiz_fetch_res_data['question'])

    def test_422_sent_on_post_quizzes_with_missing_required_body_properties(self):
        body_data = {
            'invalid': 'invalid'
        }
        quiz_fetch_res = self.client().post('/api/v1.0/quizzes', json=body_data)
        quiz_fetch_res_data = json.loads(quiz_fetch_res.data)

        self.assertTrue(quiz_fetch_res.status_code, 422)
        self.assertEqual(quiz_fetch_res_data['success'], False)
        self.assertEqual(quiz_fetch_res_data['error'], 422)
        self.assertTrue('unprocessable' in quiz_fetch_res_data['message'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
