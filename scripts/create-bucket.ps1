# create-bucket.ps1 — Crée le bucket S3 dans LocalStack
# Usage : .\scripts\create-bucket.ps1

Write-Host "Création du bucket S3 'sentinel-data' dans LocalStack..."

# Méthode 1 : awslocal (si installé)
try {
    awslocal s3 mb s3://sentinel-data
    Write-Host "OK Bucket créé avec awslocal"
} catch {
    # Méthode 2 : aws cli avec endpoint local
    try {
        aws s3 mb s3://sentinel-data --endpoint-url=http://localhost:4566 --region us-east-1
        Write-Host "OK Bucket créé avec aws cli"
    } catch {
        Write-Host "aws cli non trouvé. Création manuelle :"
        Write-Host "   aws s3 mb s3://sentinel-data --endpoint-url=http://localhost:4566"
    }
}

Write-Host "`nVérification :"
aws s3 ls --endpoint-url=http://localhost:4566 --region us-east-1 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "(vérif manuelle : aws s3 ls --endpoint-url=http://localhost:4566)"
}
