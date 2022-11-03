# Setup

pip install -r requirements.txt

# Run Script

python manage runserver

celery -A konigle worker -l info -P eventlet

celery -A konigle beat -l info 