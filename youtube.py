import time
import random
import requests
from googlesearch import search
from bs4 import BeautifulSoup

def search_with_proxy(query, proxies):
    # Choose a random proxy
    proxy = random.choice(proxies)
    
    try:
        # Make the search request using requests library with the chosen proxy
        response = requests.get(f"https://www.google.com/search?q={query}", proxies=proxy)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the search request: {e}")
        return None

def search_youtube_videos(titles_file, output_file, proxies):
    print("Reading titles from the input file...")
    # Read titles from the input file
    with open(titles_file, 'r') as file:
        titles = file.readlines()

    # Open output file to write links
    print("Searching for YouTube videos...")
    with open(output_file, 'w') as outfile:
        for idx, title in enumerate(titles):
            query = f'"{title.strip()}" youtube'  # Enclose the title in double quotes for exact match
            print(f"Searching for video '{query}' ({idx + 1}/{len(titles)})...")
            
            # Print the query being searched
            print(f"Searching for: {query}")
            
            # Perform the search request using a proxy
            search_html = search_with_proxy(query, proxies)
            if search_html:
                # Parse the HTML response
                soup = BeautifulSoup(search_html, 'html.parser')
                
                # Extract video link from search results
                video_found = False
                result_count = 0
                for link in soup.find_all('a'):
                    url = link.get('href')
                    if url and url.startswith("/url?q=https://www.youtube.com/watch"):
                        result_count += 1
                        if result_count <= 5:  # Limiting to 5 results
                            print(f"Result {result_count}:")
                            print(f"Title: {title.strip()}")
                            print(f"Link: {url}\n")
                            outfile.write(f"{title.strip()}\n{url}\n\n")
                        video_found = True
                        if result_count == 5:  # Break if 5 results are found
                            break

                if not video_found:
                    print("No video found in the search results.")
                    edit = input("Do you want to edit the title? (yes/no): ")
                    if edit.lower() == "yes":
                        new_title = input("Enter the modified title: ")
                        titles[idx] = new_title + "\n"
                        continue
            else:
                print("Failed to retrieve search results. Skipping to the next title.")
            
            # Add exponential backoff to handle rate limiting
            retries = 0
            while True:
                retries += 1
                if retries > 100:
                    print("Exceeded maximum number of retries. Moving to the next title.")
                    break
                
                # Calculate the delay using exponential backoff
                delay = 2 ** retries
                print(f"Waiting for {delay} seconds before retrying...")
                time.sleep(delay)
                
                # Perform the search request again
                search_html = search_with_proxy(query, proxies)
                if search_html:
                    # If successful, break out of the retry loop
                    break

# Provide input and output file names
titles_file = 'titles.txt'
output_file = 'video_links.txt'
              
# Provide input and output file names
titles_file = 'titles.txt'
output_file = 'video_links.txt'

# List of proxies (replace with your list)
proxies = [
    {'http': '8.222.222.64:80'},
    {'http': '35.185.196.38:3128'},
    # Add more proxies as needed
]

# Call the function with proxies
search_youtube_videos(titles_file, output_file, proxies)
