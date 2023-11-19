# import pandas as pd
# from nltk.tokenize import word_tokenize
# from nltk.probability import FreqDist 
# import nltk
# import re

# nltk.download('punkt') #NLTK data required for tokenization

# # tokenize text and calculate word frequency
# def analyze_text(text):
#     tokens = word_tokenize(text)
#     tokens = [token.lower() for token in tokens if token.isalnum() and token.lower() not in excluded_terms]
#    #check if lower case word is in excluded terms and that speical charachters are excluded
#     freq_dist = FreqDist(tokens)
#     return freq_dist

# excluded_terms = {"by","this","there","an", "as", "which","the", ",", ".", "a", "of", "and", "is", "with", "to", "in", "are", "at", "from", "on", "that", "its", ":"}

# csv_file = 'alt_data.csv'
# output_file = 'common_terms.txt'
# df = pd.read_csv(csv_file)

# common_terms_freq = FreqDist()

# for alt_text in df['Alt Text']:
#     freq_dist = analyze_text(alt_text)
#     common_terms_freq.update(freq_dist)
#     #it accumulates the word frequencies across all alternative text descriptions in the df.

# sorted_terms = sorted(common_terms_freq.items(), key=lambda x: x[1], reverse=True)
# # converts the frequency distribution into a list of tuples, where each tuple contains a term and its frequency.
# with open(output_file, 'w') as file:
#     file.write("Common Terms\tFrequency\n")
#     for term, frequency in sorted_terms:
#         file.write(f"{term}\t{frequency}\n")

# print(f"Common terms and their frequencies (excluding specified terms and punctuation) saved to {output_file}")
import os
import shutil

full_pairs_path = 'full_pairs'
fast_facts_path = 'fast_facts'
facts_pairs_path = 'facts_pairs'

# Create the facts_pairs directory if it doesn't exist
if not os.path.exists(facts_pairs_path):
    os.makedirs(facts_pairs_path)

# Iterate over the full_pairs folders
for i in range(64):
    pair_folder = f'pair_{i}'
    source_folder = os.path.join(full_pairs_path, pair_folder)
    destination_folder = os.path.join(facts_pairs_path, pair_folder)

    # Create a corresponding folder in facts_pairs
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Copy the contents of the pair folder
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        destination_item = os.path.join(destination_folder, item)
        if os.path.isfile(source_item):
            shutil.copy2(source_item, destination_item)

    # Copy the corresponding fast facts file
    fast_facts_file = f'{i+1}.txt'  # Fast facts files are named starting from 1
    source_facts_file = os.path.join(fast_facts_path, fast_facts_file)
    destination_facts_file = os.path.join(destination_folder, 'fact.txt')
    if os.path.isfile(source_facts_file):
        shutil.copy2(source_facts_file, destination_facts_file)

print("Files successfully copied to 'facts_pairs' directory.")
