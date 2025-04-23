import streamlit as st
import requests
import json
import time
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
import base64

# Configure the app
st.set_page_config(
    page_title="Code Generation App",
    page_icon="💻",
    layout="wide"
)

# API URL
API_URL = "http://localhost:8000"  # Update this if your API is hosted elsewhere

def generate_code(instruction, max_length=512, temperature=0.7, top_p=0.9, top_k=50):
    """Send request to the FastAPI backend to generate code"""
    try:
        response = requests.post(
            f"{API_URL}/generate_code",
            json={
                "instruction": instruction,
                "max_length": max_length,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()["generated_code"]
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def syntax_highlight(code):
    """Add syntax highlighting to the generated code"""
    try:
        # Try to guess the programming language
        lexer = guess_lexer(code)
        formatter = HtmlFormatter(style="monokai", cssclass="codehilite")
        highlighted = highlight(code, lexer, formatter)
        
        # Get CSS styles for the highlighted code
        css_styles = HtmlFormatter(style="monokai").get_style_defs('.codehilite')
        
        return highlighted, css_styles
    except Exception:
        # If lexer guessing fails, return the plain code
        return f"<pre>{code}</pre>", ""

def main():
    st.title("Code Generation App")
    st.markdown("Generate code using your fine-tuned GPT-2 model by providing instructions.")
    
    with st.sidebar:
        st.header("Model Parameters")
        max_length = st.slider("Max Length", min_value=64, max_value=1024, value=512, step=64,
                              help="Maximum number of tokens in generated code")
        temperature = st.slider("Temperature", min_value=0.1, max_value=1.5, value=0.7, step=0.1,
                                help="Higher values produce more diverse outputs")
        top_p = st.slider("Top-p (Nucleus Sampling)", min_value=0.1, max_value=1.0, value=0.9, step=0.05,
                         help="Cumulative probability threshold for token selection")
        top_k = st.slider("Top-k", min_value=1, max_value=100, value=50, step=1,
                         help="Number of highest probability tokens to consider")
        
        st.markdown("---")
        st.subheader("About")
        st.markdown("""
        This app uses a fine-tuned GPT-2 model to generate code based on natural language instructions.
        
        Simply enter your instructions in the text area and click 'Generate Code'.
        """)

    # Main area for code generation
    instruction = st.text_area("Enter your instructions:", 
                             height=150,
                             placeholder="Example: Write a Python function that calculates the Fibonacci sequence up to n terms.")
    
    # Advanced options (collapsible)
    with st.expander("Advanced Options", expanded=False):
        language_hint = st.text_input("Language Hint (optional)", 
                                    placeholder="e.g., python, javascript, java")
        st.markdown("Adding a language hint can improve the model's output.")
    
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("Generate Code", type="primary", use_container_width=True):
            if not instruction:
                st.warning("Please enter instructions first.")
            else:
                # Add language hint if provided
                full_instruction = instruction
                if language_hint:
                    full_instruction = f"Language: {language_hint}\n{instruction}"
                
                with st.spinner("Generating code..."):
                    # Create a placeholder for the progress bar
                    progress_placeholder = st.empty()
                    
                    # Simulate progress while waiting for the API
                    for percent in range(1, 101):
                        progress_placeholder.progress(percent)
                        time.sleep(0.01)
                    
                    # Generate code
                    code = generate_code(
                        full_instruction,
                        max_length=max_length,
                        temperature=temperature,
                        top_p=top_p,
                        top_k=top_k
                    )
                    
                    # Clear the progress bar
                    progress_placeholder.empty()
                    
                    if code:
                        # Display the generated code with syntax highlighting
                        st.session_state.generated_code = code
                        st.session_state.show_output = True
    
    with col2:
        st.empty()
    
    # Display generated code if available
    if 'show_output' in st.session_state and st.session_state.show_output:
        st.markdown("### Generated Code")
        
        # Apply syntax highlighting
        highlighted_code, css = syntax_highlight(st.session_state.generated_code)
        
        # Inject CSS for syntax highlighting
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        
        # Display highlighted code
        st.markdown(highlighted_code, unsafe_allow_html=True)
        
        # Create a download button for the code
        b64_code = base64.b64encode(st.session_state.generated_code.encode()).decode()
        
        extension = "txt"
        if 'language_hint' in st.session_state and st.session_state.language_hint:
            if st.session_state.language_hint.lower() == "python":
                extension = "py"
            elif st.session_state.language_hint.lower() in ["javascript", "js"]:
                extension = "js"
            elif st.session_state.language_hint.lower() == "java":
                extension = "java"
            # Add more mappings as needed
        
        href = f'<a href="data:text/plain;base64,{b64_code}" download="generated_code.{extension}" style="text-decoration:none;">Download Code</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        # Option to copy code to clipboard
        st.code(st.session_state.generated_code, language=language_hint.lower() if language_hint else None)

if __name__ == "__main__":
    main()