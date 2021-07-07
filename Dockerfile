FROM python:3.9

LABEL version="1.0"
LABEL description="GitCheckup is an open-source project."

ENV PYTHONBUFFERED=1

# Install dependencies.
# whitenoise and gunicorn is needed for Heroku environment.
RUN apt update
RUN pip install django matplotlib pygithub whitenoise gunicorn

# Copy the source code.
RUN mkdir /gitcheckup && cd /gitcheckup
WORKDIR /gitcheckup
ADD GitCheckup /gitcheckup/GitCheckup
COPY ./manage.py /gitcheckup
EXPOSE 8008
