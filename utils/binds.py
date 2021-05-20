from prompt_toolkit.key_binding import KeyBindings

default_bindings = KeyBindings()

@default_bindings.add('c-x')
def _(event):
  " Exit when `c-x` is pressed. "
  event.app.exit()
