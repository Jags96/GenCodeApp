# Code Generation App

This application uses a fine-tuned GPT-2 model to generate code based on natural language instructions. It consists of a FastAPI backend service for handling the model inference and a Streamlit frontend for user interaction.

## Project Structure

```
.
├── app.py                # FastAPI backend
├── utils.py              # Model utilities and inference code
├── streamlit_app.py      # Streamlit frontend
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile.api        # Dockerfile for the API service
└── Dockerfile.streamlit  # Dockerfile for the Streamlit service
```

## Setup Instructions

### Option 1: Running with Docker (Recommended)

1. Make sure you have Docker and Docker Compose installed.

2. Place your fine-tuned GPT-2 model in a directory named `model/` in the project root.

3. Build and start the services:
   ```bash
   docker-compose up -d
   ```

4. Access the Streamlit interface at [http://localhost:8501](http://localhost:8501)

### Option 2: Running Locally

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Update the `MODEL_PATH` in `utils.py` to point to your fine-tuned model.

3. Start the FastAPI backend:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

4. In a separate terminal, start the Streamlit frontend:
   ```bash
   streamlit run streamlit_app.py
   ```

5. Access the Streamlit interface at [http://localhost:8501](http://localhost:8501)

## Usage

1. Enter your code generation instructions in the text box.
2. (Optional) Use the advanced options to specify the programming language or adjust model parameters.
3. Click "Generate Code" to get the code based on your instructions.
4. The generated code will be displayed with syntax highlighting.
5. You can download the generated code using the download button.

## API Endpoints

- `POST /generate_code`: Generates code based on provided instructions
- `GET /health`: Health check endpoint

## Model Parameters

You can adjust the following parameters in the Streamlit interface:

- **Max Length**: Controls the maximum length of the generated code
- **Temperature**: Controls randomness in generation (higher = more random)
- **Top-p**: Nucleus sampling parameter
- **Top-k**: Top-k sampling parameter

## Customization

- To use a different model, update the `MODEL_PATH` in `utils.py`
- To modify the frontend layout and features, edit `streamlit_app.py`
- To add new API endpoints or functionality, edit `app.py`
