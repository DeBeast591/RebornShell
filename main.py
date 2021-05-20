# RBSH - RebornShell
# Made by Payton C
# Enjoy!


###################
# Todo Area
# TODO: clean up this file
# TODO: make shell async
###################


# imports
from prompt_toolkit.completion import NestedCompleter
import yaml
# local imports
import utils


# config
with open("config.yml") as f:
  config = yaml.load(f, Loader=yaml.FullLoader)

# autocomplete tree
autocomplete_tree = {}
for k, v in config["autocomplete"].items():
  autocomplete_tree[k] = v
autocomplete_tree = utils.replace_deep_with_none(autocomplete_tree, "None")
completer = NestedCompleter.from_nested_dict(autocomplete_tree)

# start session
session = utils.Shell(history_file=config["general"]["history_file"])
session.completer = completer
session.show_status_bar = config["general"]["show_status_bar"]
session.history_completions = config["general"]["history_completions"]
session.start()

