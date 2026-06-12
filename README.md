# KineWeave – AI-Powered Personal Productivity Assistant
## Overview

KineWeave is an AI-powered productivity and personal knowledge management system that helps users capture thoughts, tasks, goals, reminders, meetings, ideas, and notes through text or voice inputs. The system automatically analyzes user inputs using Large Language Models (LLMs), generates actionable plans, tracks progress, retrieves historical information through semantic search, and provides intelligent daily summaries.

The goal of KineWeave is to act as a second brain that helps users organize, remember, plan, and execute their personal and professional activities efficiently.

## Problem Statement

Modern productivity tools focus primarily on storing information.

Users often need to manually organize notes, categorize tasks, create reminders, and maintain context across multiple applications.

KineWeave aims to simplify this process by automatically understanding user intent and extracting meaningful information from natural language inputs.

## Key Features
1. Intelligent Capture System

Users can enter information through:

* Text input
* Voice input

The AI automatically:

* Detects intent
* Extracts entities
* Assigns priority
* Generates tags
* Categorizes information

2. Multi-Intent Analysis

A single user input may contain multiple thoughts.

Example:

"I have an interview at 5 PM and need to order shoes."

KineWeave automatically splits this into:

* Interview at 5 PM
* Order shoes

Each item is analyzed and stored independently.

3. Automatic Action Plan Generation

The Planner Engine converts goals and tasks into step-by-step action plans.

Example:
Goal:
"Learn LangChain"
Generated Plan:
* Understand LLM fundamentals
* Learn prompt engineering
* Study LangChain architecture
* Build a simple chatbot
* Deploy a project
 
 4. Progress Tracking

Users can:
* View generated plans
* Mark steps as completed
* Track overall progress

5. Daily Summary Engine
Generates personalized productivity summaries.

Includes:

* Pending tasks
* High-priority items

6. Dashboard Analytics

Provides insights including:

* Total Captures
* Total Action Plan Steps
* Completed Tasks
* Pending Tasks

7. Semantic Memory System

KineWeave includes a long-term memory system using ChromaDB.

Features:

* Semantic search over historical captures
* Context-aware retrieval
* Memory exploration interface
* Related action plan retrieval

Example Queries:

What interview do I have?
What goals am I working on?
What did I note about LangChain?
What task was related to shopping?

## Technology Stack
### Backend
* FastAPI
* SQLAlchemy
* MySQL
* Pydantic
### Frontend
* Streamlit
* AI & NLP
* Large Language Models (LLMs)
* Prompt Engineering
* Intent Classification
* Entity Extraction
* Tag Generation
### Memory Layer
* ChromaDB
* Semantic Retrieval

# Running KineWeave

## Prerequisites

Install:

* Python 3.11+
* MySQL Server
* Git

---

## Step 1: Clone Repository

```bash
git clone <repository_url>
cd KineWeave
```

---


## Step 2: Install Dependencies

Backend:

```bash
pip install -r requirements.txt
```
---

## Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=kineweave

GROQ_API_KEY=your_groq_api_key
```

---

## Step 4: Start Backend

Navigate to backend folder:

```bash
cd backend
```

Run:

```bash
uvicorn app.main:app --reload
```

Backend will start on:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Step 5: Start Frontend

Open a second terminal.

Navigate to frontend folder:

```bash
cd frontend
```

Run:

```bash
streamlit run app.py
```

Frontend will start on:

```text
http://localhost:8501
```



## Future Enhancements
* Email Notifications
* Desktop Notifications
* Calendar Integration
* Advanced RAG-based Memory Retrieval
* Mobile Application
* Multi-User Authentication
* Agentic Task Execution
 

## Project Highlights
* Built an end-to-end AI productivity assistant.
* Implemented intelligent capture processing with LLM-based analysis.
* Developed automatic action plan generation and progress tracking.
* Designed a semantic memory system using vector databases.
* Created a personalized daily summary engine.
* Integrated analytics dashboards and goal management workflows.