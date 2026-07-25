import csv
import nltk
import re

def camel_case_to_tokens(text):
    words = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', text).split()
    return [token for word in words for token in nltk.word_tokenize(word)]

def domain_ont_integration():
    DB_Ontology_classes = []
    DB_Ontology_classes_tokens = []
    DB_Ontology_properties = []
    DB_Ontology_properties_tokens = []
    Custom_Ontology_classes = []
    Custom_Ontology_classes_tokens = []
    Custom_Ontology_properties = []
    Custom_Ontology_properties_tokens = []
    matches_custom_classes = []
    matches_custom_properties = []

    with open('Custom_ontology_classes.csv', encoding='utf-8') as input_data:
        reader = csv.DictReader(input_data, delimiter=';')
        for line in reader:
            Custom_Ontology_classes.append(line['class'])
            tokens = camel_case_to_tokens(line['class'])
            Custom_Ontology_classes_tokens.append(tokens)

    with open('DB_ontology_classes.csv', encoding='utf-8') as input_data:
        reader = csv.DictReader(input_data, delimiter=';')
        for line in reader:
            DB_Ontology_classes.append(line['class'])
            tokens = camel_case_to_tokens(line['class'])
            DB_Ontology_classes_tokens.append(tokens)

    i = 0
    for item in Custom_Ontology_classes:
        custom_item = item
        j = 0
        score = 0
        for item_db in DB_Ontology_classes:
            if item_db.capitalize() == item.capitalize():
                db_item = item_db
                score = 100
                matches_custom_classes.append([custom_item, db_item, score])
            if Custom_Ontology_classes_tokens[i] in DB_Ontology_classes_tokens[j] and score != 100:
                db_item = item_db
                score = 10
                matches_custom_classes.append([custom_item, db_item, score])
            if score == 0:
                for sub_custom_item in Custom_Ontology_classes_tokens[i]:
                    if sub_custom_item in DB_Ontology_classes_tokens[j]:
                        db_item = item_db
                        score = 1/len(DB_Ontology_classes_tokens[j])
                        matches_custom_classes.append([custom_item, db_item, score])
            score = 0
            j = j + 1
        i = i + 1
    matches_custom_classes.sort(key=lambda x: x[2], reverse=True)
    f = open("matches_custom_classes.csv", "wt")
    f.write('custom_item,db_item,score\n')
    for item in matches_custom_classes:
        f.write(item[0]+','+item[1]+','+str(item[2])+'\n')
    f.close()

    with open('Custom_Ontology_properties.csv', encoding='utf-8') as input_data:
        reader = csv.DictReader(input_data, delimiter=';')
        for line in reader:
            Custom_Ontology_properties.append(line['property'])
            tokens = camel_case_to_tokens(line['property'])
            Custom_Ontology_properties_tokens.append(tokens)

    with open('DB_Ontology_properties.csv', encoding='utf-8') as input_data:
        reader = csv.DictReader(input_data, delimiter=';')
        for line in reader:
            DB_Ontology_properties.append(line['property'])
            tokens = camel_case_to_tokens(line['property'])
            DB_Ontology_properties_tokens.append(tokens)

    i = 0
    for item in Custom_Ontology_properties:
        custom_item = item
        j = 0
        score = 0
        for item_db in DB_Ontology_properties:
            if item_db.capitalize() == item.capitalize():
                db_item = item_db
                score = 100
                matches_custom_properties.append([custom_item, db_item, score])
            if Custom_Ontology_properties_tokens[i] in DB_Ontology_properties_tokens[j] and score != 100:
                db_item = item_db
                score = 10
                matches_custom_properties.append([custom_item, db_item, score])
            if score == 0:
                for sub_custom_item in Custom_Ontology_properties_tokens[i]:
                    if sub_custom_item in DB_Ontology_properties_tokens[j]:
                        db_item = item_db
                        score = 1/len(DB_Ontology_properties_tokens[j])
                        matches_custom_properties.append([custom_item, db_item, score])
            score = 0
            j = j + 1
        i = i + 1
    matches_custom_properties.sort(key=lambda x: x[2], reverse=True)
    f = open("matches_custom_properties.csv", "wt")
    f.write('custom_item,db_item,score\n')
    for item in matches_custom_properties:
        f.write(item[0]+','+item[1]+','+str(item[2])+'\n')
    f.close()
    return 1


if __name__ == '__main__':
    nltk.download('punkt_tab')
    domain_ont_integration()


