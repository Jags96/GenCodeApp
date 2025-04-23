import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os
from typing import Optional, Union, List

# Initialize model and tokenizer
MODEL_PATH = os.environ.get("MODEL_PATH", "your-finetuned-gpt2-model-path")

# Load model and tokenizer (do this once at module level)
try:
    tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH)
    model = GPT2LMHeadModel.from_pretrained(MODEL_PATH)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    model.eval()  # Set to evaluation mode
    print(f"Model loaded successfully on {device}")
except Exception as e:
    print(f"Error loading model: {e}")
    # In production, you might want to raise an exception here

def generate_code(
    instruction: str,
    max_length: int = 512,
    temperature: float = 0.7,
    top_p: float = 0.9,
    top_k: int = 50,
    num_return_sequences: int = 1
) -> str:
    """
    Generate code based on the provided instruction using the fine-tuned GPT-2 model.
    
    Args:
        instruction: The instruction for code generation
        max_length: Maximum length of generated code
        temperature: Controls randomness in generation (higher = more random)
        top_p: Nucleus sampling parameter
        top_k: Top-k sampling parameter
        num_return_sequences: Number of sequences to generate
        
    Returns:
        Generated code as a string
    """
    try:
        # Format input based on how your model was fine-tuned
        # You might need to adjust this based on your specific fine-tuning format
        input_text = f"Instruction: {instruction}\nCode:"
        
        # Tokenize input
        input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)
        
        # Generate
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                num_return_sequences=num_return_sequences,
                pad_token_id=tokenizer.eos_token_id,
                do_sample=True
            )
        
        # Decode the generated output
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Extract just the code part (remove the instruction)
        # You might need to adjust this based on your model's output format
        if "Code:" in generated_text:
            generated_code = generated_text.split("Code:", 1)[1].strip()
        else:
            generated_code = generated_text.replace(input_text, "").strip()
            
        return generated_code
    
    except Exception as e:
        print(f"Error in code generation: {e}")
        raise e

def clean_generated_code(code: str) -> str:
    """
    Clean up the generated code by removing any unwanted artifacts.
    
    Args:
        code: Raw generated code
        
    Returns:
        Cleaned code
    """
    # Add any post-processing logic here if needed
    return code.strip()