# coding=utf-8
from core.dialog_builder import DialogBuilder
from core.dialog_engine import DialogEngine

builder = DialogBuilder('../../resources/dsk_bg_dialog')
node_list = builder.build_dialog()
de = DialogEngine(node_list, 0.35)

while True:
    line = raw_input()
    if line == "q":
        break
    robot_response = ". ".join(de.process(line.decode("utf-8")))
    print(u"    - {}".format(robot_response))
    context_name = de.get_context().get_name() if de.get_context() is not None else None
    print("    ['context' : '{}']".format(context_name))
