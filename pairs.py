import shutil
import os

# new  pairs folder
src_folder = 'pairs'
dst_folder = 'pairs_copy'

if os.path.exists(dst_folder):
    shutil.rmtree(dst_folder)  # remove it if it already exists
shutil.copytree(src_folder, dst_folder)

# read into a list
with open('bad_texts.txt', 'r') as file:
    bad_texts = file.readlines()

for i, bad_text in enumerate(bad_texts):
    pair_folder = f'{dst_folder}/pair_{i}'
    
    #  just to be safe
    if os.path.exists(pair_folder):
        with open(f'{pair_folder}/b_description.txt', 'w') as bad_text_file:
            bad_text_file.write(bad_text)
        print(f'Bad text {i} written: {pair_folder}/b_description.txt')
