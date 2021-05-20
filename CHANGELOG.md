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


## 0.1.1 - Prompt updates
**Added:**
- A `CONTRIBUTING.md` and a 'contributing' section in the `README.md`
- A prompt creation system in the `config.yml`
  - You can use different prefixes to generate the output from a system command, Python code, or general utilities
  - See the `config.yml` for information
- History file can be disabled in the `config.yml` by setting `history_file` to `"None"`
- Updated `install.sh`

**Known Bugs:**
- History file is still very bugged
- Colorama is broken on the `repl.it` console, untested on local machines.
