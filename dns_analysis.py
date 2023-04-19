from datetime import datetime
from file_operations import create_directories, read_domains_from_file
from dnsviz_probe import run_dnsviz_probe
from dnsviz_grok import run_dnsviz_grok
from dnsviz_graph import run_dnsviz_graph
from error_handling import log_error

def main():
    create_directories()
    domains = read_domains_from_file("input_files/domain.txt")

    for domain in domains:
        domain = domain.strip()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        run_dnsviz_probe(domain, timestamp)
        grok_result = run_dnsviz_grok(domain, timestamp)

        if grok_result.returncode != 0:
            print(f"Error processing domain: {domain}")
            print(f"Return code: {grok_result.returncode}")
            log_error(domain, grok_result)
            continue

        run_dnsviz_graph(domain, timestamp)

        with open(f"json_files/{domain}_{timestamp}.json", "r") as json_file:
            json_content = json_file.read()

        with open("log_files/processed.txt", "a") as processed_file:
            processed_file.write(f"{domain} {timestamp}\n")

if __name__ == "__main__":
    main()