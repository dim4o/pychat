import random


class DialogEngine(object):
    THRESHOLD = 0.5

    def __init__(self, node_list):
        self._node_list = node_list
        self._context = None
        self._root_list = list(filter(lambda x: x.is_root() is True, node_list))

    def process(self, input_chat):
        if self._context is None or len(self._context.get_children()) == 0:
            self._context = None
            best_match = self._find_best_match(input_chat, self._root_list)
        else:
            best_match = self._find_best_match(input_chat, self._context.get_children())
            if best_match is None:
                best_match = self._find_best_match(input_chat, self._root_list)

        if best_match is None:
            return "не те разбирам"

        self._context = best_match

        best_match_node_concepts = best_match.get_concept_answer()
        answer = ""
        for concept in best_match_node_concepts:
            answer += random.choice(concept.get_variations()) + ". "

        return answer

    def _find_best_match(self, input_chat, node_list):
        best_match_node = None
        best_distance = 1000

        for curr_node in node_list:
            node_concepts = curr_node.get_concept()
            variations = []

            for concept in node_concepts:
                variations.extend(concept.get_variations())

            for variation in variations:
                dist = 1 - self._normalize_dist(input_chat.lower(), variation.lower())
                if dist < best_distance and 1 - dist > self.THRESHOLD:
                    best_distance = dist
                    best_match_node = curr_node

        return best_match_node

    @staticmethod
    def _find_levenshtein_dist(first_str, second_str):
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

    def _normalize_dist(self, first_str, second_str):
        longer_str = max(len(first_str), len(second_str))
        return (longer_str - self._find_levenshtein_dist(first_str, second_str)) / float(longer_str)
