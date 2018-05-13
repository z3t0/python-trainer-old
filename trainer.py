from sys import argv
from util import setup, init, select, test


def show_help():
    print("""Usage:
trainer.py [cmd]
cmd: setup or test""")


if __name__ == '__main__':
    init()

    if len(argv) >= 2:
        cmd = argv[1]

        if cmd == 'setup':
            setup()
        elif cmd == 'select':
            select(int(argv[2]))
        elif cmd == 'test':
            test()
        # elif cmd == 'add':
        #     repo = argv[2]
        else:
            show_help()
    else:
        show_help()
