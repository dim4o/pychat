# coding=utf-8
import random


class DialogEngine(object):
    """
    Contains the main functionality of the module. Processed the user input and finds the best response from the
    dialog tree (a list of the dialog nodes and their children).
    """

    def __init__(self, node_dict, threshold=0.5):
        """
        :param node_dict: a dict of nodes their names that represents the dialog tree structure
        :param threshold: the minimum confidence required to select a phrase as a matching candidate
        """
        self._threshold = threshold
        self._context = None
        self._root_list = list(filter(lambda x: x.is_root() is True, node_dict.values()))

    def process(self, input_chat):
        """
        Processes the user input and returns the most relevant answer.

        :param input_chat: the user input
        :return: the most relevant chat response as list of strings
        """
        if self._context is None or len(self._context.get_children()) == 0:
            self._context = None
            best_match = self._find_best_match(input_chat, self._root_list)
        else:
            best_match = self._find_best_match(input_chat, self._context.get_children())
            if best_match is None:
                best_match = self._find_best_match(input_chat, self._root_list)

        if best_match is None:
            return [u'не те разбирам']

        self._context = best_match

        best_match_node_concepts = best_match.get_concept_answer()
        response = []
        for concept in best_match_node_concepts:
            concept_variations = concept.get_variations()
            response_part = random.choice(concept_variations) if concept_variations else concept.get_name()
            response.append(response_part)

        return response

    def get_context(self):
        return self._context

    def _find_best_match(self, input_chat, node_list):
        """
        Finds the most suitable Node that matches the user input.

        :param input_chat: the user input
        :param node_list: the list to look for
        :return: the most suitable Node
        """
        best_match_node = None
        best_distance = 1000

        for curr_node in node_list:
            node_concepts = curr_node.get_concept()

            for concept in node_concepts:
                variations = concept.get_variations()
                local_threshold = concept.get_threshold() or self._threshold

                for variation in variations:
                    dist = 1 - self._get_min_distance(input_chat.lower(), variation.lower())
                    if dist < best_distance and 1 - dist > local_threshold:
                        best_distance = dist
                        best_match_node = curr_node

        return best_match_node

    @staticmethod
    def _find_levenshtein_dist(first_str, second_str):
        """
        Finds the minimum edit distance between two strings through the Levenshtein distance algorithm.

        :param first_str: the first string to compare
        :param second_str: the second string to compare
        :return: the Levenshtein distance between two strings
        """
        rows = len(first_str) + 1
        cols = len(second_str) + 1
        matrix = [[0] * cols for _ in range(rows)]

        for row in range(1, rows):
            matrix[row][0] = row
            for col in range(1, cols):
                matrix[0][col] = col
                substitution_cost = 0 if first_str[row - 1] == second_str[col - 1] else 1
                matrix[row][col] = min(matrix[row - 1][col] + 1, matrix[row][col - 1] + 1,
                                       matrix[row - 1][col - 1] + substitution_cost)

        return matrix[rows - 1][cols - 1]

    def _get_min_distance(self, first_str, second_str):
        """
        Finds and normalizes the minimum edit distance between two strings.

        :param first_str: the first string to compare
        :param second_str: the second string to compare
        :return: normalized minimum edit distance between two strings
        """
        longer_str = max(len(first_str), len(second_str))
        return (longer_str - self._find_levenshtein_dist(first_str, second_str)) / float(longer_str)
