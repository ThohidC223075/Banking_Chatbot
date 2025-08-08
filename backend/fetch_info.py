import os
import toml
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# === Load API Key from secrets.toml ===
here = os.path.dirname(__file__)  # Gets directory of this file (backend/)
secrets_path = os.path.join(here, "secrets.toml")
secrets = toml.load(secrets_path)
openai_api_key = secrets["openai"]["api_key"]

# === Setup Embedding Model and Vector DB ===
embedding = OpenAIEmbeddings(api_key=openai_api_key)
vectordb = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

# === Setup LLM (GPT) ===
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    api_key=openai_api_key
)

# === Prompt Template (Multilingual & Context-aware) ===
custom_prompt = PromptTemplate.from_template("""
You are a helpful assistant for a question-answering task using retrieved documents.

Instructions:
- Detect the language of the user's question.
- Respond in the **same language** as the user's input.
- Only use the context (retrieved documents) to answer the question.
- If the answer is not present in the documents, say: "Sorry, I don't have enough information to answer that."

User's input language hint: {language_hint}

Question: {query}

Context:
{context}

Answer:
""")

# === Helper Function: Format Retrieved Documents ===
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# === Main Function to Use in App ===
def answer_query(query: str, user_input: str):
    """
    Process user's query and return an answer using context-based retrieval and language-aware prompt.
    
    Args:
        query (str): cleaned question for retrieval
        user_input (str): original user query (used for language detection)
    
    Returns:
        answer (str): final LLM response
        source_docs (List[str]): context documents used for the response
    """
    print(f"\n[User Input] {user_input}")
    print(f"[Cleaned Query] {query}")

    # Step 1: Retrieve top-k documents
    source_docs = vectordb.similarity_search(query, k=3)
    formatted_context = format_docs(source_docs)

    # Step 2: Format the prompt manually
    prompt_input = custom_prompt.format_prompt(
        query=query,
        context=formatted_context,
        language_hint=user_input
    ).to_string()

    print("\n=== Final Prompt Sent to GPT ===")
    print(prompt_input)

    # Step 3: Get answer from LLM
    result = llm.invoke(prompt_input)
    
    # Step 4: Extract content from result
    if hasattr(result, "content"):
        answer = result.content
    elif isinstance(result, dict) and "content" in result:
        answer = result["content"]
    else:
        answer = str(result)

    print("\n=== Retrieved Source Documents ===")
    for i, doc in enumerate(source_docs, start=1):
        print(f"Source {i}:\n{doc.page_content}\n")

    return answer, [doc.page_content for doc in source_docs]

# === Run Directly (Standalone) ===
if __name__ == "__main__":
    # Example default input (you can change this)
    user_input = "Is there any student account available in UCB?"
    cleaned_query = user_input  # If you have a cleaner, apply it here

    # Call the main function
    answer, sources = answer_query(cleaned_query, user_input)

    print("\n=== Final Answer ===")
    print(answer)

    print("\n=== Sources ===")
    for i, src in enumerate(sources, start=1):
        print(f"Source {i}:\n{src}\n")
