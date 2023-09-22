# build_files.sh
pip install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic

echo "hola cara cola" > ./authapp/templates/welcome.html
