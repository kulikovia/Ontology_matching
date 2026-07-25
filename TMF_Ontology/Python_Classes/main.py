import xml.etree.ElementTree as xml
import random
import csv
from random import randrange
from datetime import datetime
from datetime import timedelta

class SID_ontology_entry:
    def __init__(self, domain_name, domain_id, abe_name, abe_id, be_name, be_id, attr_name, attr_id, doc, isABE_host, parent):
        self.domain_name = domain_name
        self.domain_id = domain_id
        self.abe_name = abe_name
        self.abe_id = abe_id
        self.be_name = be_name
        self.be_id = be_id
        self.attr_name = attr_name
        self.attr_id = attr_id
        self.doc = doc
        self.isABE_host = isABE_host
        self.parent = parent

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
                f.write('<!--http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#hasAttr_' + str(line['Attribute_Name']) + ' -->\n\n')
                f.write('<owl:DatatypeProperty rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#hasAttr_' + str(line['Attribute_Name']) + '">\n')
                f.write('<InformationModel_v1:hasOrigin>' + str(line['Origin']) + '</InformationModel_v1:hasOrigin>\n')
                f.write('<InformationModel_v1:hasStereotype>' + str(line['Stereotype']) + '</InformationModel_v1:hasStereotype>\n')
                f.write('<rdf:label>' + str(line['Attribute_Name']) + '</rdf:label>\n')
                f.write('<rdfs:comment>' + str(line['Documentation'].replace('\n', ' ')) + '</rdfs:comment>\n</owl:DatatypeProperty>\n\n')

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
        domain_name = ''
        for line in reader:
            if line['ABE_Name'] != '':
                domain_name = line['ABE_Name'].split('Business Entity.')
                if len(domain_name) > 1 and domain_name[1] != '':
                        ontology.append(SID_ontology_entry(domain_name[1], j,'',-1,'',-1,'',-1, line['Documentation'], False, ''))
                        domain_name_tmp = domain_name[1]
                        j = j + 1
                        continue
                ABE_host = line['ABE_Name'].split('ABE.')
                if len(ABE_host) > 1:
                        ontology.append(SID_ontology_entry(domain_name_tmp, -1,ABE_host[1], k,'',-1,'',-1, line['Documentation'], False, host_ID_name))
                        k = k + 1
                        continue
                abe_name = line['ABE_Name'].split('.')
                if abe_name[len(abe_name)-1].find('ABE') != -1:
                    ontology.append(SID_ontology_entry(domain_name_tmp, -1, abe_name[len(abe_name)-1], k, '', -1, '', -1, line['Documentation'], True, ''))
                    host_ID_name = abe_name[len(abe_name)-1]
                    k = k + 1
                    continue
            elif line['BE_Name'] != '':
                be_name = line['BE_Name']
                ontology.append(SID_ontology_entry('', -1, '', -1, be_name, l, '', -1, line['Documentation'], False, ''))
                l = l + 1
                continue
            elif line['Attribute_Name'] != '':
                attr_name = line['Attribute_Name']
                ontology.append(SID_ontology_entry('', -1, '', -1, '', -1, attr_name, m, '', False, ''))
                m = m + 1
                continue

        i = 0
        N = len(ontology)
        tmp_abe_name = ''
        tmp_be_name = ''
        while i < N:
            if ontology[i].domain_name != '' and ontology[i].domain_id != -1:
                f.write('<!--http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#Business_Entity.' + str(ontology[i].domain_name) + ' -->\n\n')
                f.write('<owl:Class rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#Business_Entity.' + str(ontology[i].domain_name)+ '">\n')
                f.write('<rdfs:subClassOf rdf:resource = "http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#TMFDomain"/>\n')
                f.write('<rdfs:comment>' + str(ontology[i].doc) + '</rdfs:comment>\n')
                f.write('<rdfs:label>Business Entity.' + str(ontology[i].domain_name) + '</rdfs:label>\n</owl:Class>\n\n')

            if (ontology[i].abe_name != ''):
                tmp_abe_name = str(ontology[i].abe_name)
                f.write('<!--http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#' + str(ontology[i].abe_name) + ' -->\n\n')
                f.write('<owl:Class rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#' + str(ontology[i].abe_name) + '">\n')
                if ontology[i].parent != '':
                    f.write('<rdfs:subClassOf rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#' + str(ontology[i].parent) + '"/>\n')
                else:
                    f.write('<rdfs:subClassOf rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#ABE"/>\n')
                f.write('<rdfs:comment>'  + str(ontology[i].doc) + '</rdfs:comment>\n')
                f.write('<rdfs:label>' + str(ontology[i].abe_name) + '</rdfs:label>\n</owl:Class>\n\n')

                f.write('<!--http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#hasDomain_for_' + str(ontology[i].abe_name) + ' -->\n\n')
                f.write('<owl:ObjectProperty rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#hasDomain_for_' + str(ontology[i].abe_name) + '">\n')
                f.write('<rdfs:subPropertyOf rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#hasDomain"/>\n')
                f.write('<rdfs:domain rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#' + str(ontology[i].abe_name) + '"/>\n')
                f.write('<rdfs:range rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#Business_Entity.' + str(ontology[i].domain_name)+ '"/>\n</owl:ObjectProperty>\n\n')

                f.write('<!--http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1# hasBE_for_' + str(ontology[i].abe_name) + ' -->\n\n')
                f.write('<owl:ObjectProperty rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#hasBE_for_' + str(ontology[i].abe_name) + '">\n')
                f.write('<rdfs:subPropertyOf rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#hasBE"/>\n')
                f.write('<rdfs:domain rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#' + str(ontology[i].abe_name) + '"/>\n')

                add_counter = 1
                while True:
                    if (i + add_counter >= N):
                        break
                    if (ontology[i + add_counter].abe_name != ''):
                        break
                    if ontology[i + add_counter].be_name != '':
                        f.write('<rdfs:range rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#' + str(ontology[i + add_counter].be_name) + '"/>\n')
                    add_counter = add_counter + 1

                f.write('<rdfs:comment>hasBE_for_' + str(ontology[i].abe_name) + '</rdfs:comment>\n')
                f.write('<rdfs:label>hasBE_for_' + str(ontology[i].abe_name) + '</rdfs:label>\n</owl:ObjectProperty>\n\n')

            if (ontology[i].be_name != ''):
                tmp_be_name = str(ontology[i].be_name)
                f.write('<!--http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#' + str(ontology[i].be_name) + ' -->\n\n')
                f.write('<owl:Class rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#' + str(ontology[i].be_name) + '">\n')
                f.write('<rdfs:subClassOf rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#BE"/>\n')
                f.write('<rdfs:subClassOf rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#' + tmp_abe_name + '"/>\n')

                f.write('<rdf:label>' + str(ontology[i].be_name) + '</rdf:label>\n')
                f.write('<rdfs:comment>' + str(ontology[i].doc) + '</rdfs:comment>\n</owl:Class>\n\n')

                '''
                f.write('<!--http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#hasAttribute_for_' + str(ontology[i].be_name) + ' -->\n\n')
                f.write('<owl:ObjectProperty rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#hasAttribute_for_' + str(ontology[i].be_name) + '">\n')
                f.write('<rdfs:subPropertyOf rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#hasAttribute"/>\n')
                f.write('<rdfs:domain rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#' + str(ontology[i].be_name) + '"/>\n')
                '''

                add_counter = 1
                while True:
                    if (i + add_counter >= N):
                        break
                    if (ontology[i + add_counter].be_name != ''):
                        break
                    if ontology[i + add_counter].attr_name != '':
                        f.write('<!--http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#hasAttr_' + str(ontology[i + add_counter].attr_name) + ' -->\n\n')
                        f.write('<owl:DatatypeProperty rdf:about="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#hasAttr_' + str(ontology[i + add_counter].attr_name) + '">\n')
                        f.write('<rdfs:domain rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/InformationModel_v1#' + tmp_be_name + '"/>\n')
                        f.write('<rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>\n</owl:DatatypeProperty>\n\n')

                    add_counter = add_counter + 1
                #f.write('<rdf:label>hasAttribute_for_' + str(ontology[i].be_name) + '</rdf:label>\n')
                #f.write('<rdfs:comment>hasAttribute_for_' + str(ontology[i].be_name) + '</rdfs:comment>\n</owl:ObjectProperty>\n\n')
            i = i + 1

        for line in ontology:
            print('ontology=',line.domain_name, line.domain_id)


def create_VG_nodes():
    f = open("VG_nodes.rdf", "wt", encoding='utf-8')
    with open('src/VG.csv', encoding='utf-8') as input_swe:
        reader = csv.DictReader(input_swe, delimiter=';')
        for line in reader:
            print(line)
            f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/ProcessModel_v1#VG.' + str(line['vg']) + ' -->\n\n')
            f.write('<owl:Class rdf:about = "http://www.semanticweb.org/igork/ontologies/2024/1/ProcessModel_v1#VG.' + str(line['vg']) + '">\n')
            f.write('<rdfs:subClassOf rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/ProcessModel_v1#VerticalGroup"/>\n')
            f.write('<rdf:label>' + str(line['vg']) + '</rdf:label>\n')
            f.write('<rdfs:comment>' + str(line['vg']) + '</rdfs:comment>\n</owl:Class>\n\n')


        f.close()
    return 1

def create_eTOM_nodes():
    vocabulary = []
    f = open("eTOM_nodes.rdf", "wt", encoding='utf-8')
    with open('src/eTOM.csv', encoding='utf-8') as input_swe:
        reader = csv.DictReader(input_swe, delimiter=';')
        for line in reader:
            print(line)
            f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/ProcessModel_v1#' + str(line['Process']) + ' -->\n\n')
            f.write('<owl:Class rdf:about = "http://www.semanticweb.org/igork/ontologies/2024/1/ProcessModel_v1#' + str(line['Process']) + '">\n')
            f.write('<rdfs:subClassOf rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/ProcessModel_v1#Process"/>\n')
            f.write('<rdf:label>' + str(line['Process']) + '</rdf:label>\n')
            f.write('<rdfs:comment>' + str(line['extended_Description']) + '</rdfs:comment>\n</owl:Class>\n\n')

        f.close()
    return 1

def create_AF_nodes():
    f = open("AF_nodes.rdf", "wt", encoding='utf-8')
    with open('src/TAM-AF.csv', encoding='utf-8') as input_swe:
        reader = csv.DictReader(input_swe, delimiter=';')
        for line in reader:
            print(line)
            f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/v1#AF.' + str(line['AF']) + ' -->\n\n')
            f.write('<owl:Class rdf:about = "http://www.semanticweb.org/igork/ontologies/2024/1/FunctionModel_v1#AF.' + str(line['AF']) + '">\n')
            f.write('<rdfs:subClassOf rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/FunctionModel_v1#AF"/>\n')
            f.write('<rdf:label>' + str(line['AF']) + '</rdf:label>\n')
            f.write('<rdfs:comment rdf:datatype = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">' + str(line['Description']) + '</rdfs:comment>\n</owl:Class>\n\n')
        f.close()
    return 1

def create_TAM_nodes():
    f = open("TAM_nodes.rdf", "wt", encoding='utf-8')
    with open('src/TAM-Functions.csv', encoding='utf-8') as input_swe:
        reader = csv.DictReader(input_swe, delimiter=';')
        for line in reader:
            print(line)
            f.write('<!-- http://www.semanticweb.org/igork/ontologies/2024/1/FunctionModel_v1#F.' + str(line['Function_Name']) + ' -->\n\n')
            f.write('<owl:Class rdf:about = "http://www.semanticweb.org/igork/ontologies/2024/1/FunctionModel_v1#F.' + str(line['Function_Name']) + '">\n')
            f.write('<rdfs:subClassOf rdf:resource="http://www.semanticweb.org/igork/ontologies/2024/1/FunctionModel_v1#Function"/>\n')
            f.write('<rdf:label rdf:datatype = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">' + str(line['Function_Name']) + '</rdf:label>\n')
            f.write('<rdfs:comment rdf:datatype = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">' + str(line['Description']) + '</rdfs:comment>\n</owl:Class>\n\n')
        f.close()
    return 1

def clear_content(content):
    content = content.replace('\xa0', ' ')
    content = content.replace('\x99', '')
    content = content.replace('\xB7', '-')
    content = content.replace('\x95', '-')
    content = content.replace('\x97', ' ')
    content = content.replace('\x96', '')
    content = content.replace('\x92', '')
    content = content.replace('\xBB', '')
    content = content.replace('\xAB', '')
    content = content.replace('&', 'and')
    #content = content.replace('<', '=')
    #content = content.replace('>', '=')
    return content

if __name__ == "__main__":
    create_SID_attrs()
    create_SID_nodes()
    create_VG_nodes()
    create_eTOM_nodes()
    create_AF_nodes()
    create_TAM_nodes()

    f = open("InformationModel_Ontology_v6.rdf", "wt", encoding='utf-8')
    f_template = open('src/InformationModel_Ontology_template_v6.rdf', encoding='utf-8')
    template_part = f_template.read().split('<!-- List of TMF entries -->')
    f.write(template_part[0])
    content = open('SID_attrs.rdf', encoding='utf-8').read()
    content = clear_content(content)
    f.write(content)
    content = open('SID_nodes.rdf', encoding='utf-8').read()
    content = clear_content(content)
    f.write(content)
    f.write(template_part[1])
    f.close()

    f = open("ProcessModel_Ontology_v6.rdf", "wt", encoding='utf-8')
    f_template = open('src/ProcessModel_Ontology_template_v6.rdf', encoding='utf-8')
    template_part = f_template.read().split('<!-- List of TMF entries -->')
    f.write(template_part[0])
    content = open('VG_nodes.rdf', encoding='utf-8').read()
    content = clear_content(content)
    f.write(content)
    content = open('eTOM_nodes.rdf', encoding='utf-8').read()
    content = clear_content(content)
    f.write(content)
    f.write(template_part[1])
    f.close()

    f = open("FunctionModel_Ontology_v6.rdf", "wt", encoding='utf-8')
    f_template = open('src/FunctionModel_Ontology_template_v6.rdf', encoding='utf-8')
    template_part = f_template.read().split('<!-- List of TMF entries -->')
    f.write(template_part[0])
    content = open('AF_nodes.rdf', encoding='utf-8').read()
    content = clear_content(content)
    f.write(content)
    content = open('TAM_nodes.rdf', encoding='utf-8').read()
    content = clear_content(content)
    f.write(content)
    f.write(template_part[1])
    f.close()




