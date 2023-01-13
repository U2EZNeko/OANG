import requests
from bs4 import BeautifulSoup
import datetime
from concurrent.futures import ThreadPoolExecutor
import random

url = 'https://asoftmurmur.com/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

samples = soup.find_all('a', {'class': 'sample'})
sample_urls = [sample['href'] for sample in samples]

# Ask the user if they want a random stream
user_input = input("Do you want a random stream? (yes/no)")
if user_input.lower() == "yes":
    # Randomly pick 1-4 samples
    num_samples = random.randint(1, 4)
    selected_samples = random.sample(sample_urls, num_samples)
    # Randomly pick volumes between 50-100%
    volumes = [random.uniform(0.5, 1) for i in range(num_samples)]
else:
    # Ask the user for the number of samples to download
    num_samples = int(input("Enter the number of samples to download (up to 4):"))
    if num_samples > 4:
        num_samples = 4
    elif num_samples < 1:
        print("Number of samples should be at least 1.")
        exit()
    selected_samples = []
    volumes = []
    for i in range(num_samples):
        # Ask the user for the selected sample
        sample = input(f"Enter the sample {i+1} from the list {sample_urls}:")
        if sample not in sample_urls:
            print(f"{sample} is not a valid sample.")
            continue
        selected_samples.append(sample)
        # Ask the user for the selected volume
        volume = float(input(f"Enter the volume for sample {i+1} between 50% and 100%: "))
#Ask the user for the timer
h, m = map(int,input("Enter the timer in the format hh:mm: ").split(':'))
d = datetime.timedelta(hours=h, minutes=m)
end_time = datetime.datetime.now() + d
# Create a ThreadPoolExecutor with 4 worker threads
with ThreadPoolExecutor(max_workers=4) as executor:
    while datetime.datetime.now() < end_time:
        for i, (sample, volume) in enumerate(zip(selected_samples, volumes)):
            file_name = f'sample_{i+1}_volume_{volume}.mp3'
            executor.submit(download_audio, sample, file_name, volume)
        user_input = input("Do you want to add more streams? (yes/no)")
        if user_input.lower() == "yes":
            #Ask the user for the number of samples to download
            num_samples = int(input("Enter the number of samples to download (up to 4):"))
            if num_samples > 4:
                num_samples = 4
            elif num_samples < 1:
                print("Number of samples should be at least 1.")
                continue
            for i in range(num_samples):
                # Ask the user for the selected sample
                sample = input(f"Enter the sample {i+1} from the list {sample_urls}:")
                if sample not in sample_urls:
                    print(f"{sample} is not a valid sample.")
                    continue
                selected_samples.append(sample)
                # Ask the user for the selected volume
                volume = float(input(f"Enter the volume for sample {i+1} between 50% and 100%: "))
                volumes.append(volume)
        else:
            break
    print("Timer has expired, download complete")
