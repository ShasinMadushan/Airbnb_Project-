import os
import requests
from tqdm import tqdm


URLS = {
    "listings": "https://data.insideairbnb.com/united-kingdom/england/london/2024-09-06/data/listings.csv.gz",
    "calendar": "https://data.insideairbnb.com/united-kingdom/england/london/2024-09-06/data/calendar.csv.gz",
    "reviews": "https://data.insideairbnb.com/united-kingdom/england/london/2024-09-06/data/reviews.csv.gz"
}

def get_file(url, path):
    if os.path.exists(path):
        print(f"File exists: {path}")
        return

    print(f"Downloading: {url}")
    res = requests.get(url, stream=True)
    res.raise_for_status()
    
    total = int(res.headers.get('content-length', 0))
    with open(path, 'wb') as f, tqdm(total=total, unit='B', unit_scale=True) as bar:
        for chunk in res.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))

def main():
    os.makedirs("data/raw", exist_ok=True)
    for name, url in URLS.items():
        path = f"data/raw/london_{name}.csv.gz"
        get_file(url, path)

if __name__ == "__main__":
    main()