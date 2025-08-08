import os
import toml
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load OpenAI API key from secrets.toml
here = os.path.dirname(__file__)  # Gets directory of this file (backend/)
secrets_path = os.path.join(here, "secrets.toml")
secrets = toml.load(secrets_path)
api_key = secrets["openai"]["api_key"]

# Initialize LangChain ChatOpenAI model
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.2,
    openai_api_key=api_key
)

def clean_query(user_input):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert query cleaner."),
        ("user", 
        """
You are a smart language interpreter. Your job is to:
- Understand the user's query.
- Fix broken grammar or informal English.
- Translate Bangla or any language to English.
- Make the query formal, clear, and grammatically correct.

Here is the user query:
\"\"\"{user_input}\"\"\"

Return only the cleaned English version of the query.
        """)
    ])

    chain = prompt_template | llm
    response = chain.invoke({"user_input": user_input})
    return response.content.strip()

if __name__ == "__main__":
    user_query = input("Enter your query: ")
    cleaned = clean_query(user_query)
    print("Cleaned Query:", cleaned)
