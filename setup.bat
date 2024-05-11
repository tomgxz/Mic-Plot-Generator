py -m venv .venv
echo SECRETKEY='django-insecure-=q5e15&3$j=10djmou2=3s!(hmz6(wqpx#@mq!w0^%)=+#6u#+' >> .env
py -m manage makemigrations micplot
py -m manage sqlmigrate micplot 0001
py -m manage migrate