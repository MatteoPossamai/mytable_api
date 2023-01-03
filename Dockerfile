FROM python:3.11

# Set the working directory to /api
RUN mkdir /api
WORKDIR /api
COPY . /api

# Update pip and install requirements
RUN pip install --default-timeout=1000 --upgrade pip
RUN pip install --default-timeout=1000 -r requirements.txt

EXPOSE 5000

# Run manage.py runserver when the container launches
CMD ["python", "manage.py", "runserver"]

# docker build -t poss03251/my_table_api:1.0 .

# docker run -d -p 5000:5000 poss03251/my_table_api:1.0