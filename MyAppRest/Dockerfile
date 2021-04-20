FROM python:3.7.3

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY common /app/common
COPY MyAppRest /app/MyAppRest

RUN pip install uwsgi

EXPOSE 5000
CMD ["uwsgi", "MyAppRest/uwsgi.ini"]