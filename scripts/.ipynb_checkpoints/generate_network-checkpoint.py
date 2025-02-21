import pymupdf
import os
import shutil
import pandas as pd

# Text analysis
import spacy
import scispacy
import kindred
import en_core_web_sm
#import en_core_sci_sm

from spacy import displacy

# Networking
import networkx as nx
from pyvis import network as net
from pyvis.network import Network

print(pymupdf.__doc__)

# Define a function that deletes all files in a folder
def files_delete(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(filepath):
                os.unlink(file_path)
            elif os.path.isdri(filepath):
                shutil.rmtree(filepath)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

# Extracting text from articles
article = []

for filename in os.listdir("../input/"):
    doc = pymupdf.open(f"../input/{filename}")
    for page in doc:
        text = str(page.get_text("text"))
        text = text.replace("\n", "")
        article.append(text)
    with open(f"../build/txt/{filename}.txt", "w") as file: # Save as a text file in build for each pdf file
        file.write(str(article))

article = str(article)

# Identify Scientific vocabulary
nlp = spacy.load("en_core_web_sm") # Load the model
document = nlp(article)

# Create a Dataframe from the extracted data
for filename in os.listdir("../build/txt/"):
    data = []
    df = pd.DataFrame()
    
    url = str(f"../build/txt/{filename}")
    file = open(url, "r").read()
    document = nlp(file)
    #print([(ent.text) for ent in document.ents])
    for ent in document.ents:
        data.append(ent)

    df["weight"] = int(1)
    df["keyword"] = data
    df["filename"] = filename
    df["filename"] = df["filename"].str[:-4]

    df.to_csv(f"../build/csv/{filename}.csv")

# Build a mastersheet out of all the csv files in ./build/csv/ files
files_delete("../build/mastersheet/") # Deletes the previous mastersheet before going ahead
#nb_files = len(os.listdir("../build/csv/"))
mastersheet = pd.DataFrame(columns = ['weight', 'keyword', 'filename'])
mastersheet["weight"] = int(1)

for filename in os.listdir("../build/csv/"):
    read_csv = pd.read_csv(f"../build/csv/{filename}")
    read_csv["weight"] = int(1)
    mastersheet = pd.concat([mastersheet, read_csv], axis=0)

mastersheet.to_csv("../build/mastersheet/mastersheet.csv")


table = pd.read_csv("../table/filter.csv") # Handmade filter imported from table

# Sort the dataframe and ponderate depending on the number of occurences
filtered_keywords = pd.merge(mastersheet, table, on=["keyword"])
filtered_keywords = filtered_keywords.sort_values(by=['filename', 'keyword'])
collapsed_df = filtered_keywords.groupby(['filename', 'keyword']).size().reset_index(name="weight")

# Create the network out of the dataframe
G = nx.Graph()

for index, row in collapsed_df.iterrows():
    row['weight'] = row['weight'] / 10
    G.add_weighted_edges_from([(row['filename'], row['keyword'], row['weight'])])
    for n, nbrs in G.adj.items():
        for nbr, eattr in nbrs.items():
            wt = eattr['weight']
            if wt < 0.5: print(f"({n}, {nbr}, {wt:.3})")

## Use Pyvis to generate a dynamical network representation
g = net.Network(width= "100%", height="100%", font_color="white", select_menu=True, bgcolor="#222222", notebook=False) # bgcolor="#222222",
g = net.Network(directed = False, notebook=True)

node_degree = dict(G.degree) # Count the degree of the node

# Setting up node size attribute
#nx.set_node_attributes(G, node_degree, 'size')

nxg = G
g.from_nx(nxg)
g.toggle_physics(True) # Toggle the physic in-between nodes
g.write_html(name="../output/articles_network.html", local=True, notebook=False)

# Clear the build/ directory
files_delete("../build/csv/")
files_delete("../build/txt/")