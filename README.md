

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AdityaK0/API.git
cd API
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```

- On Linux/macOS:
  ```bash
  source venv/bin/activate
  ```

- On Windows:
  ```bash
  venv\Scripts\activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver  (if your localhost port(8000) is already busy u can try other too  )
```

The server will start at:

```
http://127.0.0.1:8000/
```

## API Documentation

To test and explore available endpoints, use the Postman documentation below:

[Postman Collection Documentation](https://documenter.getpostman.com/view/36760108/2sB2qahgPk)

This includes all available API routes, request types, and expected responses.

## Authentication



1. create account
2. login can be done using username/phonenumber and password
3. obtain token via login if enviroment variable is intialized it will automatically set the value into the postman enviroment



