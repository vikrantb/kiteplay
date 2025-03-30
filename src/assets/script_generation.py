import openai

def generate_script(prompt):
    """Generates a script using OpenAI."""
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    print(generate_script("Write a 30-second Holi celebration video script."))