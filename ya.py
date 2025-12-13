import subprocess, dotbot, os
from pprint import PrettyPrinter

def run_command(self, command):
  try:
    if isinstance(command, list):
      command = ' '.join(command)
    elif not isinstance(command, str):
      command = str(command)
    subprocess.run([command], shell=True, check=True)
    return True
  except Exception as ex:
    self._log.error(f"failed to run command: ")
    return False

class YaPlugin:
  def __init__(self, name):
    self._name = name

  def get_command(self):
    command = []
    command.append('ya')
    command.append('pkg')
    command.append('add')
    command.append(self._name)
    return command

  def install(self):
    #TODO(@s0cks): should check if plugin needs to be installed
    return run_command(self.get_command())

  def __str__(self):
    return self._name


__version__ = "0.0.1"
class DotbotYa(dotbot.Plugin):
  def can_handle(self, directive):
    valid = directive == "ya"
    if not valid:
      self._log.debug(f"The ya plugin doesn't support the `{directive}` directive")
    return valid

  def handle(self, directive, data):
    if not self.can_handle(directive):
      return False
    try:
      pass
    except ValueError as ex:
      self._log.error(ex.args[0])
      return False

    num_installed = 0
    for plugin in data:
      try:
        self._install(plugin)
        num_installed = num_installed + 1
      except Exception as ex:
        self._log.error(f"failed to install the {plugin} plugin")
    return num_installed == length(data)

