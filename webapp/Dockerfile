
#The below 2 articles helped me setup the container and put it on azure web app
# Thanks to: https://towardsdatascience.com/dockerize-your-dash-app-1e155dd1cea3
# https://code.visualstudio.com/docs/containers/app-service

# Use the below command to build the image. The format is docker username/repoName:Tags
# docker build -t mousahassan/dvawebapp:latest .
# Use the below command to run the image or run it from docker (Read notes first)
# Don't put the value of (-e) which is environement variable in command line. Docker pulls it from current environment.
# https://stackoverflow.com/questions/30494050/how-do-i-pass-environment-variables-to-docker-containers
# Also container name must come at the end
# https://stackoverflow.com/questions/27158840/docker-executable-file-not-found-in-path
# docker run -e AZURE_CLIENT_ID -e AZURE_CLIENT_SECRET -e AZURE_TENANT_ID -p 8080:80 mousahassan/dvawebapp:latest

#This is a ready made container image for python 3.9. 
FROM python:3.9-slim
#Copy the requiremnts file
COPY requirements.txt ./requirements.txt
#Install the requirements file.
RUN pip install -r requirements.txt
#Copy the site files.
COPY . ./
#Don't Set up the environment varibles of azure here. This will expose these and can be dangerous.
#Do this by setting up these when running the image on local machine or in the app configuration in azure!
#Expose port 80
EXPOSE 80
#Run the web server.
CMD gunicorn -b 0.0.0.0:80 application:server