
Blackbird read through selected scientific articles (.PDF) and personnal notes and output a network out of 
keywords automatically extracted from it.

# Key features
- Uses Django framework to build a html based graphic interface.
- Extraction of .md files from notes/ into mySQL database.
- Automated markdown view of the database into a template.html.
- Generation of a Pyvis Network of hashtags from notes (html output).
- Screen through pdfs and identify scientific vocabulary.
- Generation of a Pyvis Network from filtered scientific vocabulary.

## Coming Updates
- API to extract database into txt to analyse.
- Adaptative navbar for easy navigation on computer/tablet/phone.
- User interface for login.
- Better esthetic of the website.

# Install
```bash
python -m venv --upgrade-deps venv
venv/bin/python -m ensurepip
venv/bin/python -m pip install -upgrade setuptools pip wheel
venv/bin/python -m pip install -r requirements.txt
```

# Usage
## Activate the virtual environment
```bash
source venv/bin/activate
```

## Transfer .md into db.sqlite
.md files can be stored in notes/ for extraction. To transfer .md notes into the database run:
```bash
python manage.py import_data
```
The script will bug if you try to extract .md files that were previously extracted.

## Extract sqlite into .txt files
_in development_

## Generate a network from the hashtags in .txt notes
The script uses re, Networkx and Pyvis to generate a network from hashtags found in the content of the .txt files.
 The script extract content from .txt files stored in /notes.
![Example of a note from which to extrqct hashtags](https://i.ibb.co/n8fbRWDn/blackbird-1.png)
 All files are automatically deleted after processed.
 The network can be retrieved in the output/ folder.
```bash
cd scripts/
python generate_notes_network.py
```

## Generate a network from filtered scientific terms found in pdf articles.
1) Edit the terms to filter.
```bash
nano table/filter.csv
```
2) Run the script (takes a lot of ram).
```bash
cd scripts/
python generate_network.py
```
The network generated can then be retrieved in the output/ directory.
