# RebornShell
RBSH (Pronounced "rub-ish") is a modern, powerful, and lightweight Linux shell made in Python 3.

# Requirements
- PyYAML
  - `pip(3) install pyyaml`
- prompt_toolkit
  - `pip(3) install prompt_toolkit`
- Pygments
  - `pip(3) install pygments`
- Colorama
  - `pip(3) install colorama`


# Installation
No installation instructions yet, but in a nutshell:

1. Download the source code (Can be `git clone` or downloading the zip)
2. Extract (If needed) and move the source to `.config/RebornShell/`
3. Set your shell to run `python3 ~/.config/RebornShell/main.py`
4. Open a terminal!

# ~~Doing my work for me~~ Contributing
Make a pull request or an issue, that way more features can be added or fixed.

When making an issue, please include the following:
- Issue
- Steps to reproduce
- Your `config.yml`
- RBSH Version
- Terminal
- Operating system

When making a PR, please include the following:
- What the PR adds or fixes
- Author(s) (For me to add credits)

# Configuration
The main goal of RebornShell is to allow for a huge amount of customization, as such, the `config.yml` file is quite large, so here's some info on everything in it:

## General Settings:
| Setting | Type | Description|
|-|-|-|
| `show_status_bar` | bool | Toggles the bottom status bar |
| `history_completions` | bool | Toggles suggestions should be given based on your history file |
| `history_file` | string | The path to the history file |
| `threaded_completion` | bool | Should the auto-complete be in a seperate thread |

## Auto-Completion Tree:
The auto-completions in the shell aren't normal, rather it's similar to an IDE's auto-completions, where you can select an option from a drop-down.

Here's a diagram of how the default tree in `config.yml` looks:
```
Autocompletions
     |
   /   \
 sudo  yay
/        \
pacman   -S/-R
 |
-S/-Syu/-R
```

For instance, if I were to type `sudo` in my prompt, I would get a little drop-down below my terminal cursor that would show `pacman`, and if I type `sudo pacman`, I'll get `-S`, `-Syu`, and `-R` in my auto-complete menu.

## Prompt:
The promp is quite different, it uses a placeholder system, similar to the `$PS1` variable in Zsh or Bash, except, the user makes the placeholders and decides the order for everything. This is what I meant by I wanted RBSH to be highly customizable...

The prompt has two required items, `order` and `placeholders`.

`order` is just a list, and the first character of each string in the list decides if that item is a placeholder or not. That character is `%`, so if I have an item that is `%user`, then RBSH will use the value of `placeholders`' `%user` key, and use it's value.

`placeholders` is a dict, and each item in it needs a value, even if it's just `None`. Depending on the first few characters of the item's value will change what will be inserted in the prompt when you use it.

For instance, if I have `"%example": "cmd:echo hello"`, then (in theory), when I use `%example` in `order`, then a new subprocess will be spawned, and it'll insert `hello` into the prompt. The `cmd` part tells RBSH that it's going to execute a command (Outside the shell). But as expected, there are more of these. There is `cmd`, which as stated above, executes a command, but there is also `py`, which executes Python code (This is untested, and probably slow), and there is `utils`, which doesn't execute anything custom, rather it has only a couple of values which return different values that are harder to get with `cmd` and `py`.

This all sounds incredibly complex, so here's another diagram:
```
Here's my prompt area of my config.yml:
prompt:
  order:
    - "%pwd"
    - " > "
  placeholders:
    "%pwd": "utils:pwd"

Here's what my prompt would look like:
~/path/to/where/you/are > 
```

## Statusbar:
The statusbar's configuration is exactly the same as the prompt's, it even uses `order` and `placeholders` in the same way.

## Aliases:
Aliases is just a dict, for instance:
```yml
aliases:
  ":q": "quit"
```
would make it so that when I type `:q`, the shell will run `quit` instead of `:q` (Which would be an error)

## Advanced Configuration:
If you want special features, you can poke around in `main.py`. There you can do all sorts of stuff, if you want to delete the `config.yml` file and do all of your configuration in Python, you can do that. Want a completely custom prompt or statusbar that you just can't get with `config.yml`, `main.py` has gotcha covered.

---
If you just read all of these config explainations, then congrats, you get a cookie. But otherwise, go and read it all, otherwise almost none of the `config.yml` file will make any sense at all.


