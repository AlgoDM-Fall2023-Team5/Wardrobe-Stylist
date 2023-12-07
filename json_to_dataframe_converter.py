"""
This file is used to convert the response.json to the dataframe 
"""

import pandas as pd
import json



def json_to_df_converter(json_data):
    # Extracting image and annotations from JSON
    data = []
    for entry in json_data:
        image = entry['image']
        
        # Extracting JSON content within triple backticks
        content_start = entry['response_content'].find("```json") + 7
        content_end = entry['response_content'].rfind("```")
        
        if content_start != -1 and content_end != -1:
            json_content = entry['response_content'][content_start:content_end].strip()

            try:
                # Removing extra characters and decoding JSON
                response_content = json.loads(json_content.replace("\n", "").replace("\r", "").replace("```", ""))
                annotations = response_content['annotations']
                data.append({'image': image, 'annotations': annotations})
            except json.decoder.JSONDecodeError as e:
                print(f"Error decoding JSON for image {image}: {e}")
        else:
            print(f"Could not find valid JSON content for image {image}")

    # Creating DataFrame
    df = pd.DataFrame(data)
    return df


if __name__ == '__main__':
    # Load JSON data from file
    with open('responses.json', 'r') as file:
        json_data = json.load(file)

    df = json_to_df_converter(json_data)

    df.to_csv("tags.csv",index=False)