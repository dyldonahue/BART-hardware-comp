from transformers import BartForConditionalGeneration, BartTokenizer


# Custom text inputs for qualitative results
custom_inputs = [
    "Tell me a story",
    "Describe the impact of climate change on society.",
    "Discuss the role of artificial intelligence in healthcare and its ethical implications.",
    "What is the capital of France?",
    "List the steps to create a Python virtual environment using venv.",
    "Summarize the plot of the movie Interstelllar."
]

# Initialize BART model and tokenizer
model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Generate responses for each custom input
responses = []
for input_text in custom_inputs:
    # Extract the input text from the formatted line
    input_text = input_text.split(': ')[1]
    input_tokens = tokenizer(input_text, return_tensors='pt')
    output = model.generate(**input_tokens)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    responses.append(response)

# Write the responses to a new file
with open('bart_responses.txt', 'w') as f:
    for i, response in enumerate(responses):
        f.write(f"Response for {custom_inputs[i].split(': ')[0]}:\n{response}\n\n")

print("BART responses generated and written to 'bart_responses.txt'.")
