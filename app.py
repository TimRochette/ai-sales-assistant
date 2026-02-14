import streamlit as st
import openai
from PyPDF2 import PdfReader

# 1. UI Setup
st.set_page_config(page_title="AI Sales Assistant", layout="wide")
st.title("🚀 Technical Sales Query Tool")
st.markdown("Extract specific requirements from complex PDFs in seconds.")

# 2. Sidebar for Configuration
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    uploaded_file = st.file_uploader("Upload an RFP or Security PDF", type="pdf")

# 3. Processing Logic
if uploaded_file and api_key:
    openai.api_key = api_key
    
    # Extract text from PDF
    reader = PdfReader(uploaded_file)
    raw_text = ""
    for page in reader.pages:
        raw_text += page.extract_text()
    
    st.success("Document Analyzed! What do you need to find?")

    # 4. Interactive Chat
    user_question = st.text_input("Example: 'Does this vendor support SAML 2.0?'")
    
    if user_question:
        # We send the text + the question to the AI
        # Note: For massive PDFs, you'd use a Vector DB (RAG), but for a 30m demo, this works!
        prompt = f"Using the following document text, answer the question. If the answer isn't there, say you don't know.\n\nDocument: {raw_text[:8000]}\n\nQuestion: {user_question}"
        
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        st.subheader("Answer:")
        st.write(response.choices[0].message.content)
