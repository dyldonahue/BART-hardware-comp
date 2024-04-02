from transformers import BartForConditionalGeneration, BartTokenizer
import torch
import psutil
import time
#from pyjoules.energy_meter import EnergyMeter

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

if device.type == 'cuda':
    import pynvml
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Assuming GPU index 0

start_time = time.time()

# Initialize the energy meter
#meter = EnergyMeter()

# Start measuring energy consumption
#meter.start()

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
responses = []
for input_text in inputs:
    if device.type == 'cuda':
        power_usage = pynvml.nvmlDeviceGetPowerUsage(handle)  # in milliwatts
    memory_usage = torch.cuda.memory_allocated(device)
    cpu_usage = psutil.cpu_percent(interval=.2) # may need to adjust if this loops faster than this


    input_tokens = tokenizer(input_text, return_tensors='pt')
    output = model.generate(**input_tokens)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    responses.append(response)

    if device.type == 'cuda':
        print(f"Power usage: {power_usage / 1000:.2f} Watts")
    print(f"Memory usage: {memory_usage / 1024 ** 2:.2f} MB")

#meter.stop()

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")

#energy_consumption = meter.total_energy()
#print(f"Energy consumption: {energy_consumption:.2f} Joules")

