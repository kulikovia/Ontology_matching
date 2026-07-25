import xml.etree.ElementTree as xml
import random
import csv
from random import randrange
from datetime import datetime
from datetime import timedelta

class SID_ontology_entry:
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

class eTOM_ontology_entry:
    def __init__(self, process_name, process_id, level, description, short_description, domain, v_group, original_id, m_level):
        self.process_name = process_name
        self.process_id = process_id
        self.level = level
        self.description = description
        self.short_description = short_description
        self.domain = domain
        self.v_group = v_group
        self.original_id = original_id
        self.m_level = m_level

def create_SID_attrs():
    vocabulary = []
    f = open("SID_attrs.rdf", "wt", encoding='utf-8')
    with open('src/SID_attrs.csv') as input_swe:
        reader = csv.DictReader(input_swe, delimiter=';')
        for line in reader:
            if vocabulary.count(str(line['Attribute_Name'])) == 0:
                print(line)
                f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#' + str(line['Attribute_Name']) + ' -->\n\n')
                f.write('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#' + str(line['Attribute_Name']) + '">\n')
                f.write('<rdf:type rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#Attribute"/>')
                f.write('<TMF_v1:hasOrigin>' + str(line['Origin']) + '</TMF_v1:hasOrigin>\n')
                f.write('<TMF_v1:hasStereotype>' + str(line['Stereotype']) + '</TMF_v1:hasStereotype>')
                #f.write('<rdf:label>' + str(line['Attribute_Name']) + '</rdf:label>\n')
                f.write('<rdf:label>' + str(line['Documentation'].replace('\n', ' ')) + '</rdf:label>\n</owl:NamedIndividual>\n\n')
                vocabulary.append(str(line['Attribute_Name']))
        f.close()
    return 1

def create_SID_nodes():
    ontology = []
    f = open("SID_nodes.rdf", "wt", encoding='utf-8')
    with open('src/SID_ABE.csv', encoding='utf-8') as input_swe:
        reader = csv.DictReader(input_swe, delimiter=';')
        j = 1 #Domain counter
        k = 1 #ABE counter
        l = 1 #BE counter
        m = 1 #Attr counter
        for line in reader:
            if line['ABE_Name'] != '':
                domain_name = line['ABE_Name'].split('Business Entity.')
                if len(domain_name) > 1:
                        ontology.append(SID_ontology_entry(domain_name[1], j,'',-1,'',-1,'',-1, line['Documentation']))
                        j = j + 1
                        continue
                abe_name = line['ABE_Name']
                ontology.append(SID_ontology_entry('', -1, abe_name, k, '', -1, '', -1, line['Documentation']))
                k = k + 1
                continue
            elif line['BE_Name'] != '':
                be_name = line['BE_Name']
                ontology.append(SID_ontology_entry('', -1, '', -1, be_name, l, '', -1, line['Documentation']))
                l = l + 1
                continue
            elif line['Attribute_Name'] != '':
                attr_name = line['Attribute_Name']
                ontology.append(SID_ontology_entry('', -1, '', -1, '', -1, attr_name, m, ''))
                m = m + 1
                continue

        i = 0
        N = len(ontology)
        while i < N:
            if ontology[i].domain_name != '':
                f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#Business_Entity.' + str(ontology[i].domain_name) + ' -->\n\n')
                f.write('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#Business_Entity.' + str(ontology[i].domain_name)+ '">\n')
                f.write('<rdf:type rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#TMFDomain"/>\n')
                #f.write('<rdf:label>Business Entity.' + str(ontology[i].domain_name) + '</rdf:label>\n')
                f.write('<rdf:label>Business Entity.' + str(ontology[i].domain_name) +' ' + str(ontology[i].doc) + '</rdf:label>\n</owl:NamedIndividual>\n\n')
            if (ontology[i].abe_name != '') and (ontology[i+1].abe_name != ''):
                i = i + 1
                continue
            if (ontology[i].abe_name != '') and (ontology[i + 1].abe_name == ''):
                f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#' + str(ontology[i].abe_name) + ' -->\n\n')
                f.write('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#' + str(ontology[i].abe_name) + '">\n')
                f.write('<rdf:type rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#ABE"/>\n')
                add_counter = 1
                while True:
                    if (i + add_counter >= N):
                        break
                    if (ontology[i + add_counter].abe_name != ''):
                        break
                    if ontology[i + add_counter].be_name != '':
                        f.write('<TMF_v1:hasBE rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#' + str(ontology[i + add_counter].be_name) + '"/>\n')
                    add_counter = add_counter + 1

                #f.write('<rdf:label>' + str(ontology[i].abe_name) + '</rdf:label>\n')
                f.write('<rdf:label>'  + str(ontology[i].abe_name) + ' ' + str(ontology[i].doc) + '</rdf:label>\n</owl:NamedIndividual>\n\n')
            if (ontology[i].be_name != ''):
                f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#' + str(ontology[i].be_name) + ' -->\n\n')
                f.write('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#' + str(ontology[i].be_name) + '">\n')
                f.write('<rdf:type rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#BE"/>\n')
                add_counter = 1
                while True:
                    if (i + add_counter >= N):
                        break
                    if (ontology[i + add_counter].be_name != ''):
                        break
                    if ontology[i + add_counter].attr_name != '':
                        f.write('<TMF_v1:hasAttribute rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#' + str(ontology[i + add_counter].attr_name) + '"/>\n')
                    add_counter = add_counter + 1
                #f.write('<rdf:label>' + str(ontology[i].be_name) + '</rdf:label>\n')
                f.write('<rdf:label>' + str(ontology[i].be_name) + ' ' + str(ontology[i].doc) + '</rdf:label>\n</owl:NamedIndividual>\n\n')
            i = i + 1

        for line in ontology:
            print('ontology=',line.domain_name, line.domain_id)


def create_VG_nodes():
    f = open("VG_nodes.rdf", "wt", encoding='utf-8')
    with open('src/VG.csv', encoding='utf-8') as input_swe:
        reader = csv.DictReader(input_swe, delimiter=';')
        for line in reader:
            print(line)
            f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#VG.' + str(line['vg']) + ' -->\n\n')
            f.write('<owl:NamedIndividual rdf:about = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#VG.' + str(line['vg']) + '">\n')
            f.write('<rdf:type rdf:resource = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#VerticalGroup"/>\n')
            #f.write('<rdf:label>' + str(line['vg']) + '</rdf:label>\n')
            f.write('<rdf:label>' + str(line['vg']) + '</rdf:label>\n</owl:NamedIndividual>\n\n')


        f.close()
    return 1

def create_eTOM_nodes():
    vocabulary = []
    f = open("eTOM_nodes.rdf", "wt", encoding='utf-8')
    with open('src/eTOM.csv', encoding='utf-8') as input_swe:
        reader = csv.DictReader(input_swe, delimiter=';')
        for line in reader:
            print(line)
            f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#' + str(line['Process']) + ' -->\n\n')
            f.write('<owl:NamedIndividual rdf:about = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#' + str(line['Process']) + '">\n')
            f.write('<rdf:type rdf:resource = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#Process"/>\n')
            f.write('<TMF_v1:hasDomain rdf:resource = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#Business_Entity.' + str(line['Domain']) + '"/>\n')
            f.write('<TMF_v1:hasVerticalGroup rdf:resource = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#VG.' + str(line['Vertical_Group']) + '"/>\n')
            f.write('<TMF_v1:BriefDescription>' + str(line['brief_description']) + '</TMF_v1:BriefDescription>\n')
            f.write('<TMF_v1:MaturityLevel rdf:datatype = "http://www.w3.org/2001/XMLSchema#integer">' + str(line['M_Level']) + '</TMF_v1:MaturityLevel>\n')
            f.write('<TMF_v1:OriginalProcessIdentifier>' + str(line['Original_id']) + '</TMF_v1:OriginalProcessIdentifier>\n')
            f.write('<TMF_v1:ProcessIdentifier>' + str(line['Process_id']) + '</TMF_v1:ProcessIdentifier>\n')
            f.write('<TMF_v1:ProcessLevel rdf:datatype = "http://www.w3.org/2001/XMLSchema#integer">' + str(line['Level']) + '</TMF_v1:ProcessLevel>\n')
            #f.write('<rdf:label>' + str(line['Process']) + '</rdf:label>\n')
            f.write('<rdf:label>' + str(line['Process']) + ' ' + str(line['extended_Description']) + '</rdf:label>\n</owl:NamedIndividual>\n\n')

        f.close()
    return 1

def create_AF_nodes():
    f = open("AF_nodes.rdf", "wt", encoding='utf-8')
    with open('src/TAM-AF.csv', encoding='utf-8') as input_swe:
        reader = csv.DictReader(input_swe, delimiter=';')
        for line in reader:
            print(line)
            f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#AF.' + str(line['AF']) + ' -->\n\n')
            f.write('<owl:NamedIndividual rdf:about = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#AF.' + str(line['AF']) + '">\n')
            f.write('<rdf:type rdf:resource = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#AF"/>\n')
            f.write('<TMF_v1:AFLevel rdf:datatype = "http://www.w3.org/2001/XMLSchema#decimal">' + str(line['Hierarchy']) + '</TMF_v1:AFLevel>\n')
            f.write('<TMF_v1:hasID rdf:datatype = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">' + str(line['ID']) + '</TMF_v1:hasID>\n')
            f.write('<TMF_v1:hasUID rdf:datatype = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">' + str(line['UID']) + '</TMF_v1:hasUID>\n')
            #f.write('<rdf:label>' + str(line['AF']) + '</rdf:label>\n')
            f.write('<rdf:label rdf:datatype = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">' + str(line['AF']) + ' ' + str(line['Description']) + '</rdf:label>\n</owl:NamedIndividual>\n\n')
        f.close()
    return 1

def create_TAM_nodes():
    f = open("TAM_nodes.rdf", "wt", encoding='utf-8')
    with open('src/TAM-Functions.csv', encoding='utf-8') as input_swe:
        reader = csv.DictReader(input_swe, delimiter=';')
        for line in reader:
            print(line)
            f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#F.' + str(line['Function_Name']) + ' -->\n\n')
            f.write('<owl:NamedIndividual rdf:about = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#F.' + str(line['Function_Name']) + '">\n')
            f.write('<rdf:type rdf:resource = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#Function"/>\n')
            f.write('<TMF_v1:AF_Lev.1 rdf:resource = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#AF.' + str(line['AF_Lev_1']) + '"/>\n')
            f.write('<TMF_v1:AF_Lev.2 rdf:resource = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#AF.' + str(line['AF_Lev_2']) + '"/>\n')
            f.write('<TMF_v1:hasDomain rdf:resource = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#Business_Entity.' + str(line['Domain']) + '"/>\n')
            f.write('<TMF_v1:hasVerticalGroup rdf:resource = "http://www.semanticweb.org/igork/ontologies/2024/1/TMF_v1#VG.' + str(line['Vertical']) + '"/>\n')
            f.write('<TMF_v1:hasID rdf:datatype = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">' + str(line['Function_ID']) + '</TMF_v1:hasID>\n')
            f.write('<TMF_v1:hasUID rdf:datatype = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">' + str(line['UID']) + '</TMF_v1:hasUID>\n')
            #f.write('<rdf:label rdf:datatype = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">' + str(line['Function_Name']) + '</rdf:label>\n')
            f.write('<rdf:label rdf:datatype = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">' + str(line['Function_Name']) + ' ' + str(line['Description']) + '</rdf:label>\n</owl:NamedIndividual>\n\n')
        f.close()
    return 1

def clear_content(content):
    content = content.replace('\xa0', ' ')
    content = content.replace('\x99', '')
    content = content.replace('\xB7', '-')
    content = content.replace('\x95', '-')
    content = content.replace('\x96', '')
    content = content.replace('\x92', '')
    content = content.replace('\xBB', '')
    content = content.replace('\xAB', '')
    content = content.replace('&', 'and')
    return content

if __name__ == "__main__":
    create_SID_attrs()
    create_SID_nodes()
    create_VG_nodes()
    create_eTOM_nodes()
    create_AF_nodes()
    create_TAM_nodes()

    f = open("TMF_Ontology_v4.rdf", "wt")
    f_template = open('src/TMF_Ontology_template_v1.rdf', encoding='utf-8')
    template_part = f_template.read().split('<!-- List of TMF entries -->')
    f.write(template_part[0])
    content = open('SID_attrs.rdf', encoding='utf-8').read()
    content = clear_content(content)
    f.write(content)
    content = open('SID_nodes.rdf', encoding='utf-8').read()
    content = clear_content(content)
    f.write(content)
    content = open('VG_nodes.rdf', encoding='utf-8').read()
    content = clear_content(content)
    f.write(content)
    content = open('eTOM_nodes.rdf', encoding='utf-8').read()
    content = clear_content(content)
    f.write(content)
    content = open('AF_nodes.rdf', encoding='utf-8').read()
    content = clear_content(content)
    f.write(content)
    content = open('TAM_nodes.rdf', encoding='utf-8').read()
    content = clear_content(content)
    f.write(content)
    f.write(template_part[1])
    f.close()



