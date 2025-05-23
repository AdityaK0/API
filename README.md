

Follow these steps to run the project locally.

```bash
git clone https://github.com/AdityaK0/API.git
cd API


python -m venv venv
For Linux: source venv/bin/activate
For Windows: venv\Scripts\activate


pip install -r requirements.txt




python manage.py makemigrations

python manage.py migrate


python manage.py runserver


To test  please go through the documentation : https://documenter.getpostman.com/view/36760108/2sB2qahgPk

