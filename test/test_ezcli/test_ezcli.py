from ezcli.ezcli import EZCLI, command, optional_argument, positional_argument


@optional_argument("--opt", default=None, help="Optional argument")
@positional_argument("pos", help="Positional argument one")
@command(description="Deploy a binary to a device")
def test_print_args(args):
    print "Positional: %s" % args["pos"]
    print "Optional: %s" % args["opt"]


def init():
    cli = EZCLI()
    cli.load()
    cli.execute()


if __name__ == "__main__":
    init()
