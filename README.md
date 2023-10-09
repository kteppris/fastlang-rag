# fastlang-rag

**Project Origin:** Development of a Chatbot-API for University Services at Technische Hochschule Lübeck.
**Status:** The project is still in development, conversational feature have not been implemented jet.

---

## Overview

`fastlang-rag` is a derivative of a prototype project aimed at creating a Chatbot-API that engages with different contents like PDFs and Websites. Originally designed to interact with the University content, this Chatbot can answer questions based on content in a vectorestore through a REST-API. It supports various pre-trained models, notably from Hugging Face and OpenAI and can easly extend with adding new YAML configs.

---

## Project Goals

1. Design a Chatbot API that interacts with content.
2. Enable the Chatbot to provide foundation-related answers.
3. Support integration with various pre-trained models, primarily from Hugging Face and OpenAI.
4. Ensure the system is scalable and maintainable by an adept team.

---

## Use Cases

- **Question Answering**: Provide responses to user queries using the Chatbot.
- **Model Switching**: Allow underlying model changes, to easly evaluate the capabilities of different Open Source LLMs.
- **Knowledgebase Update**: Refresh the vector database with fresh information.
- **Suitability and Feasibility**: Evaluate the practicality and relevance of use cases based on user demands, compatibility with other Chatbot functions, resources, capabilities, and projected costs.

---

## Repository Structure

```
.
├── app
│   ├── .env-template
│   ├── main.py
│   ├── ...
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Development & Debugging

Local development is supported via a Docker Compose setup, complemented by a `devcontainer` configuration for Visual Studio Code (VSC). When you work locally, the FastAPI Server of the Chatapi won't initiate automatically. You need to trigger it manually. This configuration supports debugging capabilities. For debugging steps in VSC, refer to the launch configuration named **"Python: FastAPI"**.

---

## Deployment

The original project was designed for deployment within a Kubernetes cluster. Due to security reasons, detailed Kubernetes deployment instructions have been excluded from this public version. However, for local testing and development purposes, you can utilize the provided `docker-compose` file.

To run the project using Docker Compose:

```bash
docker-compose up --build
```

Once started, you can access the application locally.

---

## Usage

#### Endpoints:

**Answer Questions**
```http
POST /chat/
Body: 
{
  "question": "Your question here"
}
```

**Fetch Sources**
```http
GET /sources/
```

**Search Documents**
```http
POST /query/
Body: 
{
  "query": "Your search query here"
}
```

---

## Configuration

The application is configured using `hydra` and `OmegaConf`. Different configurations for vector stores, encoders, data sources, chains, and readers can be found within their respective directories in the project structure. By utlizing the power of hierarchical configuration and config  composition, this app adds the possibillity to use langchain as an abstraction layer to access various of different LLMs and other compotents by simply adding or changing the YAML config files.
