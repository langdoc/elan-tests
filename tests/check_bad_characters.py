import glob
import os
import re
import yaml
from pathlib import Path
import pympi
from nltk.tokenize import word_tokenize

def check_bad_characters(elan_file_path):
    
    transcription_tier = "orthT"

    pattern = re.compile("[IÖiö]")

    session_name = Path(elan_file_path).stem

    elan_file = pympi.Elan.Eaf(file_path = elan_file_path)

    transcription_tiers = elan_file.get_tier_ids_for_linguistic_type(transcription_tier)

    for transcription_tier in transcription_tiers:

        annotation_values = elan_file.get_annotation_data_for_tier(transcription_tier)

        for annotation_value in annotation_values:

            text_content = annotation_value[2]
            text_content = re.sub("…", ".", text_content) # It seems word_tokenize doesn't handle "…"
            text_content = re.sub("\[\[unclear\]\]", "", text_content)

            words = word_tokenize(text_content)

            for word in words:

                if pattern.search(word):
                    
                    print("In " + session_name + " suspicious character in: " + word)
                    
session_names = glob.glob("**/*.eaf", recursive=True)

for session_name in session_names:
    check_bad_characters(session_name)