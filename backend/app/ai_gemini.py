import google.generativeai as genai

def generate_learning_content(prompt: str) -> str:
    genai.configure(api_key="YOUR_GEMINI_API_KEY")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text
