import subprocess, dotbot, os
from pprint import PrettyPrinter

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  UWHITE = '\033[4;37m'

def _run_command(command):
  if isinstance(command, list):
    command = ' '.join(command)
  elif not isinstance(command, str):
    command = str(command)
  subprocess.run([command], shell=True, check=True)

class YaPlugin:
  def __init__(self, name):
    self.name = name
    self.command = [
      'ya',
      'pkg',
      'add',
      name,
    ]

  def is_installed(self):
    try:
      _run_command(f"$(ya pkg list | grep {self.name} &>/dev/null)")
      return True
    except Exception as ex:
      return False

  def install(self):
    if self.is_installed():
      print(f"\t- {bcolors.OKCYAN} {bcolors.BOLD}{bcolors.UWHITE}{self.name}{bcolors.ENDC} already installed, skipping")
      return
    _run_command(self.command)

  def __str__(self):
    return self.name


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

    print(f"installing {len(data)} yazi plugins....")
    num_installed = 0
    for name in data:
      try:
        pkg = YaPlugin(name)
        pkg.install()
        num_installed = num_installed + 1
      except Exception as ex:
        self._log.error(f"failed to install the {plugin} plugin")

    if num_installed == len(data):
      status = f"{bcolors.OKGREEN} {bcolors.ENDC}"
    else:
      status = f"{bcolors.RED} {bcolors.ENDC}"
    print(f"\t{status} installed {num_installed}/{len(data)} yazi plugins")
    return num_installed == len(data)

