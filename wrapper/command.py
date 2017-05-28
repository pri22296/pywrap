import subprocess
import shlex
import sys

SEPERATOR = ' '
SHORT_PREFIX = '-'
LONG_PREFIX = '--'


def convert_option(value):
    string = str(value)
    if len(string) == 1:
        return SHORT_PREFIX + string
    else:
        return LONG_PREFIX + string.replace('_', '-').replace('--', '_')


def convert_arg(value):
    string = str(value)
    return repr(string) if ' ' in string else string


def execute(command):
    # https://stackoverflow.com/a/4418193/4127836
    process = subprocess.Popen(command, shell=True,
                               universal_newlines=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

    # Poll process for new output until finished
    while True:
        nextline = str(process.stdout.readline())
        if nextline == '' and process.poll() is not None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

    output = str(process.communicate()[0])
    exitCode = process.returncode

    if (exitCode == 0):
        return output
    else:
        raise subprocess.CalledProcessError(returncode=exitCode,
                                           cmd=command,
                                           output=output)


def dict2opt(options):
    opt_args = []
    for key, value in options.items():
        if value is False:
            continue
        elif value is True or value is None:
            opt_args.append(convert_option(key))
        else:
            opt_args.append(SEPERATOR.join([convert_option(key),
                                            convert_arg(value)]))
    return opt_args


class Command(object):
    def __init__(self, command, *args, **kwargs):
        self._command = command.split()
        self._options = kwargs
        self._args = args

    def __str__(self):
        pos_args = list(convert_arg(arg) for arg in self._args)
        opt_args = dict2opt(self._options)
        cmd = self._command + opt_args + pos_args
        return ' '.join(self._command + opt_args + pos_args)

    def __getattr__(self, name):
        cmd = ' '.join(self._command + [name])
        return Command(cmd, *self._args, **self._options)

    def __call__(self, *args, **kwargs):
        options = self._options.copy()
        options.update(kwargs)

        opt_args = dict2opt(options)
        pos_args = list(convert_arg(arg) for arg in args)

        cmd = Command(' '.join(self._command),
                       *(list(self._args) + list(args)),
                       **options)

        output = execute(str(cmd))
        return cmd

