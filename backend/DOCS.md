<h1 align="center"> Trivia Game App Documentation </h1>

===============================================================================================================
- `Contributor`: **Adeyemi Simeon Adedoyin**

- `version`: **v1.0**

===============================================================================================================


# Trivia Game App
A simple API built around the REST principles for allowing Udacity employee and students relate by playing a simple knowledge quiz trivia game. The api uses the standard HTTP request codes and provides responses, as well as, errors using `json` format. 

## Setting up the Backend - Trivia API

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - It is highly recommeded you setup a virtual environment where you can install your dependencies, specific to the project. To setup a virtual environment, visit [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

This project uses the `Postgres Server DBMS`. 

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```


### Run the Server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute the following commands:

On Mac
```bash
export FLASK_APP=flaskr
export FLASK_DEBUG=true
flask run --reload
```

On Windows:
```bash
set FLASK_APP=flaskr
set FLASK_DEBUG=true
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.



## THE API ENDPOINTS
This api provides access to two main resources `categories` and `questions`. 

-----
### Base URL
- `http://127.0.0.1:5000` 
 *OR*
- `http://localhost:5000`
-----

### Endpoints
-----
#### Resource: `category`
-----

1. **`GET /api/v1.0/categories`**
-----
Fetches a list of categories in json format.
- *Request Arguments:* None
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the request, and `categories`, holding list of the fetched categories
- *HTTP Response Status Codes:* 
    - `200`, 'ok', 'successful fetch'
    - `404`, 'not found', no category in database yet

Example:
```bash
curl -X GET http://localhost:5000/api/v1.0/categories
```

Sample Response
```json
{
    "success": true,
    "categories": [
        {
            "id": 1,
            "type": "Cat1"
        },
        {
            "id": 2,
            "type": "Cat2"
        },
        {
            "id": 3,
            "type": "Cat3"
        }
    ]
}
```

-----
2. **`GET /api/v1.0/categories/:id`**
-----
Retrieves record of category with `id` specified, in json format.
- *Request Arguments:* `id`, the id of the category to fetch
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the request, and `category`, holding the fetched category data.
- *HTTP Response Status Codes:* 
    - `200`, 'ok', 'successful fetch'.
    - `404`, 'not found', category with the specified id not found in database.

Example:
```bash
curl -X GET http://localhost:5000/api/v1.0/categories/1
```

Sample Response
```json
{
    "success": true,
    "category": {
        "id": 1,
        "type": "Cat1"
    }
}
```


-----
3. **`POST /api/v1.0/categories`**
-----
Saves a category in the request body, in json format, to the database.
- *Request Arguments:* None
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the post request, and `id`, the id of the created category.
- *Sample Request Body:*
```json
{ "type": "category_name" }
```

- *HTTP Response Status Codes:* 
    - `201`, 'created', created successfully
    - `200`, 'ok', 'already existing, no need creating'
    - `422`, 'unprocessable', required body property `type` not present in request body'


Example:
```bash
curl -X POST http://localhost:5000/api/v1.0/categories
-H 'application/json' 
-d '{"type": "Cat1"}'
```

Sample Response
```json
{
    "success": true,
    "id": 1
}
```


-----
4. **`PATCH /api/v1.0/categories/:id`**
-----
Performs partial update of record of category with id of `id` specified in the parameter using the object specified in the request body (in json format).
- *Request Arguments:* `id`, the id of the category to update
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the request, and `updated`, holding the id of the updated category.
- *Sample Request Body:*
```json
{ "type": "Update_text" }
```

- *HTTP Response Status Codes:* 
    - `200`, 'ok', updated successfully
    - `404`, 'not found', category with the specified id not found in database.
    - `422`, 'unprocessable', required `type` property not in request body.
    - `400`, 'bad request', no body data sent.

Example:
```bash
curl -X PATCH http://localhost:5000/api/v1.0/categories/1
-H 'application/json' 
-d '{"type": "Cat1Update"}'
```

Sample Response
```json
{
    "success": true,
    "updated": 1
}
```


-----
5. **`DELETE /api/v1.0/categories/:id`**
-----
Deletes record of category with id of `id`.
- *Request Arguments:* `id`, the id of the category to delete
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the request, and `deleted`, holding the id of the deleted category.
- *HTTP Response Codes:* 
    - `200`, 'ok', deleted successfully
    - `404`, 'not found', category with the specified id not found in database.

Example:
```bash
curl -X DELETE http://localhost:5000/api/v1.0/categories/1
```

Sample Response
```json
{
    "success": true,
    "deleted": 1
}
```

-----
#### Resource: `question`
-----
1. **`GET /api/v1.0/questions?page=<page-numb>&currCat=<cat_id>`**
-----
Fetches page (`<page-numb>`) of questions belonging to the category with `<cat_id>`, in json format, where a page is 10 questions.
- *Request Arguments:* None
- *Query Parameters:* 
    - `page`: the page number to return, where a page contains maximum of 10 questions. Defaults to `1` if not specified.
    - `currCat`: the id of the category for which questions should be fetched. Defaults to `1` if not specified. 

- *Returns:* An object with five keys, `success`, with value of `True` or `False` holding the status of the request, `questions`, holding list of the fetched questions for the page specified, `total_questions`, holding a value corresponding to total no of questions found for the current category specified, `categories`, all categories, `current_category`, an instance of the current category specified.
- *HTTP Response Status Codes:* 
    - `200`, 'ok', 'successful fetch'
    - `404`, 'not found', no category in database yet, no category with the `<cat_id>` specified, no question for the current category yet.

Example:
```bash
curl -X GET http://localhost:5000/api/v1.0/questions?page=1&currCat=1
```

Sample Response
```json
{
    "success": true,
    "total_questions": 2,
    "categories": [
        {
            "id": 1,
            "type": "Cat1"
        },
        {
            "id": 2,
            "type": "Cat2"
        },
        {
            "id": 3,
            "type": "Cat3"
        }
    ],
    "current_category": {
        "id": 1,
        "type": "Cat1"
    },
    "questions": [
        {
            "question": "What is 2 x 2?",
            "answer": "4",
            "category": "Cat1",
            "difficulty": 2,
            "id": 4,
        },
        {
            "question": "What is 10 + 10?",
            "answer": "20",
            "category": "Cat1",
            "difficulty": 2,
            "id": 22,
        }
    ]
}
```


-----
2. **`GET /api/v1.0/questions/:id`**
-----
Retrieves record of question with `id` specified in json format.
- *Request Arguments:* `id`, the id of the category to fetch
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the request, and `question`, holding the fetched question data.
- *HTTP Response Status Codes:* 
    - `200`, 'ok', 'successful fetch'.
    - `404`, 'not found', question with the specified `id` not found in database.

Example:
```bash
curl -X GET http://localhost:5000/api/v1.0/questions/4
```

Sample Response
```json
{
    "success": true,
    "question": {
        "question": "What is 10 x 2?",
        "answer": "20",
        "category": "Cat1",
        "difficulty": 2,
        "id": 4,
    }
}
```


-----
3. **`POST /api/v1.0/questions`**
-----
Saves a new question, in the request body, in json format, to the database.
- *Request Arguments:* None
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the post request, and `id`, the id of the created question.
- *Sample Request Body:*
```json
{
    "question": "Your question", 
    "answer": "your answer", 
    "category": "category_type", 
    "difficulty": 2
}
```

- *HTTP Response Status Codes:* 
    - `201`, 'created', created successfully
    - `200`, 'ok', 'already existing, no need creating'
    - `422`, 'unprocessable', required body properties `question`, `answer`, `category` and `difficulty` not present in request body.


Example:
```bash
curl -X POST http://localhost:5000/api/v1.0/questions
-H 'application/json' 
-d '{"question": "What is the product of 10 and 4?", "answer": "40", "category": "Cat1", "difficulty": 2}'
```

Sample Response
```json
{
    "success": true,
    "id": 5
}
```


-----
4. **`DELETE /api/v1.0/questions/:id`**
-----
Deletes record of question with id of `id` specified in the request parameter.
- *Request Arguments:* `id`, the id of the question to delete
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the request, and `deleted`, holding the id of the deleted question.
- *HTTP Response Status Codes:* 
    - `200`, 'ok', deleted successfully
    - `404`, 'not found', question with the specified id not found in database.

Example:
```bash
curl -X DELETE http://localhost:5000/api/v1.0/question/1
```

Sample Response
```json
{
    "success": true,
    "deleted": 1
}
```

-----
5. **Seaching for Questions containing a given term:**
-----
**`POST /api/v1.0/questions?page<page-numb>`**

-----
Retrieves a page of all questions (in json format) belonging to the specified category with id `currentCategoryId`, containing the term `searchTerm` present in the request body from the database.

NOTE:
if `currentCategoryId` not included in the request body, searches returns all questions in all categories with the matched `searchTerm`.

- *Request Arguments:* None
- *Query Parameters:* 
    - `page`: (optional) indicating the page to fetch, where each page contains 10 questions. Defaults to `1` if `page` is not specified in the query parameter.

- *Returns*: An object with the keys, `success`, with value of `True` or `False` holding the status of the post request, `total_questions`, the total number of questions found matching the term, `current_category`, object representing the current category information, `questions`, maximum of 10 questions matched for a given page number first page (first ten) questions.

- *Sample Request body:* 
```json
{
    "searchTerm": "Term to search for", 
    "currentCategoryId": 3
}
```

- *HTTP Response Status Codes:* 
    - `200`, 'ok', questions fetched successfully.
    - `404`, 'not found', no question with matching term found for `currentCategoryId` specified, if no `currentCategoryId` specified, no question matching term found in all questions.
    - `422`, 'unprocessable', required body properties `searchTerm` is missing or the id supplied for the `currentCategoryId`, in request body does not exist.


Example:
```bash
curl -X POST http://localhost:5000/api/v1.0/questions
-H 'application/json' 
-d '{"searchTerm": "what is", "currentCategoryId": 3}'
```

Sample Response
```json
{
    "success": true,
    "total_questions": 2,
    "current_category": {
        "id": 3,
        "type": "Business"
    },
    "questions": [
        {
            "question": "What is Trade?",
            "answer": "Exchange of commodity for value",
            "category": "Business",
            "difficulty": 5,
            "id": 4,
        },
        {
            "question": "What is E-commerce?",
            "answer": "A digital market",
            "category": "Business",
            "difficulty": 2,
            "id": 8
        }
    ]
}
```


-----
6. **`GET /api/v1.0/categories/<cat_id>/questions?page=<page-numb>`**
-----
Retrieves all questions for category `<cat_id>`, in json format, where a page is maximum of 10 questions.
- *Request Arguments:* 
    - `cat_id`: the `id` of the category for which questions should be retrieved.
- *Query Parameters:* 
    - `page`: the page number to return, where a page contains maximum of 10 questions. Defaults to `1` if not specified.

- *Returns:* An object with five keys, `success`, with value of `True` or `False` holding the status of the request, `questions`, holding list of the paginated fetched questions for the page specified, `total_questions`, holding a value corresponding to total no of questions found for the current category specified, `categories`, all categories, `current_category`, an instance of the current category specified.

- *HTTP Response Codes:* 
    - `200`, 'ok', 'successful fetch'
    - `404`, 'not found', no category in database yet OR no category with the `<cat_id>` specified OR no question for the current category yet.

Example:
```bash
curl -X GET http://localhost:5000/api/v1.0/categories/1/questions?page=1
```

Sample Response
```json
{
    "success": true,
    "total_questions": 2,
    "categories": [
        {
            "id": 1,
            "type": "Cat1"
        },
        {
            "id": 2,
            "type": "Cat2"
        },
        {
            "id": 3,
            "type": "Cat3"
        }
    ],
    "current_category": {
        "id": 1,
        "type": "Cat1"
    },
    "questions": [
        {
            "question": "What is 2 x 2?",
            "answer": "4",
            "category": "Cat1",
            "difficulty": 2,
            "id": 4,
        },
        {
            "question": "What is 10 + 10?",
            "answer": "20",
            "category": "Cat1",
            "difficulty": 2,
            "id": 22,
        }
    ]
}
```


-----
7. **`POST /api/v1.0/quizzes`**
-----
Retrieves a new question not previously asked from the database for the specified `quiz_category` object in the request body.
- *Request Arguments:* None
- *Query Parameters:* None
- *Returns:* An object with two keys, `success`, with value of `True` or `False` holding the status of the post request, and `question`, the new question fetched. It returns `None` for the question if all questions in the category have been previously retrieved. 

- *Sample Request body:*
```json
{
    "previous_questions": [1, 3, 4], 
    "quiz_category": {
        "id": 1,
        "type": "Cat1"
    }
}
```

- *HTTP Response Status Codes:* 
    - `200`, 'ok', question fetched successfully OR questions available for the specified quiz category, but all have been previously asked.
    - `422`, 'unprocessable', required body properties `previous_questions` and `quiz_category` object not present in request body.


Example:
```bash
curl -X POST http://localhost:5000/api/v1.0/questions
-H 'application/json' 
-d '{"question": "What is the product of 10 and 4?", "answer": "40", "category": "Cat1", "difficulty": 2}'
```

Sample Response
```json
{
    "success": true,
    "id": 5
}
```
-----

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Setting up the Frontend - Trivia API
The frontend code was written using Reactjs. 

### Install Dependencies
1. **Nodejs**: Make sure that you already have `Nodejs` installed, from their official website
2. **NPM**: Also, make sure `npm`, Node Packege Manager, is also installed. This comes with latest versions of Nodejs installation.

To test whether you already have `Nodejs` and `npm` installed, Open command prompt (for Windows users) or Terminal (For Mac users) and run the commands shown below, if the versions are shown, then you already have them installed.

```bash
node --version
npm --version
```

3. **React Dependencies**: Once `Nodejs` and `npm` are confirmed installed, to install the frontend dependencies, from within the `./frontend` directory of this project, execute the following commands:

```bash
npm install
```

### Run the Local React Server

To start the local React Server, from within the `./frontend` directory, execute the following commands:

```bash
npm start
```