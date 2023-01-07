FROM python:3.11

# Managing user
RUN adduser --disabled-login --disabled-password devuser
USER devuser
WORKDIR /home/devuser

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY --chown=devuser:devuser requirements.txt requirements.txt
RUN pip install --user --default-timeout=1000 --upgrade pip
RUN pip install --user --default-timeout=1000 -r requirements.txt

EXPOSE 5000

ENV PATH="/home/devuser/."

COPY --chown=devuser:devuser . .

# Run manage.py runserver when the container launches
CMD ["python3", "manage.py", "runserver"]

# docker build -t poss03251/my_table_api:1.0 .

# docker run -d -p 5000:5000 poss03251/my_table_api:1.0