FROM python:3.14-slim

WORKDIR /app

COPY App/requirements.txt ./App/

RUN pip install --no-cache-dir -r App/requirements.txt

COPY App/ ./App/
COPY Model/ ./Model/
COPY JoblibFiles ./JoblibFiles/

CMD ["uvicorn","App.app:app","--host","0.0.0.0","--port","8080"]