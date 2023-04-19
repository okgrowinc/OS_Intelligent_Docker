import os
import subprocess

def run_dnsviz_graph(domain, timestamp):
    with open(f"{os.path.abspath('.')}/json_files/{domain}_{timestamp}.json", "rb") as input_file:
        subprocess.run([
            "docker", "run", "--rm", "-i", "-v",
            f"{os.path.abspath('.')}/json_files:/data",
            "dnsviz/dnsviz", "graph", "-Thtml", "-o",
            f"/data/{domain}_{timestamp}.html"
        ], stdin=input_file)
