

# from fastapi import FastAPI
# from controller import provider_router
# import uvicorn

# app = FastAPI(title="MatchNP project", version="1.0")

# app.include_router(provider_router)

# if __name__ == "__main__":
#     # Run the application with Uvicorn
#     uvicorn.run("main:app", host="localhost", port=8000, reload=True)


import json
import pandas as pd
import re

# Path to the JSON file
json_file_path = r"utils\\qa.json"
excel_file_path = r"utils\\qa_data.xlsx"


def processData(textContent):
    # Replace ">" with an empty string
    text = textContent.replace(">", "")

    data = text.split("\n")
    paragraphs = []
    join_text = ""

    for each in data:
        if len(each) > 0 and   re.search(r'[a-zA-Z0-9]', each):  # If the line is not empty
            join_text += "\n" + each  # Append the current line to the paragraph
        else:
            if join_text:  # If there's some content in join_text (i.e., non-empty paragraph)
                paragraphs.append(join_text.strip())  # Append the collected paragraph to collect_data
                join_text = ""  # Reset join_text for the next paragraph

    # Check if there's any remaining text after the last paragraph
    if join_text:
        paragraphs.append(join_text.strip())

    unwanted_words = ["http", "Next steps:", "Honorarium:"]

    cleaned_paragraphs = [
        para.strip() for para in paragraphs
        if para.strip() and not any(word in para for word in unwanted_words) 
    ]

    # Join the cleaned paragraphs into a single string
    cleaned_text = "\n\n".join(cleaned_paragraphs)

    # Print each cleaned paragraph for verification
    # for para in cleaned_paragraphs:
    #     print(para)
    #     print("................................")
    return cleaned_text


try:
    # Read JSON data
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Clean the 'text_content' field
    for each_data in data:
        each_data['text_content'] = processData(each_data['text_content'])
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel
    df.to_excel(excel_file_path, index=False, encoding='utf-8', sheet_name='QA Data')
    print(f"Excel file created successfully at: {excel_file_path}")

except FileNotFoundError:
    print(f"The file {json_file_path} was not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
