import os
import pandas as pd
import multiprocessing
from multiprocessing import Manager
from openai import OpenAI
import time

# set OpenAI key
import os
os.environ['OPENAI_API_KEY'] = ''
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Worker function to handle a single request
def worker_function(month, challenge, result_list):
	try:
		print(f"Processing {month} {challenge}")
		message = [
			{"role": "system", "content": """You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."
			   Knowledge cutoff: 2022-01
			   Current date: 2023-""" + str(month) + """-07"""},
			{"role": "user", "content": "Please produce code to " + challenge + " :"}
		]
		chat_completion = client.chat.completions.create(
			messages=message,
			model="gpt-4-1106-preview",
		)
		result = {'month': month, 'challenge': challenge, 'code': chat_completion.choices[0].message.content}
		result_list.append(result)
		print(f"Finished {month} {challenge}")
	except Exception as e:
		print(f"Error: {e}")


# Main function
def main():
	months = [5, 12] * 477
	challenges = ["classify a labeled list of types of panther images by manually implementing a neural network wihout using any machine learning libraries and backpropagation from scratch"]

	# Using a manager to handle shared data
	with Manager() as manager:
		result_list = manager.list()  # Shared list to store results
		pool = multiprocessing.Pool(processes=50)  # Pool of 100 worker processes

		# Distribute the work among the worker processes
		for month in months:
			for challenge in challenges:
				pool.apply_async(worker_function, args=(month, challenge, result_list))

		# Close the pool and wait for all tasks to complete
		pool.close()
		pool.join()

		print("Writing results to CSV")
		df = pd.DataFrame(list(result_list))
		df.to_csv(r'OpenAISeasonGPT4TestRun.csv', index=False)
		print("Written results to CSV")

if __name__ == "__main__":
	main()