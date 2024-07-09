#!/usr/bin/env python
# coding: utf-8

# Import required libraries
from PIL import Image
import pandas as pd
import numpy as np
import time
import os
import random
from progressbar import progressbar

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Import configuration file
from config import CONFIG


# Parse the configuration file and make sure it's valid
def parse_config():
    assets_path = 'assets'
    
    for layer in CONFIG:
        layer_path = os.path.join(assets_path, layer['directory'])
        traits = sorted([trait for trait in os.listdir(layer_path) if trait[0] != '.'])
        
        if not layer['required']:
            traits = [None] + traits
        
        # Calculate rarity weights if they're not already provided
        if layer['rarity_weights'] is None:
            rarities = [1 for _ in traits]
        else:
            rarities = layer['rarity_weights']
        
        # Adjust rarities to sum up to 1
        rarities = get_weighted_rarities(rarities)
        
        layer['rarity_weights'] = rarities
        layer['cum_rarity_weights'] = np.cumsum(rarities)
        layer['traits'] = traits

# Weight rarities and return a numpy array that sums up to 1
def get_weighted_rarities(arr):
    total_weight = sum(arr)
    return np.array(arr) / total_weight if total_weight > 0 else arr

# Generate a single image given an array of filepaths representing layers
def generate_single_image(filepaths, output_filename=None):
    
    # Treat the first layer as the background
    bg = Image.open(os.path.join('assets', filepaths[0]))
    
    
    # Loop through layers 1 to n and stack them on top of another
    for filepath in filepaths[1:]:
        if filepath.endswith('.png'):
            img = Image.open(os.path.join('assets', filepath))
            print(f"XXX: {filepath}")
            bg.paste(img, (0,0), img)
    
    # Save the final image into desired location
    if output_filename is not None:
        bg.save(output_filename)
    else:
        # If output filename is not specified, use timestamp to name the image and save it in output/single_images
        if not os.path.exists(os.path.join('output', 'single_images')):
            os.makedirs(os.path.join('output', 'single_images'))
        bg.save(os.path.join('output', 'single_images', str(int(time.time())) + '.png'))


# Generate a single image with all possible traits
# generate_single_image(['Background/green.png', 
#                        'Body/brown.png', 
#                        'Expressions/standard.png',
#                        'Head Gear/std_crown.png',
#                        'Shirt/blue_dot.png',
#                        'Misc/pokeball.png',
#                        'Hands/standard.png',
#                        'Wristband/yellow.png'])


# Get total number of distinct possible combinations
def get_total_combinations():
    
    total = 1
    for layer in CONFIG:
        total = total * len(layer['traits'])
    return total


# Select an index based on rarity weights
def select_index(cum_rarities, rand):
    
    cum_rarities = [0] + list(cum_rarities)
    for i in range(len(cum_rarities) - 1):
        if rand >= cum_rarities[i] and rand <= cum_rarities[i+1]:
            return i
    
    # Should not reach here if everything works okay
    return None


# Generate a set of traits given rarities
def generate_trait_set_from_config():
    trait_set = []
    trait_paths = []
    
    for layer in CONFIG:
        traits, rarities, cum_rarities = layer['traits'], layer['rarity_weights'], layer['cum_rarity_weights']
        
        # Generate a random number between 0 and 1
        rand_num = random.random()
        # If it's layer 3, we only add it 50% of the time
        if layer['id'] == 3 and rand_num > 0.5:
            continue
        # Select an element index based on the random number and cumulative rarity weights
        idx = select_index(cum_rarities, rand_num)
        
        # Add selected trait to trait set
        trait_set.append(traits[idx])
        
        # Add trait path to trait paths if the trait has been selected
        if traits[idx] is not None:
            if layer['id'] == 6:
                trait_path = os.path.join(layer['directory'], trait_set[1])
            else: trait_path = os.path.join(layer['directory'], traits[idx])
            trait_paths.append(trait_path)
            # print(f"Added trait path for layer {layer['name']}: {trait_paths}")
    return trait_set, trait_paths


# Generate the image set. Don't change drop_dup
def generate_images(edition, count, drop_dup=True):
    
    # Initialize an empty rarity table
    rarity_table = {}
    for layer in CONFIG:
        rarity_table[layer['name']] = []

    # Define output path to output/edition {edition_num}
    op_path = os.path.join('output', 'edition ' + str(edition), 'images')

    # Will require this to name final images as 000, 001,...
    zfill_count = len(str(count - 1))
    
    # Create output directory if it doesn't exist
    if not os.path.exists(op_path):
        os.makedirs(op_path)
      
    # Create the images
    for n in progressbar(range(count)):
        
        # Set image name
        image_name = str(n).zfill(zfill_count) + '.png'
        
        # Get a random set of valid traits based on rarity weights
        trait_sets, trait_paths = generate_trait_set_from_config()

        # Generate the actual image
        generate_single_image(trait_paths, os.path.join(op_path, image_name))
        
        # Populate the rarity table with metadata of newly created image
        for idx, trait in enumerate(trait_sets):
            if trait is not None:
                rarity_table[CONFIG[idx]['name']].append(trait[: -1 * len('.png')])
            else:
                rarity_table[CONFIG[idx]['name']].append('none')
    
    # Create the final rarity table by removing duplicate creat
    rarity_table = pd.DataFrame(rarity_table).drop_duplicates()
    print("Generated %i images, %i are distinct" % (count, rarity_table.shape[0]))
    
    if drop_dup:
        # Get list of duplicate images
        img_tb_removed = sorted(list(set(range(count)) - set(rarity_table.index)))

        # Remove duplicate images
        print("Removing %i images..." % (len(img_tb_removed)))

        #op_path = os.path.join('output', 'edition ' + str(edition))
        for i in img_tb_removed:
            os.remove(os.path.join(op_path, str(i).zfill(zfill_count) + '.png'))

        # Rename images such that it is sequentialluy numbered
        for idx, img in enumerate(sorted(os.listdir(op_path))):
            os.rename(os.path.join(op_path, img), os.path.join(op_path, str(idx).zfill(zfill_count) + '.png'))
    
    
    # Modify rarity table to reflect removals
    rarity_table = rarity_table.reset_index()
    rarity_table = rarity_table.drop('index', axis=1)
    return rarity_table

# Main function. Point of entry
def main():

    print("Checking assets...")
    parse_config()
    print("Assets look great! We are good to go!")
    print()

    tot_comb = get_total_combinations()
    print("You can create a total of %i distinct avatars" % (tot_comb))
    print()

    print("How many avatars would you like to create? Enter a number greater than 0: ")
    while True:
        num_avatars = int(input())
        if num_avatars > 0:
            break
    
    print("What would you like to call this edition?: ")
    edition_name = input()

    print("Starting task...")
    rt = generate_images(edition_name, num_avatars)

    print("Saving metadata...")
    rt.to_csv(os.path.join('output', 'edition ' + str(edition_name), 'metadata.csv'))

    print("Task complete!")


# Run the main function
main()