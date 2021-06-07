# Changelog


**Key:**
- Headers are major updates
- H2's/Subtitles are minor updates or patches


# 0.0.1 - Initial Commit
Just a skeleton of the Shell


# 0.1 - Not a skeleton anymore
**Added:**
- The actual shell
- A basic configuration
- History + history suggestions (like ZSH/Fish)
- Vim CoC-like autocomplete
- An `install.sh` file
  - Just installs the `pip3` requirements.

**Known Bugs:**
- History file doesn't use the correct location, and always makes `rbsh_history` file in the current directory.


# 0.2 - Customization, aliases, and async
**Added:**
- A `CONTRIBUTING.md` and a 'contributing' section in the `README.md`
- A prompt creation system in the `config.yml`
  - You can use different prefixes to generate the output from a system command, Python code, or general utilities
  - See the `config.yml` for information
- History file can be disabled in the `config.yml` by setting `history_file` to `"None"`
- Updated `install.sh`
- Added a `help` command
- Made the shell use a little bit of Async
- `README.md` now has documentation on configuration
- Aliases!

**Known Bugs:**
- History file is still very bugged
- Colorama seems to be broken on the `repl.it` console, untested on local machines.


# 0.2.1 - Fuzzy finding and rbshctl updates
**Added:**
- Fuzzy finding
- RBSHCtl has more functions
- `Shell` class has args rather than needing to change the variables manually.

**Removed:**
- Colorama
- Removed `utils/binds.py`
- `prompt_exit()` function from the `Shell` class

**Fixed Bugs:**
- Pressing `ctrl+c` no longer exits the Shell
- Keybindings actually work now

**Known Bugs:**
- History is, as always, bugged.


# 0.2.2 - Pypes and Py Mode
**Added:**
- "Pype"-ing
  - By surrounding Python code in `s;` and `;e`, you can get the output of the code and use that
  - Ex: `echo s;print("text");e` prints `test`
- Py Mode, allowing you to run Python code in RBSH if you switch to the mode.
  - It's a mode because having a shell *and* Python can cause some conflicting bugs, and I'm not ready to deal with that...

**Fixed Bugs:**
- History file does work! It just needed an **absolute** path, so `~` doesn't work.
- Aliases no longer replace any instance of text, just the first ones
