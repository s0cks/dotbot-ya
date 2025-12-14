import subprocess, dotbot
from src import YaPlugin, bcolors

__version__ = "0.0.1"


class DotbotYa(dotbot.Plugin):
    def can_handle(self, directive):
        valid = directive == "ya"
        if not valid:
            self._log.debug(
                f"The ya plugin doesn't support the `{directive}` directive"
            )
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
        num_skipped = 0
        num_failed = 0
        for name in data:
            pkg = YaPlugin(name)
            status = pkg.install()
            print(status)
            if status.is_success():
                num_installed = num_installed + 1
            elif status.is_failed():
                num_failed = num_failed + 1
            elif status.is_skipped():
                num_skipped = num_skipped + 1

        if (num_installed + num_skipped) == len(data):
            status = f"{bcolors.OKGREEN} {bcolors.ENDC}"
        else:
            status = f"{bcolors.RED} {bcolors.ENDC}"
        print(f"{status} installed {num_installed}/{len(data)} yazi plugins")
        return (num_installed + num_skipped) == len(data)
