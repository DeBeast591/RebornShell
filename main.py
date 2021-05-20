# RBSH - RebornShell
# Made by Payton C
# Enjoy!


###################
# Todo Area
# TODO: clean up this file
# TODO: make shell async or make shell fast
###################


# imports
from prompt_toolkit.completion import NestedCompleter
import yaml
# local imports
import utils
from utils import prompt
from utils import statusbar
# stdlib
import asyncio


# config
with open("config.yml") as f:
  config = yaml.load(f, Loader=yaml.FullLoader)
# print(config)

# autocomplete tree
autocomplete_tree = {}
for k, v in config["autocomplete"].items():
  autocomplete_tree[k] = v
autocomplete_tree = utils.replace_deep_with_none(autocomplete_tree, "None")
completer = NestedCompleter.from_nested_dict(autocomplete_tree)

# custom prompt
def custom_prompt():
  return prompt.gen_from_dict(config["prompt"])
# custom statubar
def custom_statusbar():
  return statusbar.gen_from_dict(config["statusbar"])

# start session
session = utils.Shell(history_file=config["general"]["history_file"])
session.completer = completer
session.show_status_bar = config["general"]["show_status_bar"]
session.history_completions = config["general"]["history_completions"]
session.get_prompt = custom_prompt
session.get_statusbar = custom_statusbar
session.threaded_completion = config["general"]["threaded_completion"]
session.aliases = config["aliases"]
asyncio.run(session.start())

