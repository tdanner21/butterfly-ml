import requests
import os
import time

OUTPUT_DIR = "data/raw/"
TAXON_ID = 55626
PER_PAGE = 200
MAX_PAGES = 10

def fetch_observations(page):
    url = "https://api.inaturalist.org/v1/observations"
    params = {
        "taxon_id": TAXON_ID,
        "quality_grade": "research",
        "per_page": PER_PAGE,
        "page": page,
        "photos": True
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def download_image(url, filepath):
    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False
    
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_downloaded = 0

    for page in range(1, MAX_PAGES + 1):
        print(f"Fetching page {page}...")

        data = fetch_observations(page)
        results = data["results"]
        total_results = data["total_results"]

        if not results:
            print ("No more results.")
            break
        for obs in results:
            if not obs.get("photos"):
                continue

            species = (obs.get("species_guess") or "unknown").replace(" ", "_")
            photo_url = obs["photos"][0]["url"].replace("square", "medium")

            species_dir = os.path.join(OUTPUT_DIR, species)
            os.makedirs(species_dir, exist_ok=True)

            filename = f"{obs['id']}.jpg"
            filepath = os.path.join(species_dir, filename)

            if os.path.exists(filepath):
                continue

            if download_image(photo_url, filepath):
                total_downloaded += 1

        print (f"Page {page} done. Total downloaded: {total_downloaded} of {total_results}")
        time.sleep(1)

if __name__ == "__main__":
    main()