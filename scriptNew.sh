#!/bin/bash

# Check if dnsviz is installed
if ! [ -x "$(command -v dnsviz)" ]; then
  echo 'Error: dnsviz is not installed.' >&2
  exit 1
fi

# Get current timestamp
timestamp=$(date +%Y%m%d%H%M%S)

# Create directories for output files
mkdir -p json_files
mkdir -p logfiles

# Read domain names from file
while read -r domain; do
  # Call DNSViz to analyze the domain
  dnsviz probe -A -a . -o "json_files/${domain}_${timestamp}.json" "$domain" 


  # Grok the DNSViz output for the domain
  dnsviz grok < "json_files/${domain}_${timestamp}.json" > "json_files/${domain}_${timestamp}-chk.json" 

  # Generate an HTML graph of the DNS namespace for the domain
  dnsviz graph -Thtml < "json_files/${domain}_${timestamp}.json" > "json_files/${domain}_${timestamp}.html" 

  # Output the results to a JSON file
  cat "json_files/${domain}_${timestamp}.json" 

  # Append the domain name to the processed.txt file
  echo "${domain} ${timestamp}" >> "json_files/${timestamp}_processed.txt"
done < input/domain.txt
