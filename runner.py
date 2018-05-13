from green.loader import GreenTestLoader
from green.runner import run
from green.output import GreenStream

import green.config as config

import sys


def run_test(path):
    args = config.parseArguments()
    args = config.mergeConfig(args)
    args.verbose = 3

    args.targets = path

    stream = GreenStream(sys.stdout)

    loader = GreenTestLoader()
    test_suite = loader.loadTargets(args.targets)
    result = run(test_suite, stream, args)

    return result
