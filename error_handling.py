def log_error(domain, result):
    with open("log_files/errors.txt", "a") as error_file:
        error_file.write(f"Error processing domain: {domain} - Return code: {result.returncode}\n")
        if result.stdout:
            error_file.write(f"Standard output: {result.stdout}\n")
        if result.stderr:
            error_file.write(f"Standard error: {result.stderr}\n")
