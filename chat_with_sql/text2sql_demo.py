
import os
import re
import getpass
from langchain_community.utilities import SQLDatabase
from langchain.chat_models import init_chat_model

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


def generate_base_sql_query(schema, question):
    """Generate initial SQL query from user question."""
    prompt = f"""Based on the table schema below, write a SQL query that would answer the user's question.
    Return only the raw SQL query, without markdown formatting (e.g., no ```sql blocks) and explanations or additional text.
    
    Schema: {schema}
    Question: {question}
    
    SQL Query:"""
    return prompt

def generate_follow_up_sql_query(schema, context, follow_up_question, previous_query, previous_result):
    """Generate SQL for follow-up questions using context from previous queries."""
    prompt = f"""Based on the previous conversation context and table schema, write a SQL query for the follow-up question.
    Return only the raw SQL query, without markdown formatting (e.g., no ```sql blocks) and explanations or additional text.
    
    Schema: {schema}
    Previous Question: {context}
    Previous SQL Query: {previous_query}
    Previous Result: {previous_result}
    Follow-up Question: {follow_up_question}
    
    SQL Query:"""
    return prompt


def clean_sql_output(sql_text):
    """Remove markdown formatting from SQL query."""
    return re.sub(r"^```sql\s*|\s*```$", "", sql_text.strip(), flags=re.IGNORECASE).strip()


def execute_prompt(prompt):
    answer = llm.invoke(prompt).content
    cleaned_answer = clean_sql_output(answer)
    print("\n\n")
    print(cleaned_answer)

    result = db.run(answer)
    print("\n\n")
    print(result)
    return cleaned_answer, result


db = SQLDatabase.from_uri("sqlite:///nba_roster.db", sample_rows_in_table_info=0)
db_schema = db.get_table_info()

llm = init_chat_model("gpt-4o-mini", model_provider="openai")

question = "What team is Stephen Curry on?"
prompt = generate_base_sql_query(db_schema, question)
answer, result = execute_prompt(prompt)

follow_up_question = "What's his salary?"
prompt = generate_follow_up_sql_query(db_schema, context=question, follow_up_question=follow_up_question, previous_query=answer, previous_result=result)
answer, result = execute_prompt(prompt)
