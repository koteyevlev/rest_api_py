source /home/entrant/venvs/flaskproj/bin/activate;
cd /home/entrant/rest_api_py;
gunicorn --bind 0.0.0.0:8080 --threads 20 main:app
