FROM python

WORKDIR .

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

CMD ["python3", "./auth_bot.py"]