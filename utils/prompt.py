# This file allows generation of prompts


# imports
import colorama as cr
# stdlib
import subprocess
# local
import utils


# init
cr.init(autoreset=True)
cr.deinit()


# functions
def gen_from_dict(prompt: dict) -> str:
  cr.reinit()

  prompt_str = ""
  for x in prompt["order"]:
    # placeholders
    if x.startswith("%"):
      if prompt["placeholders"][x].startswith("cmd:"):
        to_add = subprocess.check_output(
          prompt["placeholders"][x].replace("cmd:", "", 1))
        to_add = to_add.decode("UTF-8").strip("\n")
        prompt_str += to_add
        del to_add
        continue

      elif prompt["placeholders"][x].startswith("py:"):
        prompt_str += exec(prompt["placeholders"][x].replace("py:", "",1))
        continue
      
      elif prompt["placeholders"][x].startswith("utils:"):
        if prompt["placeholders"][x] == "utils:pwd":
          prompt_str += utils.get_pwd()
        elif prompt["placeholders"][x] == "utils:pwd_small":
          prompt_str += utils.get_pwd_small()
        continue
      
      prompt_str += prompt["placeholders"][x]
    # colors
    elif x.startswith(";"):
      prompt_str += "\033m" + x + "m"
    else:
      prompt_str += x
  cr.deinit()
  return prompt_str

