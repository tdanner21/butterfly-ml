import os

# Minimum image threshold
MIN_IMAGES = 50

# Wake County species (common names only)
WAKE_COUNTY_SPECIES = [
    "Eastern Tiger Swallowtail", "Monarch", "Fiery Skipper",
    "Silver-spotted Skipper", "Common Buckeye", "Red-spotted Admiral",
    "Black Swallowtail", "Pearl Crescent", "Variegated Fritillary",
    "Pipevine Swallowtail", "American Lady", "Zabulon Skipper",
    "Sleepy Orange", "Cloudless Sulphur", "Small White",
    "Eastern Tailed-Blue", "Clouded Skipper", "Spicebush Swallowtail",
    "Red Admiral", "Gray Hairstreak", "Horace's Duskywing",
    "Common Checkered-Skipper", "Red-banded Hairstreak", "Gulf Fritillary",
    "Question Mark", "Ocola Skipper", "Carolina Satyr", "Summer Azure",
    "Viceroy", "Hackberry Emperor", "Huron Skipper", "Least Skipper",
    "Painted Lady", "Long-tailed Skipper", "American Snout",
    "Southern Pearly-eye", "Little Glassywing", "Eastern Comma",
    "Juvenal's Duskywing", "Eastern Gemmed-Satyr", "Great Purple Hairstreak",
    "Mourning Cloak", "Orange Sulphur", "Northern Pearly-eye",
    "Eufala Skipper", "Brazilian Skipper", "Tawny Emperor",
    "Appalachian Brown", "Dion Skipper", "Little Yellow", "Creole Pearly-eye",
    "Zebra Swallowtail", "White M Hairstreak", "Dun Skipper",
    "Falcate Orangetip", "Southern Skipperling", "Hoary Edge",
    "Little Wood Satyr", "Lace-winged Roadside-Skipper", "Common Wood-Nymph",
    "Common Sootywing", "Harvester", "Great Spangled Fritillary",
    "Byssus Skipper", "Juniper Hairstreak", "Henry's Elfin",
    "Checkered White", "Broad-winged Skipper", "Wild Indigo Duskywing",
    "Silvery Checkerspot", "Swarthy Skipper", "Zarucco Duskywing",
    "Southern Broken-Dash", "Crossline Skipper", "Banded Hairstreak",
    "Palamedes Swallowtail", "Clouded Sulphur", "Eastern Pine Elfin",
    "Northern Cloudywing", "Spring Azure", "Eastern Giant Swallowtail",
    "Striped Hairstreak", "Northern Crescent", "Pepper and Salt Skipper",
    "Yehl Skipper", "Oak Hairstreak"
]

DATA_DIR = "data/raw"

# Normalize names for matching
def normalize(name):
    return name.lower().replace("-", " ").replace("_", " ").strip()

# Build lookup of what we have on disk
folders = os.listdir(DATA_DIR)
disk_species = {}
for folder in folders:
    path = os.path.join(DATA_DIR, folder)
    if os.path.isdir(path):
        count = len(os.listdir(path))
        disk_species[normalize(folder)] = (folder, count)

# Cross reference
print("=== SPECIES IN WAKE COUNTY WITH IMAGES ON DISK ===\n")
matched = []
for species in WAKE_COUNTY_SPECIES:
    key = normalize(species)
    if key in disk_species:
        folder, count = disk_species[key]
        matched.append((species, count))

matched.sort(key=lambda x: x[1], reverse=True)
for species, count in matched:
    flag = "" if count >= MIN_IMAGES else " << BELOW THRESHOLD"
    print(f"{species}: {count} images{flag}")

print(f"\nTotal matched: {len(matched)} species")
above = [m for m in matched if m[1] >= MIN_IMAGES]
print(f"Above {MIN_IMAGES} image threshold: {len(above)} species")

print("\n=== WAKE COUNTY SPECIES NOT IN DATASET ===\n")
for species in WAKE_COUNTY_SPECIES:
    key = normalize(species)
    if key not in disk_species:
        print(f"Missing: {species}")