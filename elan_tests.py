import glob
import os
import re
import yaml
from pathlib import Path
import pympi
from nltk.tokenize import word_tokenize
import xml.etree.ElementTree as ET
from uralicNLP import uralicApi

def parse_project_yaml(yaml_file = "project.yaml"):

    with open("project.yaml") as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)

    corpus_location = ''.join(yaml_data['corpus_location'])
    session_name_prefixes = '|'.join(yaml_data['session_name_prefixes'])
    session_name_middle = ''.join(yaml_data['session_name_middle'])
    manually_verified_files = yaml_data['manually_verified_files']
    
    return(corpus_location, session_name_prefixes, session_name_middle, manually_verified_files)

corpus_location, session_name_prefixes, session_name_middle, manually_verified_files = parse_project_yaml("project.yaml")

def test_session_names(elan_file_path):
    
    session_basename = os.path.basename(elan_file_path)
    if not re.match(session_name_prefixes + session_name_middle, session_basename): 
        print('File ' + session_basename + ' incorrectly named!')

def test_tier_types(session_file, types):

    session_basename = os.path.basename(session_file)
    
    tree = ET.parse(session_file)

    root = tree.getroot()
    
    for type in types:
        if not root.findall("LINGUISTIC_TYPE[@LINGUISTIC_TYPE_ID='" + type + "']"):           
            print("Session " + session_basename + " is missing tier type " + type + ".")

def test_tier_existence(elan_file_path, tier_prefixes):
    
    session_basename = os.path.basename(elan_file_path)
    
    tree = ET.parse(elan_file_path)
    root = tree.getroot()
    tiers = root.findall("TIER")
    
    tier_prefix_list = []
    
    for tier in tiers:
        
        tier_name = tier.get("TIER_ID")
        tier_name_base = tier_name.rsplit('@', 1)[0]
        
        tier_prefix_list.append(tier_name_base)
        
    for tier_prefix in tier_prefixes:
        
        if tier_prefix not in tier_prefix_list:
            
            print(f"Session {session_basename} is missing tier {tier_prefix}." )

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


def check_illegal_characters(elan_file_path, verification_list, tier_type = "orthT", unwanted_characters = "[IÖiö]"):

    pattern = re.compile(unwanted_characters)

    session_name = Path(elan_file_path).stem

    if session_name not in verification_list:
    
        elan_file = pympi.Elan.Eaf(file_path = elan_file_path)

        transcription_tiers = elan_file.get_tier_ids_for_linguistic_type(tier_type)

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


def test_session_name_meta(session_name, meta_json):
    
    session_names = set()
    
    for session in meta_json:
        
        session_names.add(session['session_name'])
        
    if session_name not in session_names:
        
        print(f'Session {session_name} not found from metadata!')

def test_participant_meta(elan_file_path, meta_json, tier_type):
    
    session_name = Path(elan_file_path).stem

    elan_file = pympi.Elan.Eaf(file_path = elan_file_path)

    transcription_tiers = elan_file.get_tier_ids_for_linguistic_type(tier_type)
    
    participants = []
    
    for tier in transcription_tiers:
        
        participants.append(tier.rsplit('@', 1)[1])
    
    session_participant_pairs = []
    
    for session in meta_json:
        
        for participant in session['participants']:
        
            session_participant_pairs.append({session['session_name']:participant['participant']})
            
    for participant in participants:
        
        if {session_name:participant} not in session_participant_pairs:
            
            print(f'Participant {participant} missing from {session_name}!')

# This function checks which words aren't recognized by FST of a given language
def print_unknown_words(elan_file_path, transcription_tier = "orthT", language = "kpv"):
    
    session_name = Path(elan_file_path).stem

    elan_file = pympi.Elan.Eaf(file_path = elan_file_path)

    transcription_tiers = elan_file.get_tier_ids_for_linguistic_type(transcription_tier)

    missed_annotations = []

    for transcription_tier in transcription_tiers:

        annotation_values = elan_file.get_annotation_data_for_tier(transcription_tier)

        for annotation_value in annotation_values:

            text_content = annotation_value[2]
            text_content = re.sub("…", ".", text_content) # It seems word_tokenize doesn't handle "…"
            text_content = re.sub("\[\[unclear\]\]", "", text_content)

            words = word_tokenize(text_content)

            for word in words:

                analysis = uralicApi.analyze(word, language)
                if not analysis:
                    missed_annotations.append(word)

    for count, elem in sorted(((missed_annotations.count(e), e) for e in set(missed_annotations)), reverse=True):
        print('%s (%d)' % (elem, count))

def create_eaf(session_directory = 'test', session_name = 'test', speakers = ['S1', 'S2'], author = 'IKDP'):

    filename = f'{session_name}.eaf'
    
    elan_file = pympi.Elan.Eaf(file_path = None, author = author)

    elan_file.add_linguistic_type(lingtype='refT', timealignable=True, graphicreferences=False)
    elan_file.add_linguistic_type(lingtype='orthT', timealignable=False, graphicreferences=False, constraints='Symbolic_Association')
    elan_file.add_linguistic_type(lingtype='ft-rusT', timealignable=False, graphicreferences=False, constraints='Symbolic_Association')
    elan_file.add_linguistic_type(lingtype='ft-engT', timealignable=False, graphicreferences=False, constraints='Symbolic_Association')
    
    elan_file.add_linked_file(file_path = f'{session_name}.wav', mimetype = 'audio/x-wav')

    for speaker in speakers:
        elan_file.add_tier(tier_id=f'ref@{speaker}', ling='refT')
        elan_file.add_tier(tier_id=f'orth@{speaker}', ling='orthT', parent= f'ref@{speaker}')
        elan_file.add_language(lang_def = 'http://cdb.iso.org/lg/CDB-00131321-001', lang_id = 'kpv', lang_label = 'Komi-Zyrian (kpv)')
        elan_file.add_tier(tier_id=f'word@{speaker}', ling='wordT', parent= f'orth@{speaker}', language='kpv')

    # This tier is created automatically
    elan_file.remove_tier(id_tier='default')

    elan_file.to_file(file_path = f'{session_directory}/{filename}')        

# MESSY OLD PARTS, NOT CURRENTLY USED

def get_elan_participants(elan_file):

    tree = ET.parse(elan_file)
    root = tree.getroot()
    tiers = root.findall("TIER")
    participants_file = set()

    for tier in tiers:
        tier_id = tier.attrib['TIER_ID']
        if '@' in tier_id:
            speaker = tier_id.rsplit('@', 1)[1]
            participants_file.add(speaker)

    return(participants_file)

# This uses those functions defined above into an ELAN file

def match_elan_and_meta(elan_file):

    session_basename = os.path.basename(elan_file)

    session_noext = os.path.splitext(session_basename)[0]

    meta_participants = get_meta_participants(session_noext)
    elan_participants = get_elan_participants(elan_file)
    
    if not elan_participants.issubset(meta_participants):
        print("One of participants " + repr(elan_participants) + " in file " + session_basename + " not metadata.")

        