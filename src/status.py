from util import bcolors

SUCCESS = 0
SKIPPED = 1
FAILED = 2

class YaPluginStatus:
  def __init__(self, pkg, status):
    self.pkg = pkg
    self.status = status

  def is_success(self):
    return self.status == SUCCESS
  
  def is_skipped(self):
    return self.status == SKIPPED

  def is_failed(self):
    return self.status == FAILED

  def __str__(self):
    if self.is_success():
      return f"{bcolors.OKGREEN} {bcolors.BOLD}{bcolors.WHITE}{self.pkg}{bcolors.ENDC} installed."
    elif self.is_skipped():
      return f"{bcolors.WARNING}! {bcolors.BOLD}{bcolors.WHITE}{self.pkg}{bcolors.ENDC} is already installed, skipping"
    return f"{bcolors.RED} {bcolors.BOLD}{bcolors.WHITE}{self.pkg}{bcolors.ENDC} failed to insall"
