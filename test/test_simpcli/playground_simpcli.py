from simpcli.simpcli import simpcli, command, optional_argument, positional_argument


@optional_argument("opt", default=None, description="Optional argument")
@positional_argument(description="Positional argument one")
@command(description="Explore simpcli")
def explore(pos, opt=None):
    print "Positional argument: %s" % pos
    print "Optional argument: %s" % opt


if __name__ == "__main__":
    simpcli.load()
    simpcli.execute()
