# This test will check that some tier types are present
import glob
import os
import xml.etree.ElementTree as ET

def test_tier_types(session_file, types):

    session_basename = os.path.basename(session_file)
    
    tree = ET.parse(session_file)

    root = tree.getroot()
    
    for type in types:
        if not root.findall("LINGUISTIC_TYPE[@LINGUISTIC_TYPE_ID='" + type + "']"):           
            print("Session " + session_basename + " is missing tier type " + type + ".")

session_names = glob.glob("**/*.eaf", recursive=True)

for session_name in session_names:
    test_tier_types(session_name, types = ['refT', 'orthT', 'ft-rusT', 'ft-engT'])
