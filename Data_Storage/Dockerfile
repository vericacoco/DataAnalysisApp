# Use the official PostgreSQL image from Docker Hub
FROM postgres:13

# Optional: copy custom SQL files to initialize the database
# COPY ./init.sql /docker-entrypoint-initdb.d/

# Set environment variables for PostgreSQL (Optional, can also be set in docker-compose.yml)
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydatabase

# Expose the default PostgreSQL port
EXPOSE 5432
