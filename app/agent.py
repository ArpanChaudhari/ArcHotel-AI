import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Import the database function from our db package
from app.db.crud import search_hotels, get_hotel_details, reserve_room, cancel_reservation

# load env variables
load_dotenv(override=True)

# Initialize OpenAI Client using Groq's API
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-120b"

system_message = """ 
You are ArcHotels Booking Agent and Advisor.
You help customers find and book hotels that meets their budgets and constraints in India.

Important rules you must follow:
1. If the user has not yet provided check-in and check-out dates, ask for them.
2. Never attempt to search for hotels without Both check-in and check-out.
3. When calling the `search_hotesls` tool, Always include:
    - city
    - max_price (tool budget)
    - checkin
    - checkout
4. Treat max_price as the total budget for the whole stay, not per night.
5. Convert total budget innto a per-night budget internally (max_price / nights).
6. Do not attempt to reason about hotels withoutn calling the tool.
7. If data is missing (dates, budget), ask a clear question.
8. If booking is requested, call the `reserve_room` tool.
9. Do not invent hotel names, price, or features.
Be concise and professional.
10. If cancellation is requested, ask for the confirmation code and guest name, then call the `cancel_reservation` tool.
"""

# Search Hotels Tool
search_hotels_tool = {
    "name": "search_hotels",
    "description": "Search for hotels based on city, price, amenities, stars, and stay dates.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string"},
            "max_price": {"type": "number"},
            "required_amenities": {"type": "array", "item": {"type": "string"}},
            "min_stars": {"type": "number"},
            "checkin": {"type": "string", "description": "YYYY-MM-DD format"},
            "checkout": {"type": "string", "description": "YYYY-MM-DD format"},
        },
        "required": ["city"],
        "additionalProperties": False,
    },
}

# Get Hotels details Tool
get_details_tool = {
    "name": "get_hotel_details",
    "description": "Get detailed information about a specific hotel.",
    "parameters": {
        "type": "object",
        "properties": {"hotel_name": {"type": "string"}},
        "required": ["hotel_name"],
        "additionalProperties": False,
    },
}

# Reserve Room Tool
reserve_room_tool = {
    "name": "reserve_room",
    "description": "Reserve a room at a hotel.",
    "parameters": {
        "type": "object",
        "properties": {
            "hotel_name": {"type": "string"},
            "room_type": {"type": "string"},
            "guest_name": {"type": "string"},
            "checkin": {"type": "string", "description": "YYYY-MM-DD format"},
            "checkout": {"type": "string", "description": "YYYY-MM-DD format"},
        },
        "required": ["hotel_name", "room_type", "guest_name", "checkin", "checkout"],
        "additionalProperties": False,
    },
}

# Cancel Reservation Tool
cancel_reservation_tool = {
    "name": "cancel_reservation",
    "description": "Cancel an existing hotel reservation.",
    "parameters": {
        "type": "object",
        "properties": {
            "confirmation_code": {"type": "string"},
            "guest_name": {"type": "string"},
        },
        "required": ["confirmation_code", "guest_name"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": search_hotels_tool},
    {"type": "function", "function": get_details_tool},
    {"type": "function", "function": reserve_room_tool},
    {"type": "function", "function": cancel_reservation_tool},
]


# Dedicated Helper Function: Process the Tool Call
def handle_tools_calls(message):
    responses = []

    for tool_call in message.tool_calls:
        function_name = tool_call.function.name  # we grab tool call in this phase
        arguments = json.loads(tool_call.function.arguments)  # Parse the JSON argument

        # Run the Python function
        if function_name == "search_hotels":
            result = search_hotels(**arguments)
        elif function_name == "get_hotel_details":
            result = get_hotel_details(**arguments)
        elif function_name == "reserve_room":
            result = reserve_room(**arguments)
        elif function_name == "cancel_reservation":
            result = cancel_reservation(**arguments)
        else:
            result = "Error: Unknown function."

        # assign the formatted tool result
        responses.append(
            {"role": "tool", "content": str(result), "tool_call_id": tool_call.id}
        )

    return responses


def chat(message, history):
    # Convert Grodio history formate to OpenAI Message formate
    formatted_history = [{"role": h["role"], "content": h["content"]} for h in history]

    # Set up our System Instruction, formatted history and user message
    messages = (
        [{"role": "system", "content": system_message}]
        + formatted_history
        + [{"role": "user", "content": message}]
    )

    # Call the model
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=tools
    )

    # Keep looping as long as the AI wants to use tools!
    while response.choices[0].message.tool_calls:
        message_response = response.choices[0].message

        # Process ALL requested tool calls using our new helper function
        tool_responses = handle_tools_calls(message_response)

        # Append the AI's request and our results to the message history
        messages.append(message_response)
        messages.extend(tool_responses)

        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=tools
        )

    final_content = response.choices[0].message.content

    if final_content is None:
        return (
            "I've updated my database based on your request. How else can I help?"
        )

    return final_content
