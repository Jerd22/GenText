import google.generativeai as genai

GOOGLE_API_KEY=('AIzaSyBgYZEqneUOhc7qZOL62S0tt2RtuecHw_Q')
# Configure the GEMINI LLM
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

#basic generation
def generate_text(prompt, images):
    response = model.generate_content([prompt, images])
    return response.text