# Thanks to: https://towardsdatascience.com/dockerize-your-dash-app-1e155dd1cea3
FROM python:3.7-slim
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install tk
COPY . ./
ENV AZURE_CLIENT_ID 304a8bfd-de3b-45a7-81a1-6c444372b65f
ENV AZURE_CLIENT_SECRET iFQ7Q~0llDxGJh8uUjh8VOLnfjjVzK4z_5V6I
ENV AZURE_TENANT_ID 482198bb-ae7b-4b25-8b7a-6d7f32faa083
CMD gunicorn -b 0.0.0.0:80 application:server
