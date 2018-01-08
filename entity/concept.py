class Concept:
    def __init__(self, concept_name, threshold=0.75, variations=None):
        self._concept_name = concept_name
        self._variations = variations if variations else []
        self._threshold = threshold

    def add_variation(self, *variation):
        for var in variation:
            self._variations.append(var)

    def get_variations(self):
        return self._variations
