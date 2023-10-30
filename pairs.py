import shutil
import os

# Duplicate the pairs folder
src_folder = 'pairs'
dst_folder = 'pairs_copy'

if os.path.exists(dst_folder):
    shutil.rmtree(dst_folder)  # remove it if it already exists
shutil.copytree(src_folder, dst_folder)

# Read the lines from bad_texts.txt into a list
with open('bad_texts.txt', 'r') as file:
    bad_texts = file.readlines()

# Iterate over each folder in the pairs_copy folder and add a Bad_text{i}.txt file
for i, bad_text in enumerate(bad_texts):
    pair_folder = f'{dst_folder}/pair_{i}'
    
    # Check if the folder exists, just to be safe
    if os.path.exists(pair_folder):
        with open(f'{pair_folder}/b_description.txt', 'w') as bad_text_file:
            bad_text_file.write(bad_text)
        print(f'Bad text {i} written: {pair_folder}/b_description.txt')
