import os

def create_directories():
    os.makedirs("json_files", exist_ok=True)
    os.makedirs("log_files", exist_ok=True)

def read_domains_from_file(file_path):
    with open(file_path, "r") as file:
        return file.readlines()
