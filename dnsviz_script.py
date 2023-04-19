import os
import subprocess
from datetime import datetime

# Check if Docker is installed
try:
    subprocess.run(["docker", "--version"], check=True)
except subprocess.CalledProcessError:
    print("Error: Docker is not installed.")
    exit(1)

# Get current timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Create directories for output files
os.makedirs("json_files", exist_ok=True)
os.makedirs("log_files", exist_ok=True)

# Read domain names from file
with open("input_files/domain.txt", "r") as file:
    for domain in file.readlines():
        domain = domain.strip()

        try:
            # Call DNSViz to analyze the domain
            subprocess.run(
                [
                    "docker", "run", "--rm", "-v",
                    f"{os.path.abspath('.')}/json_files:/data",
                    "dnsviz/dnsviz", "probe", "-A", "-a", ".", "-o",
                    f"/data/{domain}_{timestamp}.json", domain
                ],
                check=True
            )

            # Grok the DNSViz output for the domain
            grok_command = [
                "docker", "run", "--rm", "-v",
                f"{os.path.abspath('.')}/json_files:/data",
                "dnsviz/dnsviz", "grok", "-f",
                f"/data/{domain}_{timestamp}.json", "-o",
                f"/data/{domain}_{timestamp}-chk.json"
            ]

            try:
                subprocess.check_output(grok_command, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                print(f"Error processing domain: {domain}")
                print(f"Return code: {e.returncode}")
                print(f"Error message: {e.output.decode('utf-8')}")
                with open("log_files/errors.txt", "a") as error_file:
                    error_file.write(f"Error processing domain: {domain} - Return code: {e.returncode} - Error message: {e.output.decode('utf-8')}\n")
                continue


            # Generate an HTML graph of the DNS namespace for the domain
            subprocess.run(
                [
                    "docker", "run", "--rm", "-v",
                    f"{os.path.abspath('.')}/json_files:/data",
                    "dnsviz/dnsviz", "graph", "-Thtml", "-f",
                    f"/data/{domain}_{timestamp}.json", "-o",
                    f"/data/{domain}_{timestamp}.html"
                ],
                check=True
            )

            # Output the results to a JSON file
            with open(f"json_files/{domain}_{timestamp}.json", "r") as json_file:
                print(json_file.read())

            # Append the domain name to the processed.txt file
            with open("log_files/processed.txt", "a") as processed_file:
                processed_file.write(f"{domain} {timestamp}\n")

        except subprocess.CalledProcessError as error:
            print(f"Error processing domain: {domain}")
            print(f"Error message: {error}")

            with open("log_files/errors.txt", "a") as error_file:
                error_file.write(f"Error processing domain: {domain} - Error message: {error}\n")
