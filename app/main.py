import gradio as gr
from app.db.seed import initialize_database
from app.agent import chat

def start_app():
    # 1. Ensure the database is created and seeded with hotels data
    print("Initializing Database...")
    initialize_database()
    print("Database initialized successfully.")

    # 2. Set up the Gradio Chat Interface
    print("Starting Gradio Web Interface...")
    demo = gr.ChatInterface(
        fn=chat,
        title="Hotelia (The ArcHotels Booking Agent and Advisor)",
        description="I can help you find and book the perfect hotel in India! Just tell me your destination, budget, and stay dates.",
        examples=[
            "Find me a 5-star hotel in Mumbai.",
            "I need a hotel in Goa with a pool. My budget is ₹50000 for 3 nights.",
            "What hotels are available in Ahmedabad?"
        ]
    )

    # 3. Launch the app
    demo.launch(
        inbrowser=True, 
        auth=("admin", "arc2026")
    )

if __name__ == "__main__":
    start_app()