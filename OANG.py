import os
from pydub import AudioSegment
import datetime
from tqdm import tqdm
import math

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
    try:
        selection_index = int(selection) - 1
        if 0 <= selection_index < len(sample_files):
            selected_samples.append(sample_files[selection_index])
        else:
            print("Invalid selection, please select a valid number.")
    except ValueError:
        print("Please enter a valid number.")

# Load the selected sample files using pydub's AudioSegment class
samples = [AudioSegment.from_file(f) for f in selected_samples]

# Prompt the user for the max volume of each sample
volumes = []
for i in range(len(selected_samples)):
    volume = float(input(f"Enter the max volume for {selected_samples[i]} (0-1): "))
    # Convert volume from linear scale to decibels
    volume_db = 20 * math.log10(volume)
    volumes.append(volume_db)

# Adjust the volume of each sample to the specified max volume
for i in range(len(samples)):
    samples[i] += samples[i].apply_gain(volumes[i])

# Prompt the user for the duration of the output loop file
output_duration = int(input("Enter the desired duration of the output loop (in seconds): ")) * 1000

# Ensure the final output matches the desired duration
final_output = AudioSegment.silent(duration=output_duration)
current_length = 0
for sample in samples:
    while current_length < output_duration:
        final_output = final_output.overlay(sample, position=current_length)
        current_length += len(sample)

# Get the current date and time
now = datetime.datetime.now()

# Format the date and time to be included in the file name
date_time = now.strftime("%Y-%m-%d %H-%M-%S")

# Export the output to a new audio file with the current date and time in the file name
final_output.export(f"output {date_time}.mp3", format="mp3")
