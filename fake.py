from faker import Faker
import random

# Initialize Faker for fake text generation
fake = Faker()

# Function to generate fake text with random lengths up to 1000 characters
def generate_fake_text(max_length=1000):
    fake_text = ''
    target_length = random.randint(1, max_length)
    while len(fake_text) < target_length:
        fake_text += fake.sentence() + ' '
    return fake_text[:target_length]  # Truncate to target_length if needed

# Generate 100 inputs and write them to a file
with open('fake10.txt', 'w') as f:
    for i in range(100):
        fake_text = generate_fake_text()
        # Format each input with a unique identifier
        input_string = f"Input {i+1}: {fake_text}\n"
        f.write(input_string)

print("Fake inputs generated and written to 'fake_inputs.txt'.")
