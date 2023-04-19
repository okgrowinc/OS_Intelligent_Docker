import os
import subprocess

def run_dnsviz_grok(domain, timestamp):
    with open(f"{os.path.abspath('.')}/json_files/{domain}_{timestamp}.json", "rb") as input_file:
        command = [
            "docker", "run", "--rm", "-i", "-v",
            f"{os.path.abspath('.')}/json_files:/data",
            "dnsviz/dnsviz", "grok", "-o",
            f"/data/{domain}_{timestamp}-chk.json"
        ]
        return subprocess.run(command, stdin=input_file, capture_output=True, text=True)
