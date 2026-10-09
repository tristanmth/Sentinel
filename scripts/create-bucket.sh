#!/bin/bash
# create-bucket.sh — Crée le bucket S3 dans LocalStack

set -e

echo "Création du bucket S3 'sentinel-data' dans LocalStack..."

if command -v awslocal &> /dev/null; then
    awslocal s3 mb s3://sentinel-data
    echo "OK Bucket créé avec awslocal"
else
    aws s3 mb s3://sentinel-data --endpoint-url=http://localhost:4566 --region us-east-1
    echo "OK Bucket créé avec aws cli"
fi

echo -e "\nVérification :"
aws s3 ls --endpoint-url=http://localhost:4566 --region us-east-1 || awslocal s3 ls
