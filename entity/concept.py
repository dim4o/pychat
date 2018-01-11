class Concept(object):
    """
    Expresses the basic idea in a phrase by combining a list of similar phrases.
    """
    def __init__(self, concept_name, variations=None, threshold=None):
        self._concept_name = concept_name
        self._variations = variations if variations else []
        self._threshold = threshold

    def add_variation(self, *variation):
        for var in variation:
            self._variations.append(var)

    def get_variations(self):
        return self._variations

    def get_threshold(self):
        return self._threshold

    def get_name(self):
        return self._concept_name
