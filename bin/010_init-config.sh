#!/bin/bash

# Load environment variables from .env file
if [[ -f .env ]]; then
    export $(cat .env | sed 's/#.*//g' | xargs)
fi

# Check if domain variable is set in the environment
if [[ -z $domains ]]; then
    echo "Error: 'domains' variable not set in the .env file."
    exit 1
fi

# Read the sample file and replace the placeholder with the domain value
sed "s/__DOMAIN__/$domains/g" ./nginx/_sample_nginx.conf > ./nginx/nginx.conf

echo "Generated nginx.conf file with the updated domain."
