# Start with the official Apache NiFi image
FROM apache/nifi:latest

# Install required packages for dnsviz and psycopg2
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip libpq-dev dnsutils && \
    pip3 install dnsviz psycopg2

# Copy the dnsviz_script.py to the container
COPY dnsviz_script.py /opt/nifi/dnsviz_script.py

# Switch back to the default NiFi user
USER nifi
