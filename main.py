from transformers import BartForConditionalGeneration, BartTokenizer
import torch
import psutil
import time
from pyJoules.energy_meter import measure_energy

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

if device.type == 'cuda':
    import pynvml
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Assuming GPU index 0



# Initialize BART model and tokenizer
model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Read inputs from the file
inputs = []
with open('fake1.txt', 'r') as f:
    for line in f:
        # Extract the input text from the formatted line
        input_text = line.strip().split(': ')[1]
        inputs.append(input_text)

# Generate responses for each input

#@measure_energy
def run_model():
    responses = []

    if device.type == 'cuda':
        model.to(device)
    for input_text in inputs:
        if device.type == 'cuda':
            power_usage = pynvml.nvmlDeviceGetPowerUsage(handle)  # in milliwatts
            memory_usage = torch.cuda.memory_allocated(device)
            memory_percent = memory_usage / torch.cuda.max_memory_allocated(device) * 100
        cpu_usage = psutil.cpu_percent(interval=.2)
        total_ram = psutil.virtual_memory().total 
        ram_usage = psutil.virtual_memory().used # in bytes
        ram_percentage = psutil.virtual_memory().percent
        


        input_tokens = tokenizer(input_text, return_tensors='pt')
        if device.type == 'cuda':
            input_tokens = {k: v.to(device) for k, v in input_tokens.items()}
            
        output = model.generate(**input_tokens)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        responses.append(response)

        if device.type == 'cuda':
            print(f"GPU Power usage: {power_usage / 1000:.2f} Watts")
            print(f" GPU Memory usage: {memory_usage / 1024 ** 2:.2f} MB")
            print(f"GPU Memory Percentage: {memory_percent:.2f}%")
        print(f"CPU usage: {cpu_usage:.2f}%")
        print(f"RAM usage: {ram_usage / 1024 ** 3:.2f} GB")
        print (f"RAM Percentage: {psutil.virtual_memory().percent:.2f}%")
        print(f"Total RAM: {total_ram / 1024 ** 3:.2f} GB")

    return

start_time = time.time()
run_model()
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")


