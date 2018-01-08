class Node:
    def __init__(self, name, concept, concept_answer, is_root=False, children=None):
        self._is_root = is_root
        self._parent = None
        self._name = name
        self._children = children if children else []
        self._concept = concept
        self._concept_answer = concept_answer

    def set_parent(self, parent):
        self._parent = parent
        parent.add_child(self)

    def add_child(self, child):
        self._children.append(child)

    def get_children(self):
        return self._children

    def get_concept(self):
        return self._concept

    def get_name(self):
        return self._name

    def add_concept(self, concept):
        self._concept.append(concept)

    def is_root(self):
        return self._is_root

    def get_concept_answer(self):
        return self._concept_answer