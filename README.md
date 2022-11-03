# Setup

## Install Enviroment
pip install -r requirements.txt

# Run Script

run command **python manage runserver**     

run worker: **celery -A konigle worker -l info -P eventlet**     

run beat: **celery -A konigle beat -l info**      