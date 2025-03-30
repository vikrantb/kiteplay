import openai

def generate_image(prompt):
    """Generates an image using DALL-E."""
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024"
    )
    return response['data'][0]['url']

if __name__ == "__main__":
    print(generate_image("A vibrant Holi festival at Mumbai beach with people throwing colors."))