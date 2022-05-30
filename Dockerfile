# Python image to use.

FROM --platform=linux/amd64 civisanalytics/datascience-python:latest
#FROM clrun6:latest


# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY requirements.txt .


# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .
COPY ./RE12_1000_221.ccdos /Bascon/Bruker/Sandbox/Reverse1/RE12_1000_221.ccdos
COPY ./RE12_1075_221.ccdos /Bascon/Bruker/Sandbox/Reverse1/RE12_1075_221.ccdos
#COPY ./Data/RE12_1075_221:0:10000 /Bascon/Bruker/Sandbox/Reverse1

#EXPOSE 8080

#CMD gunicorn --chdir app main:app -w 2 --threads 2 -b 0.0.0.0:8080


# Run app.py when the container launches
ENTRYPOINT ["python", "app.py"]
