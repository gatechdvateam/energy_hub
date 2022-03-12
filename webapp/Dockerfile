
#The below 2 articles helped me setup the container and put it on azure web app
# Thanks to: https://towardsdatascience.com/dockerize-your-dash-app-1e155dd1cea3
# https://code.visualstudio.com/docs/containers/app-service

# Use the below command to build the image. The format is docker username/repoName:Tags
# docker build -t mousahassan/webapp:latest .
# Use the below command to run the image or run it from docker.
# docker run -p 8080:80 tiny_home

#This is a ready made container image for python 3.7. 
FROM python:3.7-slim
#Copy the requiremnts file
COPY requirements.txt ./requirements.txt
#Install the requirements file.
RUN pip install -r requirements.txt
#Copy the site files.
COPY . ./
#Set up the environment varibles for the docker container.
ENV AZURE_CLIENT_ID 304a8bfd-de3b-45a7-81a1-6c444372b65f
ENV AZURE_CLIENT_SECRET iFQ7Q~0llDxGJh8uUjh8VOLnfjjVzK4z_5V6I
ENV AZURE_TENANT_ID 482198bb-ae7b-4b25-8b7a-6d7f32faa083
#Expose port 80
EXPOSE 80
#Run the web server.
CMD gunicorn -b 0.0.0.0:80 application:server