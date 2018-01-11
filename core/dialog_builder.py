import json

# this is a temp 'dirty' way to test the dialog inside the base package
try:
    from entity.concept import Concept
    from entity.node import Node
except ImportError:
    from ..entity.concept import Concept
    from ..entity.node import Node


class DialogBuilder(object):
    """
    Responsible for reading and parsing the dialog data.
    """

    def __init__(self, dialog_location):
        self._dialog_location = dialog_location

    @staticmethod
    def _read_json(json_location):
        """ Converts JSON file to python object
        :param json_location: the data files location
        :return: python object
        """
        return json.load(open(json_location))

    def _read_concepts(self):
        """
        Read concept and converts to python dict (concept_name, concept_object).

        :return: python dictionary that holds concept object value by concept name
        """
        concepts_dict = {}
        raw_concepts = self._read_json(self._dialog_location + '/concepts.json')
        for raw_con in raw_concepts:
            concept_name = raw_con['concept_name']
            variations = raw_con['variations']
            threshold = raw_con.get('threshold', "empty")
            curr_concept = Concept(concept_name, variations, threshold)
            concepts_dict[concept_name] = curr_concept

        return concepts_dict

    def _read_nodes(self, concepts_dict):
        """
        Reads and parse the node objects from JSON file.

        :param concepts_dict:
        :return: python dictionary that holds the node object value by node name
        """
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
                concept_answers.append(concepts_dict.get(ca, None) or Concept(ca))

            curr_node = Node(name, concepts, concept_answers, is_root)
            nodes_dict[name] = curr_node

        return nodes_dict

    def _read_nodes_map(self, nodes_dict):
        """
        Reads and parse the node map from JSON file and add the children ot the existing nodes.

        :param nodes_dict:
        :return: a list of nodes with their children
        """
        raw_map = self._read_json(self._dialog_location + '/nodes_map.json')
        for pair in raw_map:
            name = pair['name']
            children = pair['children']
            parent_node = nodes_dict[name]
            for child in children:
                parent_node.add_child(nodes_dict[child])

        return nodes_dict

    def build_dialog(self):
        """
        Builds a dialog from the node data.

        :return: a list of nodes that represents the dialog
        """
        concept_dict = self._read_concepts()
        nodes_dict = self._read_nodes(concept_dict)

        return self._read_nodes_map(nodes_dict)
