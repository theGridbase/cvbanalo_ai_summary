from regex import P
import requests
import time

from sympy import use

def test_stream_summary():
    # API endpoint
    url = "http://127.0.0.1:8000/create-summary/"

    # Payload for the API request
    payload = {
        "job_title": "Software Engineer",
        "experience": "5",
        "technical_skills": ["Python", "Java", "SQL"],
        "soft_skills": ["Communication", "Problem-solving"],
        "character_limit": 10000,
        "tone": "formal"
    }

    # Measure the time taken to receive the response
    start_time = time.time()
    
    try:
        # Make a streaming POST request
        response = requests.post(url, json=payload, stream=True, timeout=10)  # Added timeout to handle delays
        print(f"Initial response time: {time.time() - start_time:.2f} seconds", end="")

        if response.status_code == 200:
            # pass
            # print("Streaming the CV summary:\n")
            print(response.json())
            return response.json()['session_id']
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.Timeout:
        print("Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")

def reprompt(session_id, user_input=""):
    # API endpoint
    url = "http://127.0.0.1:8000/refine-summary/"
    
    # Payload for the API request
    payload = {
        "session_id": session_id,
        "user_input": user_input
    }
    
    try:
        # Make a POST request
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")
    

if __name__ == "__main__":
    session = test_stream_summary()
    user_input = "Kindly refine the summary to include more details about the technical skills."
    reprompt(session, user_input)
