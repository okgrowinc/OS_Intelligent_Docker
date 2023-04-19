# Define directories to create
$directories = @(
    "custom_processors",
    "input_files",
    "python_scripts"
)

# Loop through each directory and create it if it doesn't exist
foreach ($dir in $directories) {
    if (-not (Test-Path -Path $dir)) {
        New-Item -ItemType Directory -Path $dir
        Write-Host "Created directory: $dir"
    } else {
        Write-Host "Directory already exists: $dir"
    }
}

# Check if docker-compose is installed
try {
    docker-compose --version
} catch {
    Write-Host "docker-compose is not installed or not in the system PATH. Please install Docker Compose and ensure it is in the system PATH."
    exit 1
}

# Execute docker-compose up -d command to start the platform in Docker
Write-Host "Starting TalentXplorer platform using Docker Compose..."
docker-compose up -d
