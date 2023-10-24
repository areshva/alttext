import matplotlib.pyplot as plt

output_file = 'common_terms.txt'

terms = []
frequencies = []

with open(output_file, 'r') as file:
    next(file)  
    for line in file:
        term, frequency = line.strip().split('\t')
        terms.append(term)
        frequencies.append(int(frequency))

plt.figure(figsize=(12, 6))
plt.plot(terms[:10], frequencies[:10], marker='o', linestyle='-', color='b')
plt.title('Top 10 Common Terms and Their Frequencies')
plt.xlabel('Terms')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()
