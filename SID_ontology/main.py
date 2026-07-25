import xml.etree.ElementTree as xml
import random
import csv
from random import randrange
from datetime import datetime
from datetime import timedelta

class ontology_entry:
    def __init__(self, domain_name, domain_id, abe_name, abe_id, be_name, be_id, attr_name, attr_id, doc):
        self.domain_name = domain_name
        self.domain_id = domain_id
        self.abe_name = abe_name
        self.abe_id = abe_id
        self.be_name = be_name
        self.be_id = be_id
        self.attr_name = attr_name
        self.attr_id = attr_id
        self.doc = doc

def create_attrs():
    vocabulary = []
    f = open("attrs.rdf", "wt")
    with open('SID_attrs.csv', encoding='utf-8') as input_swe:
        reader = csv.DictReader(input_swe, delimiter=';')
        for line in reader:
            if vocabulary.count(str(line['Attribute_Name'])) == 0:
                print(line)
                f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#' + str(line['Attribute_Name']) + ' -->\n\n')
                f.write('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#' + str(line['Attribute_Name']) + '">\n')
                f.write('<rdf:type rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#Attribute"/>')
                f.write('<TMF_SID_v1:hasOrigin>' + str(line['Origin']) + '</TMF_SID_v1:hasOrigin>\n')
                f.write('<TMF_SID_v1:hasStereotype>' + str(line['Stereotype']) + '</TMF_SID_v1:hasStereotype>')
                f.write('<rdf:label>' + str(line['Attribute_Name']) + '</rdf:label>\n')
                f.write('<rdfs:comment>' + str(line['Documentation'].replace('\n', ' ')) + '</rdfs:comment>\n</owl:NamedIndividual>\n\n')
                vocabulary.append(str(line['Attribute_Name']))
        f.close()
    return 1

def create_nodes():
    ontology = []
    SID_objects = []
    f = open("nodes.rdf", "wt")
    with open('SID_ABE.csv', encoding='utf-8') as input_swe:
        reader = csv.DictReader(input_swe, delimiter=';')
        j = 1 #Domain counter
        k = 1 #ABE counter
        l = 1 #BE counter
        m = 1 #Attr counter
        for line in reader:
            if line['ABE_Name'] != '':
                domain_name = line['ABE_Name'].split('Business Entity.')
                if len(domain_name) > 1:
                        ontology.append(ontology_entry(domain_name[1], j,'',-1,'',-1,'',-1, line['Documentation']))
                        j = j + 1
                        continue
                abe_name = line['ABE_Name']
                SID_objects.append(abe_name)
                ontology.append(ontology_entry('', -1, abe_name, k, '', -1, '', -1, line['Documentation']))
                k = k + 1
                continue
            elif line['BE_Name'] != '':
                be_name = line['BE_Name']
                SID_objects.append(be_name)
                ontology.append(ontology_entry('', -1, '', -1, be_name, l, '', -1, line['Documentation']))
                l = l + 1
                continue
            elif line['Attribute_Name'] != '':
                attr_name = line['Attribute_Name']
                ontology.append(ontology_entry('', -1, '', -1, '', -1, attr_name, m, ''))
                m = m + 1
                continue

        i = 0
        N = len(ontology)
        while i < N:
            if ontology[i].domain_name != '':
                f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#Business_Entity.' + str(ontology[i].domain_name) + ' -->\n\n')
                f.write('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#Business_Entity.' + str(ontology[i].domain_name)+ '">\n')
                f.write('<rdf:type rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#TMFDomain"/>\n')
                f.write('<rdf:label>Business Entity.' + str(ontology[i].domain_name) + '</rdf:label>\n')
                f.write('<rdfs:comment>' + str(ontology[i].doc) + '</rdfs:comment>\n</owl:NamedIndividual>\n\n')
            if (ontology[i].abe_name != '') and (ontology[i+1].abe_name != ''):
                i = i + 1
                continue
            if (ontology[i].abe_name != '') and (ontology[i + 1].abe_name == ''):
                f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#' + str(ontology[i].abe_name) + ' -->\n\n')
                f.write('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#' + str(ontology[i].abe_name) + '">\n')
                f.write('<rdf:type rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#ABE"/>\n')
                add_counter = 1
                while True:
                    if (i + add_counter >= N):
                        break
                    if (ontology[i + add_counter].abe_name != ''):
                        break
                    if ontology[i + add_counter].be_name != '':
                        f.write('<TMF_SID_v1:hasBE rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#' + str(ontology[i + add_counter].be_name) + '"/>\n')
                    add_counter = add_counter + 1

                f.write('<rdf:label>' + str(ontology[i].abe_name) + '</rdf:label>\n')
                f.write('<rdfs:comment>'  + str(ontology[i].doc) + '</rdfs:comment>\n</owl:NamedIndividual>\n\n')
            if (ontology[i].be_name != ''):
                f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#' + str(ontology[i].be_name) + ' -->\n\n')
                f.write('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#' + str(ontology[i].be_name) + '">\n')
                f.write('<rdf:type rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#BE"/>\n')
                add_counter = 1
                while True:
                    if (i + add_counter >= N):
                        break
                    if (ontology[i + add_counter].be_name != ''):
                        break
                    if ontology[i + add_counter].attr_name != '':
                        f.write('<TMF_SID_v1:hasAttribute rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_SID_v1#' + str(ontology[i + add_counter].attr_name) + '"/>\n')
                    add_counter = add_counter + 1
                f.write('<rdf:label>' + str(ontology[i].be_name) + '</rdf:label>\n')
                f.write('<rdfs:comment>' + str(ontology[i].doc) + '</rdfs:comment>\n</owl:NamedIndividual>\n\n')
            i = i + 1

        for line in ontology:
            print('ontology=',line.domain_name, line.domain_id)
        f.close()
        f = open("SID_objects.csv", "wt")
        f.write('sid_object\n')
        for line in SID_objects:
            f.write(str(line) + '\n')
        f.close()

if __name__ == "__main__":
    create_attrs()
    create_nodes()
