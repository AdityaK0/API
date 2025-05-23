

Follow these steps to run the project locally.

```bash
git clone https://github.com/AdityaK0/API.git
cd API


python -m venv venv
For Linux: source venv/bin/activate
For Windows: venv\Scripts\activate


pip install -r requirements.txt


DATABASE_URL=sqlite:///db.sqlite3  # or PostgreSQL URI

python manage.py makemigrations

python manage.py migrate


python manage.py createsuperuser


python manage.py runserver
