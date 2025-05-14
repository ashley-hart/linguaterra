from dotenv import load_dotenv
import os
import autogen
import world_generator

# Load environment variables from .env file
load_dotenv(dotenv_path="../../api/.env")

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Base config for all agents
llm_config = {
    "api_key": api_key,
    "model": "gpt-3.5-turbo",
    # "temperature": 0.2
}

# Expose functions/tools to be used in this pipeline

tools = [
    {
        "name": "create_world",
        "description": "Generates a new fantasy world with various parameters",
        "parameters": {
            "type": "object",
            "properties": {
                "biomes": {"type": "string", "enum": ["north", "northwest", "northeast", "south", "southwest", "southeast", "west", "east", "center"]},
                "technology_era": {"type": "string"},
                "climate_type": {"type": "string"}
            },
            "required": []
        },
        "function": world_generator.create_world
    },
    # Add other functions from your world_generator.py as needed
    {
        "name": "extract_world_data",
        "description": "Takes in a natural language input and creates a JSON object for the world generator. Call this to create parameters for the world generator",
        "parameters": {
            "type": "object",
            "properties": {
                "world_data": {"type": "object", "description": "The world data object"}
            },
            "required": ["world_data"]
        },
        "function": world_generator.generate_map
    }
]


# Configure agents
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "api_key": api_key,  # Replace with your API key
        "model": "gpt-3.5-turbo"            # Or another compatible model
    }
)


# Create agents with specific roles
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="TERMINATE",
#     max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "world_gen"}
)

# Parser agent
parser = autogen.AssistantAgent(
    name="Parser",
    system_message="""You extract world-building features from user descriptions.
    Analyze input text and identify key elements: geography, climate, cultures, magic systems, etc.
    Output a structured JSON with these features in a file named world_params.json.""",
    llm_config=llm_config
)

# Developer agent
developer = autogen.AssistantAgent(
    name="Developer",
    system_message="""You create worlds based on JSON specifications.
    Use the world_generator.create_world() and world_generator.generate_map() functions.
    Always validate your outputs before sharing.""",
    llm_config={
        **llm_config,
        "tools": [
            {
                "name": "create_world",
                "description": "Creates a world based on specifications",
                "function": world_generator.create_world
            },
            {
                "name": "generate_map",
                "description": "Generates ASCII map for a world",
                "function": world_generator.generate_map
            }
        ],
        "tool_choice": "auto"
    }
)

# Validator agent
validator = autogen.AssistantAgent(
    name="Validator",
    system_message="""You validate world maps against user requirements.
    Check for consistency, adherence to specifications, and overall quality.
    Provide specific feedback if improvements are needed.
    Only approve maps that fully meet the requirements.""",
    llm_config=llm_config
)

# Function to save JSON to file
def save_json(data, filename="world_specs.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    return f"JSON saved to {filename}"

# Add tool to user_proxy
user_proxy.register_function(
    function_map={"save_json": save_json}
)

# Set up the workflow
def process_world_request(user_description):
    # Step 1: Parser extracts features from user description
    parser_response = user_proxy.initiate_chat(
        parser, 
        message=f"Extract world-building features from this description: {user_description}"
    )
    
    # Extract JSON from parser response
    world_specs = parser.last_message()["content"]
    user_proxy.execute_function(
        function_name="save_json",
        arguments={"data": world_specs, "filename": "world_specs.json"}
    )
    
    # Step 2: Developer creates world based on specs
    max_iterations = 3
    iteration = 0
    world_approved = False
    
    while not world_approved and iteration < max_iterations:
        iteration += 1
        developer_response = user_proxy.initiate_chat(
            developer,
            message=f"Create a world and ASCII map based on these specifications: {world_specs}"
        )
        
        # Step 3: Validator checks the world
        validator_response = user_proxy.initiate_chat(
            validator,
            message=f"Validate this world against the original requirements: {user_description}\n\nWorld and map: {developer.last_message()['content']}"
        )
        
        # Check if validator approves
        if "approved" in validator.last_message()["content"].lower() or "satisfactory" in validator.last_message()["content"].lower():
            world_approved = True
        else:
            # Send feedback to developer for next iteration
            user_proxy.send(
                developer,
                f"Your world was not approved. Validator feedback: {validator.last_message()['content']}. Please revise."
            )
    
    return "World creation complete. Final result: " + developer.last_message()["content"]



# Define your task
task = """
Please use the tools provided to facilitate the process of generating 2D worlds. 
The input will be provided to you by the user proxy agent. The input will be a natural language prompt that describes a world. The agents in this pipeline are to do the following: 
"""

# Initiate the conversation
user_proxy.initiate_chat(
    assistant,
    message=task
)
# Example usage
# result = process_world_request("A mountainous fantasy world with three distinct kingdoms, a complex magic system based on elements, and numerous underground caverns.")