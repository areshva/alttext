
import os
import base64
import openai

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



openai.api_key = "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"


# def encode_image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
#     return encoded_string

# def get_image_data_uri(base64_string, image_path):
#     mime_type = "image/jpg"  # Default to JPEG; adjust based on actual image type
#     if image_path.lower().endswith(".png"):
#         mime_type = "image/png"
#     elif image_path.lower().endswith(".gif"):
#         mime_type = "image/gif"
#     return f"data:{mime_type};base64,{base64_string}"
import ast

#using urls insteadof encoding to base64 str
with open('url_pairs/image_description_urls.txt', 'r') as file:
    lines = [line.strip().strip("(),'") for line in file if line.strip()]
    image_urls = lines

#based on response structure
def parse_scores_to_vector(response_text):
    lines = [line.strip() for line in response_text.strip().split('\n') if line]
    scores_vector = []

    for line in lines:
        if 'Vector'in line:
            # get the list from the string
            vector_str = line.split(':', 1)[1].strip()
            try:
                #we safely evaluate the string representation of a list to a literal list
                scores_vector = ast.literal_eval(vector_str)
            except (ValueError, SyntaxError) as e:
                print(f"Could not parse the vector: {vector_str}")
                scores_vector = None
        else:
            parts = line.split(':')
            if len(parts) == 2:
                _, score_str = parts
                score_cleaned = score_str.strip()
                try:
                    score = float(score_cleaned)
                    scores_vector.append(score)
                except ValueError as e:
                    # If there's a ValueError, it might be due to the 'Vector:' line or something.
                    # We can safely continue because the vector has already been parsed.
                    continue
    
    return scores_vector


def evaluate_description(text, image_url,categories):
    

  
    prompt = (
    "Please evaluate the following alt-text description in relation to the accompanying image, focusing on two aspects for the first ten dimensions: the usage of specific key terms and the adherence to the criteria detailed in each dimension. "
    "For the remaining four dimensions, evaluate based on the descriptions provided. Provide a floating point score between 0 (poor) and 1 (excellent) for each dimension. "
    "Combine all 14 scores in a vector to represent the total rating of the text. "
    "\n\nEvaluation criteria and key terms for each dimension:\n"
)

    for category, terms in categories.items():
        terms_list = ", ".join(terms)
        prompt += f"- {category}: Evaluate based on how well the text uses terms such as {terms_list} and the criteria detailed for the dimension.\n"

    prompt += (
        "- Conciseness: Is the text concise yet informative?\n"
        "- Accuracy: How accurate is the description in representing the image?\n"
        "- Clarity: Is the description clear and easy to understand?\n"
        "- Relevance: Are all parts of the description relevant to the image?\n\n"
        f"Description: \"{text}\"\n"
        f"Image URL: {image_url}\n"
        "Present the scores in a vector format, corresponding to the order of the dimensions listed above."
    )



   
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=600  
    )
    print( response['choices'][0]['text'])  
     
    #  'response.choices[0].text' has the text response from OpenAI
    scores_vector = parse_scores_to_vector(response.choices[0].text)
    return scores_vector


directory = "full_pairs"
output_file = "evaluation_scores.txt"



with open(output_file, 'w') as file:
    for i, image_url in enumerate(image_urls):
        if i >= 3:  # Stop after processing 5 images
            break
        pair_folder = f"pair_{i}"
        pair_path = os.path.join(directory, pair_folder)

        with open(os.path.join(pair_path, 'description.txt'), 'r') as good_file:
            good_text = good_file.read()

        with open(os.path.join(pair_path, 'b_description.txt'), 'r') as bad_file:
            bad_text = bad_file.read()

        good_scores_vector = evaluate_description(good_text, image_url, categories)
        bad_scores_vector = evaluate_description(bad_text, image_url, categories)

        print(good_text)
        print(bad_text)

        
        file.write(f"Scores for {pair_folder} - Good Text: {good_scores_vector}\n")
        file.write(f"Scores for {pair_folder} - Bad Text: {bad_scores_vector}\n")
        file.write('\n')  

print(f"Scores have been written to {output_file}")

#send etha full zip of img/txt 
#work on tailoring prompt
#work on scraping composite imgs
#check if api can handle img
#Then, I took the 'bad' PowerPoint texts that Ethat got and put those in each of the folders too. So now we have 64 sets of img-good text-bad text sets. 