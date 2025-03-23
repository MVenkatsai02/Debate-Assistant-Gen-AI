import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI-Powered Debate Assistant", layout="wide")

# Sidebar for API Key Upload
st.sidebar.title("🔑 Upload API Key")
st.sidebar.markdown("""
- [Get Google Gemini API Key](https://aistudio.google.com/app/apikey)  
""")

# API Key Input
gemini_api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

# Ensure API key is provided
if not gemini_api_key:
    st.sidebar.warning("Please enter your API key to proceed.")
    st.stop()

# Initialize Gemini API
genai.configure(api_key=gemini_api_key)

# Streamlit App Main Interface
st.title("🗣️ AI-Powered Debate Assistant")
st.subheader("Get AI-generated arguments for both sides of any debate topic!")

# User Input
debate_topic = st.text_area("Enter Debate Topic:", "Should AI replace human teachers?")
debate_format = st.selectbox("Select Debate Style:", ["Formal", "Casual", "Point-Counterpoint"])
include_references = st.checkbox("Include References & URLs")

# Function to generate debate arguments
def generate_debate_arguments(topic, style, include_references):
    prompt = f"""
    Generate a structured debate on: "{topic}" in a "{style}" style.
    Provide:
    - A clear opening statement for both Pro and Con sides.
    - Three key arguments supporting both sides.
    - A strong counterargument for each point.
    - A concluding statement for both sides.
    {"Include references and URLs for further research." if include_references else ""}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text if response else "Sorry, I couldn't generate the debate."

# Generate Debate
if st.button("Generate Debate Arguments"):
    with st.spinner("Generating debate arguments..."):
        debate_text = generate_debate_arguments(debate_topic, debate_format, include_references)
    
    # Display Debate Arguments
    st.subheader("📝 Debate Arguments")
    st.write(debate_text)

    # Download Debate as Text File
    st.download_button(
        label="📥 Download Debate Script",
        data=debate_text,
        file_name=f"{debate_topic.replace(' ', '_')}_debate.txt",
        mime="text/plain",
    )

# Run the app using:
# streamlit run debate_assistant.py
