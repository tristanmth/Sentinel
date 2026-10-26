# create-bucket.sh — Crée le bucket S3 dans LocalStack
#
#set -e
#
#echo "Création du bucket S3 'sentinel-data' dans LocalStack..."
#
#if command -v awslocal &> /dev/null; then
#    awslocal s3 mb s3://sentinel-data
#    echo "OK Bucket créé avec awslocal"
#else
#    aws s3 mb s3://sentinel-data --endpoint-url=http://localhost:4566 --region us-east-1
#    echo "OK Bucket créé avec aws cli"
#fi
#
#echo -e "\nVérification :"
#aws s3 ls --endpoint-url=http://localhost:4566 --region us-east-1 || awslocal s3 ls
#

#!/bin/bash
# create-bucket.sh — Crée et vérifie le bucket S3 dans LocalStack

set -e

ENDPOINT="http://localhost:4566"
BUCKET="sentinel-data"
REGION="us-east-1"

export AWS_ACCESS_KEY_ID="sentinel"
export AWS_SECRET_ACCESS_KEY="sentinel123"
export AWS_DEFAULT_REGION="$REGION"

echo "Création du bucket S3 '$BUCKET' dans LocalStack..."

# Sélectionne AWS CLI
if command -v awslocal >/dev/null 2>&1; then
    AWS_CMD=(awslocal)
    USE_LOCAL=true
elif command -v aws >/dev/null 2>&1; then
    AWS_CMD=(aws)
    USE_LOCAL=false
else
    echo "ERREUR : AWS CLI ou awslocal est introuvable." >&2
    exit 1
fi

# Vérifie que LocalStack est accessible
if ! curl -fsS --max-time 5 "$ENDPOINT/_localstack/health" >/dev/null; then
    echo "ERREUR : LocalStack n'est pas accessible sur $ENDPOINT." >&2
    echo "Démarre-le avec : docker compose up -d localstack" >&2
    exit 1
fi

if [ "$USE_LOCAL" = true ]; then
    "${AWS_CMD[@]}" s3 mb "s3://$BUCKET" || echo "Le bucket existe peut-être déjà."
    echo
    "${AWS_CMD[@]}" s3 ls
else
    "${AWS_CMD[@]}" s3 mb "s3://$BUCKET" 
        --endpoint-url="$ENDPOINT" --region "$REGION" 
        || echo "Le bucket existe peut-être déjà."

    echo
    "${AWS_CMD[@]}" s3 ls \
        --endpoint-url="$ENDPOINT" --region "$REGION"
fi

echo "Vérification terminée."