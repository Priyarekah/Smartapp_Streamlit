# NLP-AMILI

## Setup Instructions

### 1. Create & Activate Virtual Environment
```bash
virtualenv env
source env/Scripts/activate
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Create secrets.toml File
Create a file called secrets.toml under a folder called .streamlit. Your directory structure should look like this:
```css
your-repository/
├── .streamlit/
│   └── secrets.toml
├── main.py
└── requirements.txt
```
### 4. Set Credentials
Edit the secrets.toml file with your credentials for OpenAI, OpenRouter, MongoDB, and PostgreSQL:

```toml
OPENAI_API_KEY = ""
OPENAI_MODEL = "gpt-3.5-turbo"
OPENROUTER_API_KEY = ""

MONGODB_PAPER = "Connection URL"
MONGODB_CHAT = "Connection URL"
MONGO_DB = "insightdb"
MONGO_COLLECTION = "paper_demo"

[connections.postgresql]
dialect = "postgresql"
host = "localhost"
port = "5432"
database = ""
username = ""
password = ""
```
### 5. Run the App
Run the app in your browser with the following command:
```bash
streamlit run main.py
```
