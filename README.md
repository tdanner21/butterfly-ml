# Butterfly ML Project

I am undergoing a project where I want to build an ML model and combine it with physical hardware to identify different butterfly species in Raleigh, NC. 

## Project Goal
The purpose of this project is to learn important ML skills while creating something cool. I chose this specific project because I wanted to do something in nature, while also combining software + hardware. 

## Dataset
- 41 species observable in Wake County, NC
- 9,023 images sourced from iNaturalist
- Filtered to Research Grade observations with 50+ images per species

## Project Structure
- `src/` - Data pipeline and training scripts
- `data/raw/` - Downloaded images organized by species
- `models/` - Trained model checkpoints
- `logs/` - Training logs and experiment results

## Scripts
- `download_data.py` - Downloads butterfly images from iNaturalist API
- `download_small_white.py` - Targeted download for Small White species
- `explore_dataset.py` - Analyzes dataset composition
- `cleanup_dataset.py` - Filters and merges dataset folders

## Status
Phase 1 complete: dataset collected and cleaned.
Phase 2 in progress: baseline model training.