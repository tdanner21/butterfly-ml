DRY_RUN = False

import os
import shutil

DATA_DIR = "data/raw"
MIN_IMAGES = 50

WAKE_COUNTY_SPECIES = [
    "Eastern_Tiger_Swallowtail", "Monarch", "Fiery_Skipper",
    "Silver-spotted_Skipper", "Common_Buckeye", "Red-spotted_Admiral",
    "Black_Swallowtail", "Pearl_Crescent", "Variegated_Fritillary",
    "Pipevine_Swallowtail", "American_Lady", "Zabulon_Skipper",
    "Sleepy_Orange", "Cloudless_Sulphur", "Small_White",
    "Eastern_Tailed-Blue", "Clouded_Skipper", "Spicebush_Swallowtail",
    "Red_Admiral", "Gray_Hairstreak", "Horace's_Duskywing",
    "Common_Checkered-Skipper", "Red-banded_Hairstreak", "Gulf_Fritillary",
    "Question_Mark", "Ocola_Skipper", "Carolina_Satyr", "Summer_Azure",
    "Viceroy", "Hackberry_Emperor", "Huron_Skipper", "Least_Skipper",
    "Painted_Lady", "Long-tailed_Skipper", "American_Snout",
    "Southern_Pearly-eye", "Little_Glassywing", "Eastern_Comma",
    "Juvenal's_Duskywing", "Eastern_Gemmed-Satyr", "Great_Purple_Hairstreak",
    "Mourning_Cloak", "Orange_Sulphur", "Northern_Pearly-eye",
    "Eufala_Skipper", "Brazilian_Skipper", "Tawny_Emperor",
    "Appalachian_Brown", "Dion_Skipper", "Little_Yellow", "Creole_Pearly-eye",
    "Zebra_Swallowtail", "White_M_Hairstreak", "Dun_Skipper",
    "Falcate_Orangetip", "Southern_Skipperling", "Hoary_Edge",
    "Little_Wood_Satyr", "Lace-winged_Roadside-Skipper", "Common_Wood-Nymph",
    "Common_Sootywing", "Harvester", "Great_Spangled_Fritillary",
    "Byssus_Skipper", "Juniper_Hairstreak", "Henry's_Elfin",
    "Checkered_White", "Broad-winged_Skipper", "Wild_Indigo_Duskywing",
    "Silvery_Checkerspot", "Swarthy_Skipper", "Zarucco_Duskywing",
    "Southern_Broken-Dash", "Crossline_Skipper", "Banded_Hairstreak",
    "Palamedes_Swallowtail", "Clouded_Sulphur", "Eastern_Pine_Elfin",
    "Northern_Cloudywing", "Spring_Azure", "Eastern_Giant_Swallowtail",
    "Striped_Hairstreak", "Northern_Crescent", "Pepper_and_Salt_Skipper",
    "Yehl_Skipper", "Oak_Hairstreak"
]

# Step 1: Merge Pieris rapae folders into Small_White
# All known Pieris rapae folder names across languages

small_white_dir = os.path.join(DATA_DIR, "Small_White")
os.makedirs(small_white_dir, exist_ok=True)

SMALL_WHITE_VARIANTS = [
    "Pieris_rapae", "Pieris_rapae_crucivora", "Pieris_rapae_rapae",
    "Cabbage_White", "Kleiner_Kohlweißling", "Piéride_de_la_rave",
    "Blanquilla_de_la_col", "モンシロチョウ", "菜粉蝶", "Bielinek_rzepnik",
    "Borboleta-pequena-da-couve", "Білан_ріп'яний", "Белянка_репная",
    "Blanqueta_de_la_col", "배추흰나비", "Répalepke", "Klein_koolwitje",
    "Cavolaia_minore", "bělásek_řepový", "mlynárik_repový",
    "Cabbage_Butterfly", "Small_Cabbage_White", "Ropinis_baltukas",
    "Fluturele_verzei", "Рапична_пеперуда", "Repičin_bijelac",
    "Mariposa_blanca_de_la_col", "לבנין_הצנון", "Πιερίδα_των_γογγυλίων"
]

for folder in SMALL_WHITE_VARIANTS:
    src = os.path.join(DATA_DIR, folder)
    if os.path.exists(src):
        for img in os.listdir(src):
            src_path = os.path.join(src, img)
            dst_path = os.path.join(small_white_dir, img)
            if not os.path.exists(dst_path) and os.path.exists(src_path):
                if not DRY_RUN:
                    shutil.move(src_path, dst_path)
        if not DRY_RUN and os.path.exists(src):
            shutil.rmtree(src)
        print(f"{'Would merge' if DRY_RUN else 'Merged'} {folder} into Small_White")

# Merge Eastern_Black_Swallowtail into Black_Swallowtail
black_swallowtail_dir = os.path.join(DATA_DIR, "Black_Swallowtail")
os.makedirs(black_swallowtail_dir, exist_ok=True)
for folder in ["Eastern_Black_Swallowtail"]:
    src = os.path.join(DATA_DIR, folder)
    if os.path.exists(src):
        for img in os.listdir(src):
            src_path = os.path.join(src, img)
            dst_path = os.path.join(black_swallowtail_dir, img)
            if not os.path.exists(dst_path) and os.path.exists(src_path):
                if not DRY_RUN:
                    shutil.move(src_path, dst_path)
        if not DRY_RUN and os.path.exists(src):
            shutil.rmtree(src)
        print(f"{'Would merge' if DRY_RUN else 'Merged'} {folder} into Black_Swallowtail")

# Merge Red-spotted_Purple into Red-spotted_Admiral
red_spotted_dir = os.path.join(DATA_DIR, "Red-spotted_Admiral")
os.makedirs(red_spotted_dir, exist_ok=True)
for folder in ["Red-spotted_Purple"]:
    src = os.path.join(DATA_DIR, folder)
    if os.path.exists(src):
        for img in os.listdir(src):
            src_path = os.path.join(src, img)
            dst_path = os.path.join(red_spotted_dir, img)
            if not os.path.exists(dst_path) and os.path.exists(src_path):
                if not DRY_RUN:
                    shutil.move(src_path, dst_path)
        if not DRY_RUN and os.path.exists(src):
            shutil.rmtree(src)
        print(f"{'Would merge' if DRY_RUN else 'Merged'} {folder} into Red-spotted_Admiral")

# Merge Migratory_Monarch and Danaus_plexippus into Monarch
monarch_dir = os.path.join(DATA_DIR, "Monarch")
os.makedirs(monarch_dir, exist_ok=True)
for folder in ["Migratory_Monarch", "Danaus_plexippus", "Monark", "Monarque"]:
    src = os.path.join(DATA_DIR, folder)
    if os.path.exists(src):
        for img in os.listdir(src):
            src_path = os.path.join(src, img)
            dst_path = os.path.join(monarch_dir, img)
            if not os.path.exists(dst_path) and os.path.exists(src_path):
                if not DRY_RUN:
                    shutil.move(src_path, dst_path)
        if not DRY_RUN and os.path.exists(src):
            shutil.rmtree(src)
        print(f"{'Would merge' if DRY_RUN else 'Merged'} {folder} into Monarch")

# Merge Eastern_Black_Swallowtail into Black_Swallowtail
BLACK_SWALLOWTAIL_VARIANTS = ["Eastern_Black_Swallowtail"]

# Merge Red-spotted_Purple into Red-spotted_Admiral
RED_SPOTTED_VARIANTS = ["Red-spotted_Purple"]

# Merge Migratory_Monarch into Monarch
MONARCH_VARIANTS = ["Migratory_Monarch", "Danaus_plexippus", "Monark", "Monarque"]

# Step 2: Remove folders not in Wake County list or below threshold
print("\n=== STEP 2: Removing out-of-scope and low-image folders ===\n")
for folder in os.listdir(DATA_DIR):
    path = os.path.join(DATA_DIR, folder)
    if not os.path.isdir(path):
        continue
    image_count = len(os.listdir(path))
    if folder not in WAKE_COUNTY_SPECIES:
        if not DRY_RUN:
            shutil.rmtree(path)
        print(f"{'Would remove' if DRY_RUN else 'Removed'} (not in Wake County): {folder} ({image_count} images)")
    elif image_count < MIN_IMAGES:
        if not DRY_RUN:
            shutil.rmtree(path)
        print(f"{'Would remove' if DRY_RUN else 'Removed'} (below threshold): {folder} ({image_count} images)")

# Step 3: Final count
print("\n=== FINAL DATASET ===\n")
remaining = []
for folder in os.listdir(DATA_DIR):
    path = os.path.join(DATA_DIR, folder)
    if os.path.isdir(path):
        count = len(os.listdir(path))
        remaining.append((folder, count))

remaining.sort(key=lambda x: x[1], reverse=True)
for folder, count in remaining:
    print(f"{folder}: {count} images")
print(f"\nTotal species: {len(remaining)}")
print(f"Total images: {sum(c for _, c in remaining)}")