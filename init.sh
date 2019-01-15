# Only for MacOS:
# brew install nginx
# brew install uwsgi --with-python
# mkdir -p /usr/local/etc/nginx/sites-{enabled,available}
# ln -s  /Users/snipghost/django/BlackJack/blackjack_nginx.conf /usr/local/etc/nginx/sites-enabled/

pip3 install -r requirements.txt

# Only for start working:
# django-admin startproject blackjack
# python3 manage.py startapp auth

mysql < init_db.sql

python3 manage.py makemigrations GameManager
python3 manage.py makemigrations
python3 manage.py migrate

mysql game_manager < datadump.sql
