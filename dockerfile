FROM ubuntu
WORKDIR /app
RUN apt update; apt install -y python3-venv python3-opencv
COPY app.py .
COPY requirements.txt .
RUN python3 -m venv .
RUN bin/pip install -r requirements.txt
RUN mkdir /app/static
CMD ["bin/python", "app.py"]
