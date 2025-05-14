from dotenv import load_dotenv
import os
import autogen

# Load environment variables from .env file
load_dotenv(dotenv_path="../../api/.env")

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Configure agents
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "api_key": api_key,  # Replace with your API key
        "model": "gpt-3.5-turbo"            # Or another compatible model
    }
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
)

# Define your task
task = """
Please create a Python script that:
1. Reads data from a CSV file named 'data.csv'
2. Calculates the average of the 'score' column
3. Generates a bar chart of the results
4. Saves the chart as 'results.png'
"""

# Initiate the conversation
user_proxy.initiate_chat(
    assistant,
    message=task
)