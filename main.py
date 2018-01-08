from core.dialog_builder import DialogBuilder
from core.dialog_engine import DialogEngine

builder = DialogBuilder('./dialog_data')
node_list = builder.build_node_map()
de = DialogEngine(node_list)

while True:
    line = input()
    print("    {}".format(de.process(line)))
