import glob
import os
import re
import yaml

with open("project.yaml") as f:
    yaml_data = yaml.load(f, Loader=yaml.FullLoader)

corpus_location = ''.join(yaml_data['corpus_location'])
session_name_prefixes = '|'.join(yaml_data['session_name_prefixes'])
session_name_middle = ''.join(yaml_data['session_name_middle'])

def test_name_pattern(type):
    session_names = glob.glob(type, recursive=True)

    for session_name in session_names:
        session_basename = os.path.basename(session_name)
        if not re.match(session_name_prefixes + session_name_middle, session_basename): 
            print('File ' + session_basename + ' incorrectly named!')

test_name_pattern(corpus_location + "/**/*.eaf")