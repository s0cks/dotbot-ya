import subprocess, dotbot

__version__ = "0.0.1"


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    UWHITE = "\033[4;37m"
    WHITE = "\033[37m"
    RED = "\033[31m"


def run_command(command):
    if isinstance(command, list):
        command = " ".join(command)
    elif not isinstance(command, str):
        command = str(command)
    subprocess.run([command], shell=True, check=True)


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


class YaPlugin:
    def __init__(self, name):
        self.name = name
        self.command = [
            "ya",
            "pkg",
            "add",
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
