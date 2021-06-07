# RBSH - RebornShell
# Made by Payton C
# Enjoy!


# RBSH Version
# it's at the top of this file so i dont forget to update it
RBSH_VERSION = "RBSH Version 0.2.2"


# imports
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.key_binding import KeyBindings
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


# autocomplete tree
autocomplete_tree = {}
for k, v in config["autocomplete"].items():
  autocomplete_tree[k] = v
# replaces all `"None"`s with `None`s
autocomplete_tree = utils.replace_deep_with_none(autocomplete_tree, "None")
# makes a completer
completer = NestedCompleter.from_nested_dict(autocomplete_tree)


# keybinds
key_binds = KeyBindings()

@key_binds.add("c-c")
def _(event):
  pass


# start session
session = utils.Shell(
  history_file = config["general"]["history_file"],
  completer = completer,
  bindings = key_binds,
  show_status_bar = config["general"]["show_status_bar"],
  history_completions = config["general"]["history_completions"],
  threaded_completion = config["general"]["threaded_completion"],
  aliases = config["aliases"],
  version = RBSH_VERSION
)


# generates a prompt and statusbar from the config
# custom prompt
def custom_prompt():
  return prompt.gen_from_dict(config["prompt"], shell=session)
# custom statusbar
def custom_statusbar():
  return statusbar.gen_from_dict(config["statusbar"], shell=session)


# session settings
session.get_prompt = custom_prompt
session.get_statusbar = custom_statusbar

# start the session
asyncio.run(session.start())

