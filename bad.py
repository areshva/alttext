import shutil
import os

def clean_description(lines):
    
    skip_prefixes = ["Chandra Release -", "Visual Description:"]
    return [line for line in lines if not any(line.startswith(prefix) for prefix in skip_prefixes) and line.strip() != '']

# Duplicate the pairs folder
src_folder = 'pairs'
dst_folder = 'full_pairs'

if os.path.exists(dst_folder):
    shutil.rmtree(dst_folder)  # remove it if it already exists
shutil.copytree(src_folder, dst_folder)

# modify description_text files
for i in range(len(os.listdir(dst_folder))):
    pair_folder = f'{dst_folder}/pair_{i}'
    desc_file_path = f'{pair_folder}/description.txt'  #our naming is consistent

    # does the description file exist?
    if os.path.exists(desc_file_path):
        with open(desc_file_path, 'r', encoding='utf-8', errors='replace') as desc_file:
            lines = desc_file.readlines()

        cleaned_lines = clean_description(lines)

        with open(desc_file_path, 'w', encoding='utf-8') as desc_file:
            desc_file.writelines(cleaned_lines)
        print(f'Modified: {desc_file_path}')

# read into a list
with open('bad_texts.txt', 'r') as file:
    bad_texts = file.readlines()

# add a bad txt file
for i, bad_text in enumerate(bad_texts):
    pair_folder = f'{dst_folder}/pair_{i}'
    
    #  just to be safe
    if os.path.exists(pair_folder):
        with open(f'{pair_folder}/b_description.txt', 'w') as bad_text_file:
            bad_text_file.write(bad_text)
        print(f'Bad text {i} written: {pair_folder}/b_description.txt')
