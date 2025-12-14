from status import YaPluginStatus, SKIPPED, SUCCESS, FAILED
from util import run_command

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
      run_command(f"$(ya pkg list | grep {self.name} &>/dev/null)")
      return True
    except Exception as ex:
      return False

  def install(self):
    if self.is_installed():
      return YaPluginStatus(self, SKIPPED)

    try:
      run_command(self.command)
      return YaPluginStatus(self, SUCCESS)
    except Exception as ex:
      return YaPluginStatus(self, FAILED)

  def __str__(self):
    return self.name
