web: gunicorn group_discussion.wsgi --log-file -
worker: python manage.py calculate_groups
worker: python manage.py check_for_inactivity