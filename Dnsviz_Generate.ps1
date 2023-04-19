# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker is not installed." -ForegroundColor Red
    exit 1
}

# Get current timestamp
$timestamp = Get-Date -Format "yyyyMMddHHmmss"

# Create directories for output files
New-Item -ItemType Directory -Path json_files -Force | Out-Null
New-Item -ItemType Directory -Path log_files -Force | Out-Null

# Read domain names from file
Get-Content (Resolve-Path ./input_files/domain.txt) | ForEach-Object {
    $domain = $_
    
    try {
        # Call DNSViz to analyze the domain
        docker run --rm -v "$(Resolve-Path .)\json_files:/data" dnsviz/dnsviz probe -A -a . -o "/data/$($domain)_$($timestamp).json" $domain

        # Grok the DNSViz output for the domain
        docker run --rm -v "$(Resolve-Path .)\json_files:/data" dnsviz/dnsviz grok -f "/data/$($domain)_$($timestamp).json" -o "/data/$($domain)_$($timestamp)-chk.json"

        # Generate an HTML graph of the DNS namespace for the domain
        docker run --rm -v "$(Resolve-Path .)\json_files:/data" dnsviz/dnsviz graph -Thtml -f "/data/$($domain)_$($timestamp).json" -o "/data/$($domain)_$($timestamp).html"

        # Output the results to a JSON file
        Get-Content "json_files/$($domain)_$($timestamp).json"

        # Append the domain name to the processed.txt file
        Add-Content -Path "log_files/processed.txt" -Value "$($domain) $($timestamp)"
    }
    catch {
        Write-Host "Error processing domain: $domain" -ForegroundColor Red
        Write-Host "Error message: $_" -ForegroundColor Red
        Add-Content -Path "log_files/errors.txt" -Value "Error processing domain: $domain - Error message: $_"
    }
}
