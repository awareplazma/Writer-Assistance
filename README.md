# Writer Assistance

Writer Assistance is a personal project that uses Agentic Workflows to help writers brainstorm prose, plot points, and bounce ideas using the Gemini API (which will later be adapted to open-source Ollama).

**Note:** This project is currently in Linear Workflow mode and will be expanded into Agentic Workflows where inputs are self-iterative.

## Stack

- Python 3.10+
- FastAPI (Asynchronous API Framework)
- Google Gemini API
- HTML5 & Bootstrap 5 (Managed via npm)

## Project Architecture

- `main.py`: Handles API routing and static file serving
- `chatbot.py`: Manages Gemini sessions and prompt engineering
- `/static`: Contains the Bootstrap-powered UI
- `.venv`: Python Virtual Environment
- `node_modules`: Managed by npm for frontend assets like Bootstrap

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/awareplazma/Writer-Assistance.git
cd Writer-Assistance
```

### 2. Setup Python Environment

```bash
#This is to install tool for creating isolated virtual environment
pip install uv
```

### 3. Setup Frontend Assets

```bash
#Fetch non-Python dependencies
npm install
```

### 4. Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

### 5. Create .venv

```bash
uv sync
```

### 6. Start Command

```bash
#Use uv since the dependencies are in isolated .venv
uv run uvicorn main:app --reload
```

## Development Note

`.venv` and `node_modules` are kept separate to ensure the backend logic and frontend styling remain decoupled—making the app easier to scale or transition to a framework like React in the future.