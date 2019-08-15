# This test checks that the tier types are used with correct tiers. This means 
# mainly that tier name convention has to match the type name, so in our case
# tier called orth@S1 should have the type called orthT. If it has anything else,
# an error should be raised.
import glob
import os
import xml.etree.ElementTree as ET
import re
import yaml

with open("project.yaml") as f:
    yaml_data = yaml.load(f, Loader=yaml.FullLoader)

corpus_location = ''.join(yaml_data['corpus_location'])

def test_tier_type_consistency(session_file):
    
    session_basename = os.path.basename(session_file)
    tree = ET.parse(session_file)
    root = tree.getroot()
    tiers = root.findall("TIER")

    for tier in tiers:
        tier_type = tier.get("LINGUISTIC_TYPE_REF")
        tier_type_base = tier_type[:-1]
        tier_type_base = re.sub('\(.+\)', '', tier_type_base) # this removes the parts of names in brackets
        tier_name = tier.get("TIER_ID")
        tier_name_base = tier_name.rsplit('@', 1)[0]
        tier_name_base = re.sub('\(.+\)', '', tier_name_base)
        if tier_type_base.lower() != tier_name_base.lower(): # we need to compare the lowercased names
            print("Tier–type consistency broken: " + session_basename + " has tier " + tier_name + " with type " + tier_type + ".")

session_names = glob.glob(corpus_location + "/**/*.eaf", recursive=True)

for session_name in session_names:
    test_tier_type_consistency(session_name)