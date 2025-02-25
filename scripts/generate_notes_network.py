import os
import pandas as pd

# Building a network
import networkx as nx
from pyvis import network as net
from pyvis.network import Network

# Hashtag extraction
import re

# Define useful functions
# Define a function that recognize and extract hashtags from a text
def hashtag_extract(text):
    words = text.split()
    hashtags = [word for word in words if word.startswith("#")]
    return hashtags
# Define a function to save the text
#def save_text():
#    print("hello world!")

# Defin a function to delete .txt files after import
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

# Extract the hashtags from notes
hashtag_list = []
df = pd.DataFrame()

for note in os.listdir("../notes/"):
    url = os.path.join("..", "notes", note)
    with open(url, "r") as file:
        content = file.read()
        hashtags = hashtag_extract(content)  # Capture the return value
        hashtag_list.extend(hashtags)  # Use .extend() to add each hashtag individually

        # Append each hashtag with filename and weight
        df = pd.concat([df, pd.DataFrame([{"keyword": hashtag, "filename": note, "weight": 1} for hashtag in hashtags])], ignore_index=True)

# Create the network out of the notes
G = nx.Graph()

for index, row in df.iterrows():
    G.add_weighted_edges_from([(row['filename'], row['keyword'], row['weight'])])
    for n, nbrs in G.adj.items():
        for nbr, eattr in nbrs.items():
            wt = eattr['weight']
            if wt < 0.5: print(f"({n}, {nbr}, {wt:.3})")

## Use Pyvis to generate a dynamical network representation
g = net.Network(width= "100%", height="100%", font_color="white", select_menu=True, bgcolor="#222222", notebook=False) # bgcolor="#222222",
g = net.Network(directed = False, notebook=False)
#g = net.add_event_listener("selectNode", save_text()) #Save the text from filename

node_degree = dict(G.degree) # Count the degree of the node

# Setting up node size attribute
#nx.set_node_attributes(G, node_degree, 'size')

nxg = G
g.from_nx(nxg)
g.toggle_physics(True) # Toggle the physic in-between nodes
g.write_html(name="../output/notes_network.html", local=True, notebook=False)


# Delete the txt files
files_delete("../notes/")
