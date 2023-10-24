import openai
import os
import json
import unicodedata
from tqdm import tqdm

openai.api_key = os.getenv("alt-text-key") # set your API key here

MODEL = "text-davinci-003" #(?)

categories = {
    "Colors and Descriptions": {"blue", "light", "bright", "white", "black", "red", "orange", "yellow", "pink", "green", "color", "colorful", "shades"},
    "Spatial Directions and Positions": {"left", "right", "top", "bottom", "center", "below", "above", "up", "down", "side"},
    "Astronomical Terms": {"galaxies", "galaxy", "star", "stars", "telescope", "planet", "nebula", "rings", "dust", "gas", "core", "disk", "cluster", "sphere", "arms", "area", "field", "outer", "distant", "region", "central", "material", "thin"},
    "Visualization Elements": {"image", "graphic", "illustration", "infographic", "arrows", "key", "dots", "mirror", "lines", "shapes", "panel", "sizes", "oval", "wispy"},
    "Telescope and Instrument Names": {"webb", "nircam", "microns", "nirspec", "miri"},
    "Text and Labels": {"labeled", "titled", "showing", "shows", "points", "appear", "throughout", "representing"},
    "Measurement and Data": {"scale", "wavelength", "diffraction", "spectrum", "brightness"},
    "Direction and Movement": {"there", "out", "around", "toward", "horizontal", "vertical", "across", "between", "create", "sizes"},
    "Quantitative Terms": {"three", "more", "few", "many", "most", "some", "about", "time", "while"},
    "Other Terms": {"arrows", "key", "clock", "indicate", "field", "cloud", "clouds", "also", "hubble", "exoplanet", "used", "miri", "oval"}
}
INSTRUCTION = "I will provide you with some alt-texts along with the pictures they describe. rate how well each performs across all ten dimensions. for each dimension, give the alt text a floating point score, then combine all ten scores in a vector to represent the total rating of the text. Please also include scores for conciseness, accuracy, clarity and relevance."

INCONTEXT_EXAMPLE = "ALt-Text: A star cluster within a nebula. The center of the image contains arcs of orange and pink gas that form a boat-like shape. One end of these arcs points to the top right of the image, while the other end points toward the bottom left. Another plume of orange and pink gas expands from the center to the top left of the image. To the right of this plume is a large cluster of white stars. There are more of these white stars and a few galaxies of different sizes spread throughout the image.\n\n Image: xxxxx \n\n Score : [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0]"


def load_data(filename, n_entries = -1) -> list:
    data = [json.loads(jline) for jline in open(filename, 'r')]
    data = data[:n_entries]
    return data

ANIL_R3_TEST = load_data('anli_v1.0/R3/test.jsonl', 100)

def make_query(sample):
    context_str, hypothesis_str = sample['context'], sample['hypothesis']
    query = f"{INSTRUCTION} \n\n {INCONTEXT_EXAMPLE} \n\n"
    query += f"Context: {context_str} \n\n Hypothesis: {hypothesis_str} \n\n Relation:"
    return query

# def extract_label(output):
#     label = None
#     if "entailment" in output or "entails" in output or "Entailment" in output:
#         label = "e"
#     elif "contradiction" in output or "contradicts" in output or "Contradiction" in output:
#         label = "c"
#     elif "neutral" in output or "Neutral" in output:
#         label = "n"
#     return label

def model_inference(model, query, max_tokens=50, temperature=0, top_p=1.0):
    response = openai.Completion.create(engine=model, prompt=query, max_tokens=max_tokens, 
                                        temperature=temperature,
                                        top_p=top_p)
    output = response['choices'][0]['text']
    pred_label = extract_label(output)
    return pred_label

def accuracy_score(ground_truths, predictions):
    correct = 0
    for gt, pred in zip(ground_truths, predictions):
        if gt == pred:
            correct += 1
    return correct / len(ground_truths)

def evaluateModel(model, eval_dataset):
    ground_truths = [sample['label'] for sample in eval_dataset]
    predictions = []

    for sample in tqdm(eval_dataset):
        query = make_query(sample)
        output = model_inference(model, query)
        predictions.append(output)

    return ground_truths, predictions, accuracy_score(ground_truths, predictions)

groundtruth, predictions, accuracy = evaluateModel(MODEL, ANIL_R3_TEST)

with open("result.txt", "w") as text_file:
    text_file.write("gt: " + str(groundtruth) + "\npr: " + str(predictions) + "\nAccuracy: " + str(accuracy) + "\n")

# queries = []

# for sample in tqdm(ANIL_R3_TEST):
#     query = make_query(sample)
#     queries.append(query)

# with open("queries.txt", "w") as text_file:
#     for q in queries:
#         text_file.write(q + "\n\n\n\n\n")