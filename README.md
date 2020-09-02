# glocal

Django base Front+Backend for glocal project

  

# setup

### Anaconda download & install

참조: https://www.anaconda.com/download/

각 OS에 해당되는 파일 다운로드

``` bash

$ curl https://repo.continuum.io/archive/Anaconda3-2018.12-Linux-x86_64.sh > Anaconda3-2018.12-Linux-x86_64.sh

$ bash Anaconda3-2018.12-Linux-x86_64.sh

```

  

### Create virtual envinronment

환경 이름을 'glocal'으로 할 경우

  

``` python

$ conda create -n glocal python=3.7

$ . activate glocal

(glocal) $ _

```

  

### Install requirements packages

```python

(glocal) $ pip install -r requirements.txt

```

### Install packages Reference

requirements.txt 참고

  

### DB setting

```python

(glocal) $ ./manage.py makemigrations

(glocal) $ ./manage.py migrate

```

  

### run dev. server

```python

(glocal) $ ./manage.py runserver

```
### Secret.json
##### make json file
```python
 __ accounts/
|__ annual/
|__ commute/
|__ glocal/  | __pycache__/
			 | __init__.py
			 | csrfexempt.py
			 | secret.json <-- make here!!!!
			 | secret.py 
			 | settings.py
			 | urls.py
			 | wsgi.py
|__ home/
|__ .../
```
##### secret.json
```python
{
	"key":"<your django secret key>",
	"GITHUB_WEBHOOK_KEY":"<your github webhook key>",
	"slack_key":"<your slacker key>",
	"ALLOWED_HOSTS":["<your domain name>","127.0.0.1","localhost"],
	"EMAIL_BACKEND":"django.core.mail.backends.smtp.EmailBackend",
	"EMAIL_USE_TLS":<true or false>,
	"EMAIL_HOST":"<ex: smtp.gmail.com>",
	"EMAIL_PORT":<ex: 587>,
	"EMAIL_HOST_USER":"<your mail address>",
	"EMAIL_HOST_PASSWORD":"<your mail password>",
	"SERVER_EMAIL":"<your mail address>",
	"DEFAULT_FROM_MAIL":"<your mail name>",
	"CONDA_ENV":"<your conda environment>",
	"map_api":"<your naver map api>"
}
```
### Celery, Redis Setup (for Pushbullet, githook server reloading)
##### Redis install
> (run)ubuntu@--.--.--.--/srv/glocal$ sudo apt-get install redis-server
##### Redis start
> (run)ubuntu@--.--.--.--/srv/glocal$ redis-server
> 
##### Celery Setup
Linux tmux
> (run)ubuntu@--.--.--.--/srv/glocal$ tmux attach
> (run)ubuntu@--.--.--.--/srv/glocal$ celery -A glocal worker -l info
---
### Linux Crontab Batch Command (for Annual app)
##### make linux shell script for Django command
Annual Create action
```python
#annual_create.sh
if cd /srv/glocal/&&source ~/anaconda3/etc/profile.d/conda.sh&&conda activate run&&python manage.py annual_create ; then
echo "$(date +%Y):$(date +%m):$(date +%d)  $(date +%H):$(date +%M):$(date +%S) annual create"
else
<Your failed action>
fi
```
Annual Email send
```python
#annual_email.sh
if cd /srv/glocal/ && source ~/anaconda3/etc/profile.d/conda.sh && conda activate run && python manage.py annual_email ; then
echo "$(date +%Y):$(date +%m):$(date +%d)  $(date +%H):$(date +%M):$(date +%S) annual email"
else
<Your failed action>
fi
```
Annual Extnc action
```python
#annual_extnc.sh
if cd /srv/glocal/ && source ~/anaconda3/etc/profile.d/conda.sh && conda activate run && python manage.py annual_extnc ; then
echo "$(date +%Y):$(date +%m):$(date +%d)  $(date +%H):$(date +%M):$(date +%S) annual extnc"
else
<Your failed action>
fi
```
Annual Use action
```python
#annual_use.sh
if cd /srv/glocal/ && source ~/anaconda3/etc/profile.d/conda.sh && conda activate run && python manage.py annual_use ; then
echo "$(date +%Y):$(date +%m):$(date +%d)  $(date +%H):$(date +%M):$(date +%S) annual extnc"
else
<Your failed action>
fi
```
##### Crontab config 
> (run)ubuntu@--.--.--.--/$ crontab -e
```python
# 분 시 일 달 요일
0 0 * * * /srv/batch/annual_create.sh >> <your log directory>.log 2>&1
# 매일 0시 0분 실행
0 23 * * * /srv/batch/annual_use.sh >> <your log directory>.log 2>&1
# 매일 23시 0분 실행
5 0 * * * /srv/batch/annual_extnc.sh >> <your log directory>.log 2>&1
# 매일 0시 5분 실행
0 10 * * * /srv/batch/annual_email.sh >> <your log directory>.log 2>&1
# 매일 10시 0분 실행
```

* * *
 ------------
  ---
# Operating in Linux server

 * Web server : Nginx
 * WSGI : gunicorn
 * SSL 인증서 : letsencrypt(for map api)
 * Postgresql

### Linux Setup and Django project Setup

##### locale 설정
>  ubuntu@--.--.--.--/$ sudo nano /etc/default/locale
```python
LC_CTYPE=”en_US.UTF-8”
LC_ALL=”en_US.UTF-8”
LANG=”en_US.UTF-8”
```
##### 패키지 업데이트
>  ubuntu@--.--.--.--/$ sudo apt-get update

##### 패키지 의존성 검사 및 업데이트
>  ubuntu@--.--.--.--/$ sudo apt-get dist-upgrade

##### pip install
>  ubuntu@--.--.--.--/$ sudo apt-get install python-pip

##### anaconda install
다운로드 : https://www.anaconda.com/download/#linux
>  ubuntu@--.--.--.--/$ bash Anaconda3-2019.03-Linux-x86_64.sh

##### anaconda 환경변수 적용
> ubuntu@--.--.--.--/$ source ~/.bashrc

##### 가상환경 생성 및 적용
> (base)ubuntu@--.--.--.--/$ conda create -n <가상환경 이름> python=3.7
> (base)ubuntu@--.--.--.--/$ source activate <가상환경 이름>
가상환경은 run 이라 가정
> (run)ubuntu@--.--.--.--/$ 

##### 생성하고자 하는 디렉토리로 이동
디렉토리는 '/srv' 로 가정
> (run)ubuntu@--.--.--.--/$ cd /srv

##### git clone
> (run)ubuntu@--.--.--.--/srv$ git clone https://github.com/kimdong0/glocal.git

##### install requirements package
> (run)ubuntu@--.--.--.--/srv$ cd glocal
> (run)ubuntu@--.--.--.--/srv/glocal$ pip install -r requirements.txt

##### DB Settings
> (run)ubuntu@--.--.--.--/srv/glocal$ python manage.py makemigrations
> (run)ubuntu@--.--.--.--/srv/glocal$ python manage.py migrate
---
### Gunicorn Setup

##### install gunicorn
> (run)ubuntu@--.--.--.--/$ pip install gunicorn

##### gunicorn daemon setup
> (run)ubuntu@--.--.--.--/$ sudo nano /etc/systemd/system/gunicorn.service
```python
[Unit]
Description=gunicorn daemon
After=network.target
#
[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/srv/glocal/
ExecStart=/home/ubuntu/anaconda3/envs/run/bin/gunicorn \
--workers 3 \
--bind unix:/srv/glocal.sock \
glocal.wsgi:application

[Install]
WantedBy=multi-user.target
```
| 값 | 의미 | 
| :-------------------: | :-------------------: |
 User, Group | 리눅스 계정 유저이름, 그룹이름 
 WorkingDirectory | 프로젝트 폴더 위치 |
ExecStart | gunicorn의 설치 위치
--workers | gunicorn 프로세스 수
--bind | 통신 방식
glocal.wsgi : application | project 폴더 안의 wsgi.py


##### gunicorn service register
> (run)ubuntu@--.--.--.--/$ sudo systemctl enable gunicorn
##### gunicorn service start
> (run)ubuntu@--.--.--.--/$ sudo systemctl start gunicorn
---
### Nginx Setup
##### install nginx
> (run)ubuntu@--.--.--.--/$ sudo apt-get install nginx
##### nginx daemon setup
> (run)ubuntu@--.--.--.--/$ sudo nano /etc/nginx/sites-enabled/nginx.conf
```python
server {
	listen 80; #포트 번호 지정
	server_name <your domain>;

	location / {
		proxy_pass http://unix:/srv/glocal.sock; #gunicorn과 통신할 socket 지정
		include proxy_params;
}
```
##### nginx restart
> (run)ubuntu@--.--.--.--/$ sudo systemctl restart nginx

----

### Django static, media 파일 모아주기
##### Django collectstatic
> (run)ubuntu@--.--.--.--/srv/glocal$ ./manage.py collectstatic
##### nginx staticfiles config
> (run)ubuntu@--.--.--.--/srv/glocal$ sudo nano /etc/nginx/sites-enabled/nginx.conf
```python
server {
	listen 80;
	server_name <domain name>;
	
	location / {
		proxy_pass http://unix:/srv/glocal.sock;
		include proxy_params;
	}
	location /static/ {
		alias /srv/glocal/statics/;
	}
	location /media/ {
		alias /srv/glocal/media/;
	}
}
```
---
### SSL certificate(letsencrypt) setup for map API
##### letsencrypt certbot install 
> (run)ubuntu@--.--.--.--/srv/glocal$ sudo apt-get install software-properties-common
> (run)ubuntu@--.--.--.--/srv/glocal$ sudo add-apt-repository ppa:certbot/certbot
> (run)ubuntu@--.--.--.--/srv/glocal$ sudo apt-get install certbot
##### nginx, gunicorn stop
> (run)ubuntu@--.--.--.--/srv/glocal$ sudo systemctl stop nginx gunicorn
##### certificate 발급
> (run)ubuntu@--.--.--.--/srv/glocal$ certbot certonly --standalone -d <도메인이름>
##### nginx 연결
> (run)ubuntu@--.--.--.--/srv/glocal$ sudo nano /etc/nginx/sites-enabled/nginx.conf
```python
server {
	listen 443;
	server_name <도메인 이름>;

	ssl on;
	ssl_certificate /etc/letsencrypt/live/<도메인이름>/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/<도메인이름>/privkey.pem;

	location / {
		proxy_pass http://unix:/srv/glocal.sock;
		include proxy_params;
	}

	location /static/ {
		alias /srv/glocal/statics/;
	}
	location /media/ {
		alias /srv/glocal/media/;
	}
}
```
---
### Postgresql
##### postgresql install
> (run)ubuntu@--.--.--.--/srv/glocal$ sudo apt-get install postgresql
##### DB 생성
> (run)ubuntu@--.--.--.--/srv/glocal$ sudo -u <user명> createdb <db이름>
##### DB 접속
> (run)ubuntu@--.--.--.--/srv/glocal$ sudo -u <user명> psql <db이름>
> DB이름=#
##### DB encoding, timezone 설정
> DB이름=# postgres=# create user <user명> with password <패스워드>;
> DB이름=# alter role <user명> set client_encoding to ‘utf-8’;
> DB이름=# alter role <user명> set timezone to ‘Asia/Seoul’;
##### DB user 권한설정
> DB이름=# grant all privileges on database <DB이름> to <user명>;
##### Django postgresql 연동
> (run)ubuntu@--.--.--.--/srv/glocal$ sudo nano /srv/glocal/glocal/secret.json
```python
DATABASE ={
	‘default:{
	‘ENGINE’:’django.db.backends.postgresql’,
	‘NAME’:’DB 이름’,
	‘USER’:’user명’,
	‘PASSWORD’:’유저 비밀번호’,
	‘HOST’:’localhost’,
	‘PORT’:’포트(default 포트는 5432라고 한다)’
	}
}
```
##### DB migrations
> (run)ubuntu@--.--.--.--/srv/glocal$ python manage.py makemigrations
> (run)ubuntu@--.--.--.--/srv/glocal$ python manage.py migrate
--------
-------