import csv
import nltk
import re

def camel_case_to_tokens(text):
    words = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', text).split()
    return [token for word in words for token in nltk.word_tokenize(word)]

def domain_ont_integration():
    SID_objects = []
    SID_objects_tokens = []
    common_ont_classes = []
    common_ont_classes_tokens = []
    matches = []

    with open('SID_objects.csv', encoding='utf-8') as input_data:
        reader = csv.DictReader(input_data, delimiter=';')
        for line in reader:
            SID_objects.append(line['sid_object'])
            tokens = camel_case_to_tokens(line['sid_object'])
            SID_objects_tokens.append(tokens)

    with open('toco_classes.csv', encoding='utf-8') as input_data:
        reader = csv.DictReader(input_data, delimiter=';')
        for line in reader:
            common_ont_classes.append(line['Classes'])
            tokens = camel_case_to_tokens(line['Classes'])
            common_ont_classes_tokens.append(tokens)

    i = 0
    for item in common_ont_classes:
        common_item = item
        j = 0
        for item_domain in SID_objects:
            #print(item_domain, item)
            if item_domain.capitalize() == item.capitalize():
                domain_item = item_domain
                score = 100
                matches.append([common_item, domain_item, score])
            if common_ont_classes_tokens[i] in SID_objects_tokens[j]:
                domain_item = item_domain
                score = 10
                matches.append([common_item, domain_item, score])
            for sub_comon_item in common_ont_classes_tokens[i]:
                if sub_comon_item in SID_objects_tokens[j]:
                    domain_item = item_domain
                    score = 1/len(SID_objects_tokens[j])
                    matches.append([common_item, domain_item, score])
            j = j + 1
        i = i + 1
    matches.sort(key=lambda x: x[2], reverse=True)
    f = open("matches_common_domain.csv", "wt")
    f.write('common_item,domain_item,score\n')
    for item in matches:
        f.write(item[0]+','+item[1]+','+str(item[2])+'\n')
    f.close()
    #print(matches)
    return 1


if __name__ == '__main__':
    nltk.download('punkt_tab')
    domain_ont_integration()


