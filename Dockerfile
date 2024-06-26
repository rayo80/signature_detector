FROM python:3.10

RUN python3 -m venv /env
ENV PATH /env/bin:$PATH

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx ffmpeg libsm6 libxext6 libgtk2.0-dev

#RUN apt install -y ffmpeg libsm6 libxext6 libgtk2.0-dev

ADD requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt
ADD . /app

WORKDIR /app
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
