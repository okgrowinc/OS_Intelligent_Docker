import os
import subprocess

def run_dnsviz_probe(domain, timestamp):
    subprocess.run([
        "docker", "run", "--rm", "-v",
        f"{os.path.abspath('.')}/json_files:/data",
        "dnsviz/dnsviz", "probe", "-A", "-a", ".", "-o",
        f"/data/{domain}_{timestamp}.json", domain
    ])
