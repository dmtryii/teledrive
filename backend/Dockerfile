FROM python

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Install postgresql-client to use pg_isready command
RUN apt-get update && apt-get install -y postgresql-client


# Set environment variables (if needed)
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Make sure the wait-for-db.sh script is executable
RUN chmod +x ./wait-for-db.sh

# Expose the port the app runs on
EXPOSE 5001

# Run the application
CMD ["/bin/sh", "-c", "./wait-for-db.sh db flask db upgrade && flask run --host=0.0.0.0 --port=5001"]