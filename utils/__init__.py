# imports
import prompt_toolkit
from pygments.lexers import BashLexer
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.completion import FuzzyCompleter
# stdlib
import subprocess
import os



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

# gets the user's pwd without any formatting
def get_pwd_raw() -> str:
  pwd = subprocess.check_output("pwd")
  pwd = pwd.decode("UTF-8").strip("\n")
  return pwd

# formats a dict to make it look good
def format_dict(dict_: dict) -> None:
  for k, v in dict_.items():
    print(str(k) + ": " + str(v))
  return

# returns if the shell is using fuzzy completion or not
def is_fuzzy(shell) -> str:
  if shell.completer == shell.fuzzy_completer:
    return "yes"
  return "no"


# shell class
# TODO: clean up!
class Shell:
  def __init__(self,
    history_file: str = "rbsh_history",
    completer: any = None,
    bindings: any = None,
    show_status_bar: bool = True,
    history_completions: bool = True,
    threaded_completion: bool = False,
    aliases: any = None,
    version: str = "RBSH Version N/a"
  ) -> None:
    # config
    self.completer = completer
    self.bindings = bindings
    self.show_status_bar = show_status_bar
    self.history_completions = history_completions
    self.history_file = history_file
    self.threaded_completion = threaded_completion
    self.aliases = aliases
    self.VERSION = version

    # things
    self.goback = get_pwd_raw()
    self.current_completer = self.completer
    self.fuzzy_completer = None

    # prompt session
    self.session = prompt_toolkit.PromptSession(
      history = prompt_toolkit.history.FileHistory (history_file) if self.history_file != "None" else None
    )

    return
  
  async def start(self) -> None:
    self.current_completer = self.completer
    self.fuzzy_completer = FuzzyCompleter(self.completer)
    while True:
      with prompt_toolkit.patch_stdout.patch_stdout():
        # read
        action = await self.prompt_user()
      action = self.format_aliases(action)
      
      # shell-handled commands
      if action in ["quit", "exit"]:
        quit()
      elif action.startswith("cd"):
        if action == "cd":
          self.goback_dir = get_pwd_raw()
          os.chdir(os.path.expanduser("~"))
          continue
        try:
          self.goback_dir = get_pwd_raw()
          os.chdir(action.replace("cd ", "", 1))
        except FileNotFoundError:
          print("RBSH: cd: " + action.replace("cd ", "", 1) + ": No such file or directory")
      elif action.startswith("goback"):
        os.chdir(self.goback)
      elif action.startswith("rbshctl"):
        self.rbshctl(action)
      elif action.startswith("help"):
        self.help()
      elif action in ["", "\n"]:
        continue
      else:
        # eval/print
        self.execute_cmd(action)
    # loop
    return
  
  def get_statusbar(self) -> list:
    text = "RebornShell"
    return [
      ("class:toolbar", text)
    ]
  
  async def prompt_user(self) -> None:
    # get input async
    prompt = self.get_prompt()
    action = await self.session.prompt_async(
      prompt,
      lexer = PygmentsLexer(BashLexer),
      completer = self.current_completer,
      auto_suggest = AutoSuggestFromHistory() if self.history_completions else None,
      key_bindings = self.bindings,
      bottom_toolbar = self.get_statusbar if self.show_status_bar else None,
      mouse_support = True,
      is_password = False,
      complete_in_thread = False if self.threaded_completion else True,
    )
    return action
  
  def execute_cmd(self, cmd: str) -> None:
    '''
    Executes a command outside the shell
    '''
    try:
      output = subprocess.check_output(cmd.split(), shell=False)
      print(output.decode("UTF-8").strip("\n"))
    except FileNotFoundError:
      print("RBSH: cmd not found: " + cmd)
    except Exception:
      pass
    return
  
  def rbshctl(self, cmd: str) -> None:
    '''
    RBSH Control
    '''
    if cmd == "rbshctl":
      print("""RBSHCTL - RBSH Control
Usage:
rbshctl get [setting]
rbshctl version
rbshctl toggle [setting]""")
    if cmd.startswith("rbshctl get"):
      if cmd == "rbshctl get":
        print(format_dict(self.__dict__))
        return
      cmd = cmd.replace("rbshctl get ", "", 1)
      print(self.__dict__[cmd])
    elif cmd.startswith("rbshctl version"):
      print(self.VERSION)
    elif cmd.startswith("rbshctl toggle"):
      if cmd == "rbshctl toggle fuzzy":
        if self.current_completer == self.completer:
          self.current_completer = self.fuzzy_completer
        else:
          self.current_completer = self.completer
    return
  
  def get_prompt(self) -> str:
    '''
    Gets the default prompt and returns it
    '''
    return (
      get_pwd() +
      " $ "
    )
  
  def help(self) -> None:
    '''
    Prints help
    '''
    print("""RebornShell / Help
Shell Commands:
 - `help` - Gets help
 - `rbshctl` - Get/set different RBSH settings
 - `cd` - Change to another directory
 - `goback` - Go back the the last directory you were in.
 - `quit` and `exit` - Exit the shell""")
    return
    
  def format_aliases(self, string: str) -> str:
    '''
    Replaces the aliases in the string with the commands they corrispond to.
    '''
    new_str = string
    for x in self.aliases.keys():
      if x in new_str:
        new_str = new_str.replace(x, self.aliases[x])
    return new_str
