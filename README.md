# ArcHotel-AI 🏨🤖

ArcHotel-AI is an interactive, AI-powered hotel booking assistant. It helps users search, explore, book, and cancel hotel reservations across various cities in India. The agent is powered by Groq's high-speed LLM infrastructure (using models like LLaMA 3.1) and integrates directly with a local SQLite database to provide realistic room availability, dynamic pricing, and immediate confirmations.

## Features ✨

*   **Conversational Search**: Search for hotels based on city, stay dates, budget constraints, required amenities, and star ratings using natural language.
*   **Detailed Insights**: Ask the AI for specific hotel details, room types, and availability.
*   **Instant Booking**: Reserve a room and receive a unique confirmation code. The database automatically updates available room counts.
*   **Reservation Management**: Cancel existing reservations using a confirmation code and guest name, automatically freeing up the room.
*   **Web Interface**: A clean, responsive chat interface built with Gradio for easy user interaction.

## Tech Stack 🛠️

*   **Backend / Database**: Python, SQLite3
*   **AI / LLM Integration**: Groq API (via OpenAI Python SDK)
*   **Frontend / UI**: Gradio

## Project Structure 📁

```text
ArcHotel-AI/
├── app/
│   ├── db/
│   │   ├── connection.py  # SQLite connection setup
│   │   ├── schema.py      # Database table structures
│   │   ├── data.py        # Seed data for Indian hotels and room types
│   │   ├── crud.py        # Database operations (search, book, cancel)
│   │   └── seed.py        # Logic to populate the database on first run
│   ├── agent.py           # AI logic, system prompt, and tool-call routing
│   └── main.py            # Application entry point and Gradio UI setup
├── .env                   # Environment variables (API keys)
├── requirements.txt       # Python dependencies
└── arc_hotels.db          # SQLite database
```

## Setup & Installation 🚀

### 1. Clone the repository
Ensure you have the project files on your local machine.

### 2. Set up a virtual environment (Recommended)
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory (if it doesn't exist) and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application
Start the Gradio web interface. The application will automatically initialize and seed the database if it's running for the first time.
```bash
python -m app.main
```

## Usage 💬

Once the application is running, a local URL (usually `http://127.0.0.1:7860`) will be provided in your terminal. Open this URL in your browser and log in with:
*   **Username**: `admin`
*   **Password**: `arc2026`

Start chatting with the AI! Try prompts like:
*   *"Find me a 5-star hotel in Mumbai for under ₹20000 total from tomorrow to next Friday."*
*   *"I'd like to book a Deluxe room at the Riverfront Grand Hotel for John Doe from 2026-10-01 to 2026-10-05."*
*   *"Cancel my reservation. My code is AB12CD34 and my name is John Doe."*
