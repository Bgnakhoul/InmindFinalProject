# Project Title: HR headhunter

## Project Overview
The main idea behind this project is a multi-agent system made of two agents that communicate via A2A protocol. The first agent is made using `google-adk` and the second is made using `LangGraph` framework. The first agent takes a raw job description for a job, for example "We are in need of a Software Engineer to design and develop scalable software. The candidate will write clean code, collaborate on features, and optimize performance. Requires proficiency in Python, Java, or JavaScript...", this agent (agent 1) will transform this Job Description into clear and consice bullet points, it might ask for more information from the user. After,  recieving enough information about the job it will pass this new parsed Job Description to agent 2. Now agent 2 will have to use a RAG tool, passing to it the correct parameters and parsed job description to search for k (by default k = 5) most ideal candidates from a folder of resumes collected from the internet and will then return them to agent 1.
![Demo Screenshot](images/Screenshot%202025-08-22%20043726.png)


---

## Setup & Usage Instructions

### Installation
1.  Clone the repository: `git clone <https://github.com/Bgnakhoul/InmindFinalProject.git>`

### Prerequisites

Before running the application locally, ensure you have the following installed:

1. **uv:** The Python package management tool used in this project. Follow the installation guide: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

## Run the Agents

You will need to run each agent in a separate terminal window. The first time you run these commands, `uv` will create a virtual environment and install all necessary dependencies before starting the agent.

### Terminal 1: Run Kaitlynn Agent
```powershell
cd search_agent_RAG
uv venv
.venv\Scripts\activate
uv run --active app/__main__.py
```

### Terminal 2: Run Host Agent
```powershell
cd host_agent_adk
uv venv
.venv\Scripts\activate
uv run --active adk web      
```

---

## The Engineering Log

### i) Iterative Design
#### Version 1:

The original idea was a workflow that looked like this:
Agent 1 (LangGraph) --> Agent 2 (LangGraph) --> Agent 3 (ADK)
The concept was a bit similar but more complex.

Agent 1: the job description parser (transforms raw job description into bullet points)

Agent 2: Takes bullet points and call RAG tool to get best candidates and passes them to Agent 3

Agent 3: Takes best candidates, then asks user for his schedule (PDF format) and tries to fit interviews for the candidates in the schedule

This approach was too complex to implement especially as I approached towards A2A

MCP server worked

This approach was not implemented

Days spent: 3-4 days

#### Version 2:
I found out a very helpful guide on youtube [Tutorial link](https://www.youtube.com/watch?v=mFkw3p5qSuA&t=3829s) for using A2A. Here I changed my architecture to this:

IMAGE siuadhaudsashdhsaiduauiadsh

Workflow:

Agent 1: the ADK job description parser (transforms raw job description into bullet points)

Agent 2: Takes bullet points and calls RAG tool to get best candidates and passes them back to Agent 1

Agent 1: Takes best candidates and asks user questions about his schedule.

Agent 3: Takes infomation from Agent 1 about candidates and schedule, and tries to fit interviews for the candidates in the schedule.

Agent 1: Takes the proposed schedule from Agent 3 and tells the user about it

This approach was not implemented because I noticed that there is no need for Agent 3 because Agent 1 can do all the work.

#### Version 3 (Final version):

Agent 1: the ADK job description parser (transforms raw job description into bullet points)

Agent 2: Takes bullet points and calls RAG tool to get best candidates and passes them back to Agent 1

The goal was also to make Agent 1 a scheduling agent but I spent too much time debugging A2A protocol between Agent 1 and Agent 2, so I wasn't able to implement my full idea.


### ii) Experiment Tracker
A record of experiments, tests, and their outcomes. Essential for tracking what works and what doesn't.

| Experiment ID | Goal                          | Parameters/Changes                                  | Outcome                                     | Conclusion/Next Step                         |
| :------------ | :---------------------------- | :-------------------------------------------------- | :------------------------------------------ | :------------------------------------------- |
| EXP-001       | Improve output formatting     | Used library `A` vs. custom function `B`            | Library `A` was 70% slower but more robust. | Proceed with custom function `B` for now.    |
| EXP-002       | Optimize API call latency     | Implemented request batching (batch size=5)         | Reduced total number of calls by 80%.       | **Success.** Implement in main branch.       |

### iii) Prompt Versioning
#### Version 1:










## Referencing and AI Collaboration
This section transparently documents the use of AI tools and external resources.

### AI Assistance
*   **ChatGPT (GPT-4):** Used for initial project scaffolding, generating boilerplate code, and debugging assistance.
*   **Claude 3 Opus:** Consulted for optimizing database query structure and generating documentation templates.
*   **GitHub Copilot:** Used for inline code suggestions and autocompletion throughout development.

### External Resources & Libraries
*   **[Library Name](https://link-to-library.com)**: v1.2.3 - Brief description of its purpose in the project.
*   **[Tutorial/Article Name](https://link-to-article.com)**- Concept or code snippet that was influential.
*   **Dataset: [Dataset Name](https://link-to-dataset.com)** - Source of any data used.






















































