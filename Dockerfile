FROM python:3.7 as builder

LABEL maintainer="Dominika Kowalczyk <dominika15kowalczyk@gmail.com>"


######################
# Install Dependencies
######################
COPY /requirements.txt /req/
COPY /extra_requirements.txt /req/
RUN pip3 install -U pip
RUN cd /req && pip3 install -r requirements.txt && pip3 install -r extra_requirements.txt



######################
# Install Application
######################
COPY /app /app



######################
# Set Application Environment Variables
######################

ENV PYTHONIOENCODING=utf-8 \
    PYTHONPATH=/app \
    FLASK_APP=run_app.py \
    DYNACONF_SETTINGS=settings


# Expose ports
EXPOSE 80

WORKDIR /app

# Execute the app
CMD [ "python3.7", "run_app.py" ]
