import json
import os

# Construct the file path to the parent directory
file_path = os.path.join(os.path.dirname(__file__), '..', 'site_titles_urls.json')

# Load the JSON data from the file
with open(file_path, 'r') as file:
    data = json.load(file)

# Iterate over each item and filter sublinks
def filter_sublinks(sublinks):
    invalid_starts = ('#', 'mailto:', 'http://', 'https://', 'www.', 'javascript:', 'tel:', '{')
    return [
        sublink.lstrip('/')
        for sublink in sublinks
        if not sublink.startswith(invalid_starts) and
			'unm.edu' not in sublink and
			sublink.strip() and
			len(sublink) > 1
	]

for item in data:
    item['sublinks'] = filter_sublinks(item['sublinks'])

# Save the modified JSON data back to the file
with open(file_path, 'w') as file:
    json.dump(data, file, indent=4)