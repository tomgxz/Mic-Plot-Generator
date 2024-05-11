py -m pip install -r requirements.txt
echo SECRETKEY='INSECURE-CHANGE' >> .env
py -m manage makemigrations micplot
py -m manage sqlmigrate micplot 0001
py -m manage migrate