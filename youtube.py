import requests

def read_existing_links(output_file):
    existing_titles = set()
    existing_urls = set()

    try:
        with open(output_file, 'r') as f:
            lines = f.readlines()
            for i in range(0, len(lines), 3):
                existing_titles.add(lines[i].strip())
                existing_urls.add(lines[i+1].strip())
    except FileNotFoundError:
        pass

    return existing_titles, existing_urls

def search_youtube_videos(titles, api_key, output_file):
    base_url = 'https://www.googleapis.com/youtube/v3/search'
    max_results = 5  # Number of search results to retrieve per title
    existing_titles, existing_urls = read_existing_links(output_file)
    new_video_links = []

    for title in titles:
        if title in existing_titles:
            print(f"Skipping title '{title}' as it already exists in the output file.")
            continue

        params = {
            'part': 'snippet',
            'q': title,
            'maxResults': max_results,
            'key': api_key
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('items', []):
                if 'videoId' in item['id']:
                    video_id = item['id']['videoId']
                    video_title = item['snippet']['title']
                    video_link = f'https://www.youtube.com/watch?v={video_id}'
                    if video_link not in existing_urls:
                        new_video_links.append((video_title, video_link))
                        print(f"Found new video: {video_title} - {video_link}")
                else:
                    print(f"No video ID found for item: {item}")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    # Append new links to output file
    with open(output_file, 'a') as f:
        for video_title, video_link in new_video_links:
            f.write(f"{video_title}\n{video_link}\n\n")

# Example usage
api_key = 'AIzaSyBUV4_zc5bNcfv0C_ghoUB2siS8MMa-A2g'
output_file = 'video_links.txt'
with open('titles.txt', 'r') as file:
    titles = [line.strip() for line in file.readlines()]

search_youtube_videos(titles, api_key, output_file)
