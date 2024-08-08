FROM python:3.11.7-slim-bullseye


WORKDIR /src

# upgrade pip install setuptools and wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# copy requirements into the container 
COPY ./requirements.txt /src/requirements.txt

# install requirements
RUN pip install --no-cache-dir  --upgrade -r /src/requirements.txt

# Copy code 
COPY . .

# port 
EXPOSE 80
# Run app
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80" ]


# Test at the home, 
# docker build -t imagename .
# create and run container
# docker run --name containername -p 80:80 imagename