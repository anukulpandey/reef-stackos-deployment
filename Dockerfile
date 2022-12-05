# 
FROM python:3.9

# 
WORKDIR /stackOS

# 
COPY ./requirements.txt /stackOS/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /stackOS/requirements.txt

# 
COPY ./app /stackOS/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
