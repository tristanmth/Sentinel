# create-bucket.ps1 — Crée le bucket S3 dans LocalStack
# Usage : .\scripts\create-bucket.ps1

#Write-Host "Création du bucket S3 'sentinel-data' dans LocalStack..."

# Méthode 1 : awslocal (si installé)
#try {
#    awslocal s3 mb s3://sentinel-data
#    Write-Host "OK Bucket créé avec awslocal"
#} catch {
#    # Méthode 2 : aws cli avec endpoint local
#    try {
#        aws s3 mb s3://sentinel-data --endpoint-url=http://localhost:4566 --region us-east-1
#        Write-Host "OK Bucket créé avec aws cli"
#    } catch {
#        Write-Host "aws cli non trouvé. Création manuelle :"
#        Write-Host "   aws s3 mb s3://sentinel-data --endpoint-url=http://localhost:4566"
#    }
#}
#
#Write-Host "`nVérification :"
#aws s3 ls --endpoint-url=http://localhost:4566 --region us-east-1 2>$null
#if ($LASTEXITCODE -ne 0) {
#    Write-Host "(vérif manuelle : aws s3 ls --endpoint-url=http://localhost:4566)"
#}


# create-bucket.ps1 — Crée et vérifie le bucket S3 dans LocalStack
# Usage : .\scripts\create-bucket.ps1

# Création et vérification du bucket S3 dans LocalStack

$ErrorActionPreference = "Stop"

$endpoint = "http://localhost:4566"
$bucket = "sentinel-data"
$region = "us-east-1"
$python = "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe"

Write-Host "Création du bucket S3 '$bucket' dans LocalStack..."

# Identifiants pour LocalStack
$env:AWS_ACCESS_KEY_ID = "sentinel"
$env:AWS_SECRET_ACCESS_KEY = "sentinel123"
$env:AWS_DEFAULT_REGION = $region

# Vérifier Python et AWS CLI
if (-not (Test-Path $python)) {
    Write-Host "ERREUR : Python est introuvable." -ForegroundColor Red
    exit 1
}

# Vérifier que LocalStack fonctionne
try {
    Invoke-RestMethod "$endpoint/_localstack/health" -TimeoutSec 5 | Out-Null
}
catch {
    Write-Host "ERREUR : LocalStack n'est pas démarré." -ForegroundColor Red
    Write-Host "Lance : docker compose up -d"
    exit 1
}

# Créer le bucket
& $python -m awscli s3 mb "s3://$bucket" "--endpoint-url=$endpoint" --region $region

if ($LASTEXITCODE -ne 0) {
    Write-Host "Le bucket existe peut-être déjà. Vérification..."
}

# Afficher les buckets
Write-Host "`nBuckets disponibles :"

& $python -m awscli s3 ls "--endpoint-url=$endpoint" --region $region

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR : impossible de lister les buckets." -ForegroundColor Red
    exit 1
}

Write-Host "`nTerminé !" -ForegroundColor Green