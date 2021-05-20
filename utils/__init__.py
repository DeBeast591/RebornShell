# imports
import prompt_toolkit
from pygments.lexers.html import HtmlLexer
# stdlib
import subprocess
import os
# local imports
from utils import binds



# replace all in a dict, including nested ones.
# https://stackoverflow.com/questions/65542170/how-to-replace-all-occurence-of-string-in-a-nested-dict
# this is a modified version of the above made by Payton
def replace_deep_with_none(data: dict, a: str) -> any:
    if isinstance(data, str):
        return None
    elif isinstance(data, dict):
        return {k: replace_deep_with_none(v, a) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_deep_with_none(v, a) for v in data]
    else:
        return data

# gets the user's pwd
def get_pwd() -> str:
  pwd = subprocess.check_output("pwd")
  pwd = pwd.decode("UTF-8").strip("\n")
  pwd = pwd.replace(os.path.expanduser("~"), "~")
  return pwd


# shell class
# TODO: clean up!
class Shell:
  def __init__(self, history_file: str="rbsh_history") -> None:
    # config
    self.completer           = {}
    self.bindings            = binds.default_bindings
    self.show_status_bar     = True
    self.history_completions = True
    self.history_file        = history_file

    self.session = prompt_toolkit.PromptSession(
      history = prompt_toolkit.history.FileHistory (history_file) if self.history_file != "None" else None
    )
    return
  
  def start(self) -> None:
    while True:
      action = self.prompt_user()
      if action in ["quit", "exit"]:
        break
      elif action.startswith("cd"):
        if action == "cd":
          os.chdir(os.path.expanduser("~"))
          continue
        os.chdir(action.replace("cd ", "", 1))
      elif action.startswith("rbshctl"):
        self.rbshctl(action)
      else:
        self.execute_cmd(action)
    return
  
  def get_statusbar(self) -> list:
    text = "RebornShell"
    return [
      ("class:toolbar", text)
    ]
  
  def prompt_user(self) -> None:
    action = self.session.prompt(
      self.get_prompt,
      lexer          = prompt_toolkit.lexers.PygmentsLexer(HtmlLexer),
      completer      = self.completer,
      auto_suggest   = prompt_toolkit.auto_suggest.AutoSuggestFromHistory() if self.history_completions else None,
      key_bindings   = self.bindings,
      bottom_toolbar = self.get_statusbar if self.show_status_bar else None,
      mouse_support  = True,
      is_password    = False
    )
    return action
  
  def prompt_exit(self) -> None:
    prompt_toolkit.shortcuts.message_dialog(
      title='Exit?',
      text='Do you want to exit?\nPress ENTER to quit.').run()
    return quit()
  
  def execute_cmd(self, cmd: str) -> None:
    try:
      output = subprocess.check_output(cmd.split(), shell=False)
      print(output.decode("UTF-8").strip("\n"))
    except Exception:
      print("RBSH: cmd not found: " + cmd)
    return
  
  def rbshctl(self, cmd: str) -> None:
    if cmd.startswith("rbshctl get"):
      cmd = cmd.replace("rbshctl get ", "", 1)
      if cmd == "history_file":
        print(self.history_file)
      elif cmd == "show_status_bar":
        print(self.show_status_bar)
      elif cmd == "history_completions":
        print(self.history_completions)
      elif cmd == "completion_tree":
        print(self.completions)
      else:
        print("Variable not found.")
    return
  
  def get_prompt(self) -> str:
    return (
      get_pwd() +
      " $ "
    )

