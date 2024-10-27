# Check if the Docker Desktop process is running
$dockerProcess = Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue

# Check if the Docker daemon is responsive
$dockerStatus = docker info 2>&1

if ($dockerProcess -and $dockerStatus -notmatch "Is the docker daemon running?") {
    Write-Host "Docker Desktop is running."

    Set-Location "C:\Users\chawl\OneDrive\Documents\practice\kubernetes\website\frontend\"
    docker build -t abhishekcha/stock-project-microservice:frontend .

    docker push abhishekcha/stock-project-microservice:frontend

    Set-Location "C:\Users\chawl\OneDrive\Documents\practice\kubernetes\website\backend\"
    docker build -t abhishekcha/stock-project-microservice:backend .

    docker push abhishekcha/stock-project-microservice:backend

    Set-Location "C:\Users\chawl\OneDrive\Documents\practice\kubernetes\website\alert-svc\"
    docker build -t abhishekcha/stock-project-microservice:alert-svc . 

    docker push abhishekcha/stock-project-microservice:alert-svc

    Set-Location "C:\Users\chawl\OneDrive\Documents\practice\kubernetes\website\inventory-mgmt\"
    docker build -t abhishekcha/stock-project-microservice:inventory-mgmt .

    docker push abhishekcha/stock-project-microservice:inventory-mgmt

    Set-Location "C:\Users\chawl\OneDrive\Documents\practice\kubernetes\website\sharemarket\"
    docker build -t abhishekcha/stock-project-microservice:sharemarket .

    docker push abhishekcha/stock-project-microservice:sharemarket

} else {
    Write-Host "Docker Desktop is NOT running."
}
