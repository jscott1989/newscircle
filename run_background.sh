while true
do 
    python manage.py calculate_groups
    python manage.py check_for_inactivity
    sleep 10
done