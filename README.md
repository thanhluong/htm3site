## First time clone
Please create a new virtual environment and install all the packages in the requirements.txt file.

Run the following command:
```
python manage.py makemigrations
python manage.py migrate
```

To create a new superuser, run:
```
python manage.py createsuperuser
```

Make sure you can access the admin page at `localhost:8000/admin`

To start the app in LAN, run:
```
python manage.py runserver 0.0.0.0:8000
```
