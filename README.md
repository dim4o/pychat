# Python chat bot
This is a simple language independent chat bot

## Usage

### Dialog data
The dialog data can be represented of three files in a specific directory: `concepts.json`, `nodes.json`, `nodes_map.json`

### Concept
This is the main unit of the dialog. The concept is independent part of the speech and can be used from both - bot or human.

```
[
  ...
  {
    "concept_name": "hello_concept",
    "variations": [
    "hello",
    "hi"
    ]
  },
  ...
]
```

### Node
Represents the basic unit of interaction. Contains a pair or request and response.

```
{
  "name": "hello_hello_how_are_you_node",
  "is_root": true,
  "concepts": [
    "hello_concept"
  ],
  "concept_answers": [
    "hello_concept",
    "how_are_you"
  ]
}
```

### Node map
Maps the relations between the nodes. Each item contains a list of it's children nodes represented by name.

```
{
  "name": "hello_hello_how_are_you_node",
  "children": [
    "fine_im_glad_you_are_fine_products_prop_node",
    "im_sorry_for_you_node"
  ]
}
```

### Initialization
``` Python
node_dictionary = DialogBuilder("path_to_dialog_data_directory")
dialog_engine = DialogEngine(node_dictionary, threshold=0.35)
sentences = dialog_engine.process(user_input)
```
