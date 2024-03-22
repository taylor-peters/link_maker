from googlesearch import search
from bs4 import BeautifulSoup

def search_youtube_videos(titles_file, output_file):
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
            
            # Use generator to limit search results to 1
            search_results = search(query, num_results=5)
            
            # Extract video link from search results
            video_found = False
            for url in search_results:
                if url.startswith("https://www.youtube.com/watch"):
                    print(f"Found video: {title.strip()}")
                    print(f"Link: {url}\n")
                    outfile.write(f"{title.strip()}\n{url}\n\n")
                    video_found = True
                    break
            
            # If no video is found, print a message
            if not video_found:
                print(f"No video found for '{title.strip()}'\n")

    print("Search completed. Check the output file for links.")

# Provide input and output file names
titles_file = 'titles.txt'
output_file = 'video_links.txt'

# Call the function
search_youtube_videos(titles_file, output_file)
