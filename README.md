# RickyGPT

RickyGPT is an AI-powered conversational assistant built with **FastAPI**, **LangChain/LangGraph**, and a custom ChatGPT-style web interface.

The application supports streaming AI responses, persistent conversation history, document uploads for retrieval-augmented generation (RAG), and tool-enabled agent workflows.

## Features

- ChatGPT-style conversational interface
- FastAPI backend
- Streaming AI responses using Server-Sent Events (SSE)
- Persistent conversation history
- Multiple conversation threads
- Document upload and RAG support
- Tool-enabled AI agent
- Web search integration
- Markdown rendering
- Code block formatting and copy support
- Model selection support
- Docker support
- Optional GitHub Actions CI/CD deployment workflow

## Tech Stack

### Backend

- Python 3.11
- FastAPI
- Uvicorn
- LangChain
- LangGraph
- SQL database for conversation history

### AI / Agent

- Google Gemini
- Tavily Search
- LangSmith
- Retrieval-Augmented Generation (RAG)

### Frontend

- HTML
- CSS
- JavaScript
- Jinja2 Templates
- Server-Sent Events
- Marked.js
- DOMPurify

### DevOps

- Docker
- Docker Hub
- GitHub Actions
- AWS EC2
- AWS IAM
- AWS Systems Manager
- GitHub OIDC authentication

---

## Project Structure

```text
RickyGPT/
│
├── app.py
├── agent.py
├── database.py
├── rag.py
├── tools.py
├── requirements.txt
├── Dockerfile
│
├── templates/
│   └── index.html
│
├── uploads/
│
├── data/
│
└── .github/
    └── workflows/
        └── cicd.yaml
```

## Application Architecture

```text
Browser
   │
   ▼
ChatGPT-style Frontend
HTML / CSS / JavaScript
   │
   │ HTTP + SSE
   ▼
FastAPI
   │
   ▼
LangGraph / LangChain Agent
   │
   ├── Gemini
   ├── Tavily Search
   ├── RAG
   └── Agent Tools
   │
   ▼
Conversation Database
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/rt3438/RickyGPT.git
cd RickyGPT
```

### 2. Create a Conda environment

```bash
conda create -n rickygpt python=3.11 -y
conda activate rickygpt
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
GOOGLE_API_KEY=your_google_api_key
GOOGLE_MODEL=your_model_name

TAVILY_API_KEY=your_tavily_api_key

LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_ENDPOINT=your_langsmith_endpoint
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=RickyGPT
```

Do not commit your `.env` file to GitHub.

Add it to `.gitignore`:

```text
.env
```

---

## Running the Application

Start the FastAPI server:

```bash
python app.py
```

The application runs on:

```text
http://localhost:8080
```

Uvicorn is configured to listen on:

```text
0.0.0.0:8080
```

When accessing the application locally, use:

```text
http://localhost:8080
```

or:

```text
http://127.0.0.1:8080
```

---

## API Endpoints

### Home

```http
GET /
```

Loads the RickyGPT web interface.

### Conversations

```http
GET /conversations
```

Returns saved conversation threads.

### Conversation History

```http
GET /history/{thread_id}
```

Returns the messages associated with a conversation.

### Document Upload

```http
POST /upload
```

Uploads a document and adds it to the RAG knowledge base for the specified conversation.

Supported file types include:

```text
PDF
DOCX
TXT
Markdown
Python
CSV
```

### Streaming Chat

```http
POST /chat/stream
```

Sends a message to the AI agent and streams the response back to the frontend using Server-Sent Events.

Example request:

```json
{
  "message": "Explain retrieval-augmented generation.",
  "thread_id": "example-thread-id",
  "model": "gemini-3-flash-preview"
}
```

---

## Retrieval-Augmented Generation

RickyGPT supports uploading documents that can be used as additional context during conversations.

The basic workflow is:

```text
Upload document
      │
      ▼
Process document
      │
      ▼
Split into chunks
      │
      ▼
Store document embeddings
      │
      ▼
Retrieve relevant context
      │
      ▼
Agent generates response
```

This allows the assistant to answer questions based on uploaded files instead of relying only on the language model's existing knowledge.

---

## Streaming Responses

The `/chat/stream` endpoint uses FastAPI's `StreamingResponse` and Server-Sent Events.

The backend streams individual AI response chunks to the browser:

```text
FastAPI
   │
   │ token
   ▼
Browser
   │
   │ token
   ▼
Browser
   │
   │ token
   ▼
Complete response
```

This provides a conversational experience similar to modern AI chat applications.

---

## Docker

Build the Docker image:

```bash
docker build -t rickygpt .
```

Run the container:

```bash
docker run -d \
  --name rickygpt \
  --env-file .env \
  -p 8080:8080 \
  rickygpt
```

Then open:

```text
http://localhost:8080
```

Check running containers:

```bash
docker ps
```

View application logs:

```bash
docker logs -f rickygpt
```

---

## CI/CD Architecture

The repository includes an optional GitHub Actions workflow for container-based deployment.

The deployment architecture is:

```text
GitHub
   │
   │ push to main
   ▼
GitHub Actions
   │
   ├── Validate Python
   ├── Install dependencies
   ├── Build Docker image
   └── Push Docker image
   │
   ▼
Docker Hub
   │
   ▼
AWS OIDC Authentication
   │
   ▼
AWS Systems Manager
   │
   ▼
EC2
   │
   ├── Pull new image
   ├── Replace container
   └── Start FastAPI
```

The deployment workflow is optional and is not required to run RickyGPT locally.

### GitHub Actions Secrets

```text
AWS_ROLE_ARN
DOCKERHUB_TOKEN
```

### GitHub Actions Variables

```text
AWS_REGION
EC2_INSTANCE_ID
DOCKERHUB_USERNAME
DOCKERHUB_IMAGE_NAME
```

Application API keys should not be stored inside the Docker image.

For an EC2 deployment, they can be stored in a server-side environment file such as:

```text
/opt/nova-ai-fastapi/.env
```

and supplied to Docker using:

```bash
--env-file /opt/nova-ai-fastapi/.env
```

---

## AWS Deployment Notes

An EC2 instance used with the GitHub Actions deployment workflow needs:

- Docker installed
- AWS Systems Manager Agent installed and running
- An EC2 IAM instance role
- `AmazonSSMManagedInstanceCore` attached to the EC2 IAM role
- Network access to Docker Hub
- Enough disk space for Docker images
- Port `8080` allowed through the security group if the application is accessed directly

GitHub authenticates to AWS using **OIDC**, avoiding the need to store long-lived AWS access keys in GitHub.

---

## Security

Sensitive values should be stored in environment variables and never committed to source control.

Examples include:

```text
Google API keys
Tavily API keys
LangSmith API keys
AWS credentials
Docker Hub access tokens
```

Recommended `.gitignore` entries:

```text
.env
__pycache__/
*.pyc
uploads/
data/
```

---

## Future Improvements

Potential improvements include:

- HTTPS and custom domain support
- User authentication
- Conversation rename and delete controls
- Improved document management
- Additional agent tools
- Multiple model providers
- Automated testing
- Production reverse proxy
- Improved observability and logging
- Cloud-native secret management

---

## Repository

GitHub:

```text
https://github.com/rt3438/RickyGPT
```

---

## Author

Built as a hands-on AI engineering project demonstrating:

- FastAPI development
- AI agent development
- LangChain / LangGraph
- Retrieval-Augmented Generation
- Streaming web applications
- Docker containerization
- GitHub Actions CI/CD
- AWS infrastructure integration
```

