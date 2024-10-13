import spacy

nlp = spacy.load("en_core_web_sm")

def process_nlp_query(query):
    doc = nlp(query)
    
    # Extract task details
    task = {
        'title': '',
        'description': '',
        'due_date': None
    }
    
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            task['due_date'] = ent.text
        elif ent.label_ == 'TIME':
            task['due_date'] = f"{task['due_date']} {ent.text}" if task['due_date'] else ent.text
    
    # Extract task title and description
    verb_found = False
    for token in doc:
        if token.pos_ == 'VERB' and not verb_found:
            verb_found = True
            task['title'] += token.text + ' '
        elif verb_found:
            task['description'] += token.text + ' '
    
    task['title'] = task['title'].strip()
    task['description'] = task['description'].strip()
    
    return task