# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10

EXPOSE 1883
EXPOSE 1884
EXPOSE 7000


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /Laufzeitumgebung
COPY Docker /Laufzeitumgebung
ADD Laufzeitumgebung .

# Run the application
ENTRYPOINT ["python"]
CMD ["Laufzeitumgebung.py"]

# get requirements: pip list --format=freeze > requirements.txt
# venv aktivieren dann: Scripts\activate.bat
# docker build -t laufzeitumgebung .
# docker run -p 7000:7000 -p 1883:1883 laufzeitumgebung