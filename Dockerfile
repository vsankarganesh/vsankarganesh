FROM python:3
WORKDIR  /WORK_DIR
#RUN python3 -m venv /opt/venv
COPY requirements.txt .
#RUN . /opt/venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "./src/main.py"]
