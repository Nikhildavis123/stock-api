# Stock Stats API

A blazing-fast REST API built with FastAPI that retrieves real-time stock market data using yfinance. Ideal for financial dashboards, analytics platforms, or automated trading systems.

Features

- Fetch historical and real-time stock data
- FastAPI for high-performance REST endpoints
- Dockerized for easy deployment
- CI/CD pipeline with Jenkins, AWS ECR, Kubernetes, and ArgoCD

Installation & Running with Docker

# Build the Docker image

docker build -t stock-api .

# Run the container

docker run -p 8000:8000 stock-api

Access the API at: http://localhost:8000

Sample:http://localhost:8000/api/stats?ticker=MSFT&start=2023-01-01&end=2023-12-31

CI/CD Pipeline Overview
Here's how your code flows from commit to deployment:

- Developer pushes code to the Git repository.
- Jenkins pipeline triggers via webhook or Multibranch setup.

### Jenkins:

- Runs tests (pytest)
- Builds Docker image
- Optionally scans the image
- Tags the image with git commit or a semantic version
- Jenkins pushes the image to AWS ECR.
- Jenkins updates Kubernetes manifests (or Helm values) in the manifests Git repo with the new image tag.

### ArgoCD:

- Monitors the manifests repo
- Detects changes
- Syncs the cluster with the new image

### Rollback:

- Can be triggered via ArgoCD
- Or by reverting the manifest commit
