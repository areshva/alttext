import matplotlib.pyplot as plt

output_file = 'common_categories.txt'

categories = []
frequencies = []

with open(output_file, 'r') as file:
    next(file)  
    for line in file:
        category, frequency = line.strip().split('\t')
        categories.append(category)
        frequencies.append(int(frequency))

plt.figure(figsize=(10, 6))
plt.plot(categories, frequencies, marker='o', linestyle='-', color='b')
plt.title('Category Frequencies')
plt.xlabel('Category')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.grid(True)

plt.tight_layout()
plt.show()
