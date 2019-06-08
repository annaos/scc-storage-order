# lsdf-portal

lsdf-portal is a Django-Project to management storage requests by [Large Scale Data Facility (LSDF)](https://www.scc.kit.edu/forschung/11843.php).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Django.

```bash
pip install Django==2.2.1
```

Install Shibboleth

```bash
pip install git+https://github.com/Brown-University-Library/django-shibboleth-remoteuser.git
```

## Usage

```bash
python manage.py runserver # run server
python manage.py migrate # run all migrations
python manage.py createsuperuser # create super user for /admin

```

Under [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) you find admin part for database.

Under [http://127.0.0.1:8000/order](http://127.0.0.1:8000/order) you find management system for storage requests.

## License
This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License
