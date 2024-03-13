This is project is a simple web app that implements the basic CRUD operations for students, courses, and instructors

To run:
    Navigate to project folder and run the following commands (windows):
    py -m venv environment
    environment\Scripts\activate
    pip install flask databases
    set FLASK_APP=app
    set FLASK_ENV=development
    python init_db.py
    flask run

Based on a template from https://github.com/do-community/flask_blog