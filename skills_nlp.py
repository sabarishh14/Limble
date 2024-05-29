# imports
import spacy
from spacy.matcher import PhraseMatcher
import json
from nlp_skills.general_params import SKILL_DB
from nlp_skills.skill_extractor_class import SkillExtractor

def skills(job_description):
    nlp = spacy.load("en_core_web_lg")
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
    annotations = skill_extractor.annotate(job_description)
    skills=[]

    if 'full_matches' in annotations["results"]: 
        for i in annotations["results"]['full_matches']:
            skills.append([i['skill_id'],i['doc_node_value']])

    if 'ngram_scored' in annotations["results"]:
        for i in annotations["results"]['ngram_scored']:
            skills.append([i['skill_id'],i['doc_node_value']])

    with open("buckets/skills_processed.json") as json_file:
        data = json.load(json_file)

    skills_final=[]
    for i in skills:
        skills_final.append(data[i[0]])

    skills_name=[]
    for j in skills_final:
        skills_name.append([j['skill_name']])
        
    x=""
    for i in skills_name:
        x+=i[0]+", "

    return(x[:-2])