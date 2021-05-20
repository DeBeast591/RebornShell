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
# this is a modified version that I made, the original is above
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

# gets the user's pwd and makes it smaller
def get_pwd_small() -> str:
  pwd = get_pwd()
  pwd = pwd.split("/")[-1]
  if pwd[-1] != "/":
    pwd += "/"
  return pwd

# formats a dict to make it look good
def format_dict(dict_: dict) -> None:
  for k, v in dict_.items():
    print(str(k) + ": " + str(v))
  return
    


# shell class
# TODO: clean up!
class Shell:
  def __init__(self, history_file: str="rbsh_history") -> None:
    # config
    self.completer = {}
    self.bindings = binds.default_bindings
    self.show_status_bar = True
    self.history_completions = True
    self.history_file = history_file
    self.threaded_completion = False
    self.aliases = {}

    self.session = prompt_toolkit.PromptSession(
      history = prompt_toolkit.history.FileHistory (history_file) if self.history_file != "None" else None
    )

    return
  
  async def start(self) -> None:
    while True:
      with prompt_toolkit.patch_stdout.patch_stdout():
        action = await self.prompt_user()
      action = self.format_aliases(action)
      
      # shell-handled commands
      if action in ["quit", "exit"]:
        quit()
      elif action.startswith("cd"):
        if action == "cd":
          os.chdir(os.path.expanduser("~"))
          continue
        os.chdir(action.replace("cd ", "", 1))
      elif action.startswith("rbshctl"):
        self.rbshctl(action)
      elif action.startswith("help"):
        self.help()
      elif action in ["", "\n"]:
        continue
      else:
        self.execute_cmd(action)
    return
  
  def get_statusbar(self) -> list:
    text = "RebornShell"
    return [
      ("class:toolbar", text)
    ]
  
  async def prompt_user(self) -> None:
    action = await self.session.prompt_async(
      self.get_prompt,
      lexer = prompt_toolkit.lexers.PygmentsLexer(HtmlLexer),
      completer = self.completer,
      auto_suggest = prompt_toolkit.auto_suggest.AutoSuggestFromHistory() if self.history_completions else None,
      key_bindings = self.bindings,
      bottom_toolbar = self.get_statusbar if self.show_status_bar else None,
      mouse_support = True,
      is_password = False,
      complete_in_thread = False if self.threaded_completion else True
    )
    return action
  
  def prompt_exit(self) -> None:
    if prompt_toolkit.shortcuts.yes_no_dialog(
        title = 'Exit?',
        text = 'Do you want to exit?\nPress ENTER to quit.',
        style = prompt_toolkit.styles.Style.from_dict({
          'dialog': 'bg:#2f2f2f',
          'dialog frame.label': 'bg:#00ff00 #000000',
          'dialog.body': 'bg:#000000 #00ff00',
          'dialog shadow': 'bg:#1f1f1f',
        })
        ).run():
      exit()
  
  def execute_cmd(self, cmd: str) -> None:
    try:
      output = subprocess.check_output(cmd.split(), shell=False)
      print(output.decode("UTF-8").strip("\n"))
    except Exception:
      print("RBSH: cmd not found: " + cmd)
    return
  
  def rbshctl(self, cmd: str) -> None:
    if cmd.startswith("rbshctl get"):
      if cmd == "rbshctl get":
        print(format_dict(self.__dict__))
        return
      cmd = cmd.replace("rbshctl get ", "", 1)
      print(self.__dict__[cmd])
    return
  
  def get_prompt(self) -> str:
    return (
      get_pwd() +
      " $ "
    )
  
  def help(self) -> None:
    print("""RebornShell / Help
    Shell Commands:
     - `help` - Gets help
     - `rbshctl` - Get/set different RBSH settings
     - `cd` - Change to another directory
     - `quit` and `exit` - Exit the shell""")
    return
    
  def format_aliases(self, string: str) -> str:
    new_str = string
    for x in self.aliases.keys():
      if x in new_str:
        new_str = new_str.replace(x, self.aliases[x])
    return new_str

  def ctrlc_handler(self, signum, frame) -> None:
    return
