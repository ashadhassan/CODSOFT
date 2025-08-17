# Rule-Based Chatbot (Task 1 - Codsoft AI Internship)
# By Ashad Hassan

import re

def chatbot_response(user_input):
    user_input = user_input.lower()

    # Simple if-else rules
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"
    elif "your name" in user_input:
        return "I am a simple chatbot created by Ashad Hassan for Codsoft Internship."
    elif "how are you" in user_input:
        return "I'm doing great, thank you! What about you?"
    elif "bye" in user_input or "exit" in user_input:
        return "Goodbye! Have a wonderful day!"

    # Regex pattern matching rules
    elif re.search(r"(time|current time)", user_input):
        return "I cannot check real-time clock yet, but you can use Python's datetime module for that."
    elif re.search(r"(weather|temperature)", user_input):
        return "I'm not connected to live weather, but it's always sunny in code world!"
    elif re.search(r"(help|support)", user_input):
        return "Sure! You can ask me about greetings, weather, or time."
    
    # Default fallback response
    else:
        return "Sorry, I don't understand that yet. Can you rephrase?"

# Chat loop
print("🤖 Chatbot is running! Type 'bye' to exit.\n")
while True:
    user = input("You: ")
    response = chatbot_response(user)
    print("Bot:", response)
    if "bye" in user.lower() or "exit" in user.lower():
        break
