import os
from pydub import AudioSegment
import datetime
from tqdm import tqdm

# Set the path to the folder containing the sample files
sample_folder = "Sound Samples"

# Initialize an empty list to store the sample files
sample_files = []

# Use os.walk to recursively scan the sample_folder and its subdirectories
for root, dirs, files in os.walk(sample_folder):
    for file in files:
        if file.endswith(".mp3"):
            # Add the full path of the file to the list
            sample_files.append(os.path.join(root, file))

# Prompt the user to select up to 4 samples
selected_samples = []
while len(selected_samples) < 4:
    print("Select a sample file (press enter to finish):")
    for i, sample in enumerate(sample_files):
        print(f"{i+1}. {sample}")
    selection = input()
    if selection == "":
        break
    else:
        selected_samples.append(sample_files[int(selection) - 1])

# Load the selected sample files using pydub's AudioSegment class
samples = [AudioSegment.from_file(f) for f in selected_samples]

# Prompt the user for the max volume of each sample
volumes = []
for i in range(len(selected_samples)):
    volumes.append(float(input(f"Enter the max volume for {selected_samples[i]} (0-1): ")))

# Adjust the volume of each sample to the specified max volume
for i in range(len(samples)):
    samples[i] = samples[i].apply_gain(volumes[i])

# Prompt the user for the duration of the output loop file
output_duration = int(input("Enter the desired duration of the output loop (in seconds): ")) * 1000

# repeat the shorter samples to match the length of the longest sample
max_length = max([len(sample) for sample in samples])
for i in range(len(samples)):
    while len(samples[i]) < max_length:
        samples[i] += samples[i]

# alternate the volumes of the samples
for i in range(len(samples)):
    if i == 0:
        samples[i] = samples[i].fade_in(1000)
    else:
        samples[i] = samples[i].fade_out(1000).fade_in(1000)

# Crossfade the samples and create the output file
output = samples[0]
for i in range(1, len(samples)):
    output = output.append(samples[i], crossfade=1000)

# Get the current date and time
now = datetime.datetime.now()

# Format the date and time to be included in the file name
date_time = now.strftime("%Y-%m-%d %H-%M-%S")

# Export the output to a new audio file with the current date and time in the file
output.export(f"output {date_time}.mp3", format="mp3")
