import re
import matplotlib.pyplot as plt

# Function to read data from the raw data files and add to lists
def read_data(file_path):
    cpu_usage_pattern = r'CPU usage: (\d+\.\d+)%'
    ram_usage_pattern = r'RAM usage: (\d+\.\d+) GB'
    ram_percentage_pattern = r'RAM Percentage: (\d+\.\d+)%'
    execution_time_pattern = r'Execution time: (\d+\.\d+) seconds'

    gpu_power_pattern = r'GPU Power usage: (\d+\.\d+) W'
    gpu_memory_usage_pattern = r'GPU Memory Usage: (\d+\.\d+) GB'
    gpu_memory_percentage_pattern = r'GPU Memory Percentage: (\d+\.\d+)%'

    cpu_usage = []
    ram_usage = []
    ram_percentage = []
    execution_time = []

    gpu_power = []
    gpu_memory_usage = []
    gpu_memory_percentage = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        match = re.search(cpu_usage_pattern, line)
        if match:
            cpu_usage.append(float(match.group(1)))

        match = re.search(ram_usage_pattern, line)
        if match:
            ram_usage.append(float(match.group(1)))

        match = re.search(ram_percentage_pattern, line)
        if match:
            ram_percentage.append(float(match.group(1)))

        match = re.search(execution_time_pattern, line)
        if match:
            execution_time.append(float(match.group(1)))

        # Check if file name contains 'p100' or 't4' to include GPU data
        if 'p100' in file_path.lower() or 't4' in file_path.lower():
            match = re.search(gpu_power_pattern, line)
            if match:
                gpu_power.append(float(match.group(1)))

            match = re.search(gpu_memory_usage_pattern, line)
            if match:
                gpu_memory_usage.append(float(match.group(1)))

            match = re.search(gpu_memory_percentage_pattern, line)
            if match:
                gpu_memory_percentage.append(float(match.group(1)))

    return cpu_usage, ram_usage, ram_percentage, execution_time, gpu_power, gpu_memory_usage, gpu_memory_percentage

def calculate_average(list1, list2, list3):
    avg_list = []
    for item1, item2, item3 in zip(list1, list2, list3):
        avg_list.append((item1 + item2 + item3) / 3)
    return avg_list

# read all data
broadwell1 = read_data('broadwell1.txt')
broadwell2 = read_data('broadwell2.txt')
broadwell3 = read_data('broadwell3.txt')

cascadelake1 = read_data('cascadelake1.txt')
cascadelake2 = read_data('cascadelake2.txt')
cascadelake3 = read_data('cascadelake3.txt')

p1001 = read_data('p1001.txt')
p1002 = read_data('p1002.txt')
p1003 = read_data('p1003.txt')

t41 = read_data('t41.txt')
t42 = read_data('t42.txt')
t43 = read_data('t43.txt')


# Calculate averages for each device
broadwell_cpu = calculate_average(broadwell1[0], broadwell2[0], broadwell3[0])
broadwell_ram = calculate_average(broadwell1[2], broadwell2[2], broadwell3[2])
broadwell_time = calculate_average(broadwell1[3], broadwell2[3], broadwell3[3])

cascadelake_cpu = calculate_average(cascadelake1[0], cascadelake2[0], cascadelake3[0])
cascadelake_ram = calculate_average(cascadelake1[2], cascadelake2[2], cascadelake3[2])
cascadelake_time = calculate_average(cascadelake1[3], cascadelake2[3], cascadelake3[3])

p100_cpu = calculate_average(p1001[0], p1002[0], p1003[0])
p100_ram = calculate_average(p1001[2], p1002[2], p1003[2])
p100_time = calculate_average(p1001[3], p1002[3], p1003[3])
p100_gpu_power = calculate_average(p1001[4], p1002[4], p1003[4])
p100_gpu_percentage = calculate_average(p1001[6], p1002[6], p1003[6])

t4_cpu = calculate_average(t41[0], t42[0], t43[0])
t4_ram = calculate_average(t41[2], t42[2], t43[2])
t4_time = calculate_average(t41[3], t42[3], t43[3])
t4_gpu_power = calculate_average(t41[4], t42[4], t43[4])
t4_gpu_percentage = calculate_average(t41[6], t42[6], t43[6])

# Plot the data
plt.style.use('default')
plt.rcParams.update({'font.size': 14})
plt.rcParams.update({'font.family': 'serif'})

plt.figure(figsize=(12, 8))


plt.set_cmap('tab10')
plt.grid(True, linestyle='--', alpha=0.6)

# Plot each line with a label
plt.plot(broadwell_cpu, label='Broadwell CPU', color='#1f77b4')
plt.plot(cascadelake_cpu, label='Cascadelake CPU', color='#2ca02c')
plt.plot(p100_cpu, label='P100 CPU', color='#d62728')
plt.plot(t4_cpu, label='T4 CPU', color='#9467bd')

# Add legend with specified location
plt.legend(loc='upper right')

plt.xlabel('Device')
plt.ylabel('CPU Usage (%)')
plt.title('CPU Usage (%)')

plt.ylim(0, 100)  # Set the range from 0 to 40
plt.show()


