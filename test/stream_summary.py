import requests
import time
import sys

def test_stream_summary_with_typing_effect():
    # API endpoint
    url = "http://127.0.0.1:8000/stream-summary/"

    # Payload for the API request
    payload = {
        "job_title": "Software Engineer",
        "experience": "5",
        "technical_skills": ["Python", "Java", "SQL"],
        "soft_skills": ["Communication", "Problem-solving"],
        "character_limit": 10000,
        "tone": "formal"
    }

    try:
        # Make a streaming POST request
        with requests.post(url, json=payload, stream=True, timeout=10) as r:
            if r.status_code == 200:
                print("Streaming the CV summary:\n")
                start = time.time()
                # Simulate typing effect by printing each chunk with a small delay
                for chunk in r.iter_content(100):  # Process each byte as it's received
                    if chunk:
                        sys.stdout.write(chunk.decode("utf-8"))
                        sys.stdout.flush()  # Ensure the output is printed immediately
                        # time.sleep(0.0000000005)    # 50ms delay to simulate typing
                print(f"\n\nTotal time taken: {time.time() - start:.2f} seconds")
                print("\n\nStreaming complete.")
            else:
                print(f"Error: {r.status_code} - {r.text}")
                
        start_time = time.time()
        # without using with statement
        response = requests.post(url, json=payload, timeout=10)
        print("Streaming the CV summary:\n")
        print(response.text)
        print(f"Initial response time: {time.time() - start_time:.2f} seconds")

    except requests.exceptions.Timeout:
        print("Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_stream_summary_with_typing_effect()
