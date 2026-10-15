# RickyGPT

## Setup

Create and activate the Conda environment, then install the project dependencies:

```bash
conda create -n rickygpt python=3.11 -y
conda activate rickygpt
pip install -r requirements.txt

```


AWS-CICD-Deployment-with-Github-Actions
1. Login to AWS console.

2. Create IAM user for deployment

- EC2: access : It is a virtual machine
- ECR: Elastic Container registry to save your docker image in aws

# Description: About the deployment

- Build docker image of the source code
- Push your docker image to ECR
- Lanch your EC2
- Pull Your image from ECR in EC2
- Lanuch your docker image in EC2



5. Open EC2 and Install docker in EC2 Machine:

# optional

sudo apt-get update -y

sudo apt-get upgrade

# required
curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo suermod -aG docker ubuntu

newgrp docker



6. Configure EC2 as self-hosted runner:

settings>actions>runner>new self hosted runner> choose os > then run command one by one

7. Setup github secrets:

GOOGLE_API_KEY
GOOGLE_MODEL
TAVILY_API_KEY

LANGSMITH_API_KEY
LANGSMITH_ENDPOINT
LANGSMITH_TRACING
LANGSMITH_PROJECT