# Import the necessary packages
import pandas as pd
import urllib.request, json, csv

# Import the articles dataset
with urllib.request.urlopen("http://127.0.0.1:8000/api/?format=json") as url:
    data = pd.read_json(url)

def write_txt():
    i = 1
    for index, row in data.iterrows():
        file_path = f"../notes/{row['title']}.txt"
        with open(file_path, 'w') as file:
            # convert the row to a string
            row_string = ', '.join(str(item) for item in row.values)
            # Write the row to the file, adding a newline character
            file.write(row_string + '\n')

write_txt()