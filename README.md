# Salestock Assessment
## Installation

prefer to create new virtual environment to isolate python lib from your system
use python2.7.

install all requirements by running:
```
pip install -r requirements.txt
```

after successfully install all requirements start development server by running:
```
python manage.py runserver
```
login with:

username: nasa

pasword: adminnasa

#### Category Page
point your browser to http://127.0.0.1:8000/categories/
browseable API for categories will be shown.

if you didn't want to use browseable API, you can send header with Content-Type: application/json or just append ?format=json at the url

### Product page
point your browser to http://127.0.0.1:8000/products/
browseable API for products will be shown.

if you didn't want to use browseable API, you can send header with Content-Type: application/json or just append ?format=json at the url

### Unit test
enter salestock directory
run unit test with command:
```
python manage.py test
```

### Functional test
enter salestock directory
then run with command:
```
python manage.py test functional_tests --liveserver=localhost:8000
```
functional test will using selenium firefox webdriver, screenshot of the test will be saved inside functional_tests/screendumps


