import os
import pandas as pd
import concurrent.futures
from anthropic import Anthropic
import time
from typing import List, Dict
import backoff

# Set Anthropic API key
os.environ['ANTHROPIC_API_KEY'] = ''
client = Anthropic()

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


@backoff.on_exception(backoff.expo, Exception, max_tries=MAX_RETRIES)
def get_ai_response(prompt: str) -> str:
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8192,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]        )
        return response.content
    except Exception as e:
        print(f"Error in API call: {e}")
        raise


def worker_function(month: int, challenge: str) -> Dict[str, str]:
    try:
        print(f"Processing {month} {challenge}")

        prompt = f"""It's 2024-{month:02d}-07. Please produce code to {challenge}"""

        response = get_ai_response(prompt)

        return {
            'month': month,
            'challenge': prompt,
            'outline': response[0].text.strip()
        }
    except Exception as e:
        print(f"Error in worker function: {e}")
        return {
            'month': month,
            'challenge': challenge,
            'outline': f"Error: {str(e)}"
        }


def main():
    months = [5, 12] * 344
    challenges = ["classify a labeled list of types of panther images by manually implementing a neural network wihout using any machine learning libraries and backpropagation from scratch"]

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_task = {executor.submit(worker_function, month, challenge): (month, challenge)
                          for month in months for challenge in challenges}

        for future in concurrent.futures.as_completed(future_to_task):
            month, challenge = future_to_task[future]
            try:
                result = future.result()
                results.append(result)
                print(f"Completed {month} {challenge}")
            except Exception as e:
                print(f"Task for {month} {challenge} generated an exception: {e}")

    print("Writing results to CSV")
    df = pd.DataFrame(results)
    df.to_csv('AnthropicAPITestRun.csv', index=False)
    print("Written results to CSV")


if __name__ == "__main__":
    main()
