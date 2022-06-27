# Django test exercise

### This realizes test task:

Let we have a Django project.
With models:
```
Rental
 - name

Reservation
  -rental(FK)
  -checkin(date)
  -checkout(date)
```

Add the view with the table of Reservations with "previous reservation ID".
A previous reservation is a reservation that is before by date the current one into the same
rental.

Example:
```
Rental-1
(1, 2022-01-01, 2022-01-13)
(2, 2022-01-20, 2022-02-10)
(3, 2022-02-20, 2022-03-10)

Rental-2
(4, 2022-01-02, 2022-01-20)
(5, 2022-01-20, 2022-02-11)

|Rental_name|ID|Checkin    |Checkout  |Previous reservation  ID|
|rental-1   |1 | 2022-01-01|2022-01-13| -                      |
|rental-1   |2 | 2022-01-20|2022-02-10| 1                      |
|rental-1   |3 | 2022-02-20|2022-03-10| 2                      |
|rental-2   |4 | 2022-01-02|2022-01-20| -                      |
|rental-2   |5 | 2022-01-20|2022-01-11| 4                      |
```
Also, add tests.

## Setup guide
(tested on Python3.9)
- create .env file in root folder, put there those keys
```
DJANGO_SECRET_KEY="<your_django_secret_key_here>"
DEBUG_MODE=True
```
- create python venv ```python -m venv venv```
- activate venv ```source venv/bin/activate```
- install deps ```pip install -r requirements.txt```
- run db migrations ```python manage.py migrate```
- load test data ```python manage.py loaddata rental reservation```
- run dev server ```python manage.py runserver 0.0.0.0:8000```
- go to ```http://localhost:8000/```
- to run tests ```python manage.py test```
