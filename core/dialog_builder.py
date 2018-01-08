import json
from entity.concept import Concept
from entity.node import Node


class DialogBuilder:
    """ Responsible for reading and parsing the dialog data """

    def __init__(self, dialog_location):
        self._dialog_location = dialog_location

    @staticmethod
    def _read_json(json_location):
        """ Converts JSON file to python object """
        return json.load(open(json_location))

    def _read_concepts(self):
        """ Read concept and converts to python dict (concept_name, concept_object)"""
        concepts_dict = {}
        raw_concepts = self._read_json(self._dialog_location + '/concepts.json')
        for raw_con in raw_concepts:
            concept_name = raw_con['concept_name']
            variations = raw_con['variations']
            threshold = raw_con['threshold']
            curr_concept = Concept(concept_name, threshold, variations)
            concepts_dict[concept_name] = curr_concept

        return concepts_dict

    def _read_nodes(self, concepts_dict):
        nodes_dict = {}
        raw_nodes = self._read_json(self._dialog_location + '/nodes.json')
        for raw_n in raw_nodes:
            name = raw_n['name']
            is_root = raw_n['is_root']
            concept_names = raw_n['concepts']
            concept_answers_names = raw_n['concept_answers']
            concepts = []
            concept_answers = []
            for c in concept_names:
                concepts.append(concepts_dict[c])
            for ca in concept_answers_names:
                concept_answers.append(concepts_dict[ca])

            curr_node = Node(name, concepts, concept_answers, is_root)
            nodes_dict[name] = curr_node

        return nodes_dict

    def _read_nodes_map(self, nodes_dict):
        raw_map = self._read_json(self._dialog_location + '/nodes_map.json')
        node_list = []
        for pair in raw_map:
            name = pair['name']
            children = pair['children']
            parent_node = nodes_dict[name]
            for child in children:
                parent_node.add_child(nodes_dict[child])
            node_list.append(parent_node)

        return node_list

    def build_node_map(self):
        concept_dict = self._read_concepts()
        nodes_dict = self._read_nodes(concept_dict)

        return self._read_nodes_map(nodes_dict)
