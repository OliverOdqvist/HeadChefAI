from headchef_interface import query_llm



def chat():
    print("💬")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        elif user_input.strip() == "":
            continue
        try:
            response = query_llm(user_input)
            print("Bot:", response)
        except Exception as e:
            print("❌ Error:", e)

if __name__ == "__main__":
    chat()