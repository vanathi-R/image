import google.generativeai as genai
import gradio as gr
from PIL import Image
import os

# Set up Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Replace with your API key

def generate_poem(image, prompt, language):
    """Generate a poem based on the image and prompt, optimized for speed."""
    if not language:
        return "Please select a language."

    model = genai.GenerativeModel("gemini-1.5-flash")  # Use a faster model

    # Convert and resize the image for faster processing
    img = image.convert("RGB")
    img = img.resize((256, 256))  

    # Optimized short prompt
    full_prompt = f"Generate a short poem in {language} based on this image and theme: {prompt}."

    # Generate poem without streaming
    response = model.generate_content([img, full_prompt])  
    output_text = response.text

    return output_text

# Gradio UI
iface = gr.Interface(
    fn=generate_poem,
    inputs=[
        gr.Image(type="pil"),  # Directly loads as PIL object
        gr.Textbox(label="Enter a theme for the poem (in English)"), 
        gr.Dropdown(
            ["Hindi", "Tamil", "Telugu", "Malayalam", "Kannada", "Marathi", "Bengali"], 
            label="Select Output Language"
        )
    ],
    outputs="text",
    title="Multilingual Image Poetry Generator",
    description="Upload an image, enter a theme in English, and get a poem in your chosen regional language."
)

# Run the app
if __name__ == "__main__":
    iface.launch()
