from ezcli import EZCLI, command, arg


@arg("--host", default=None, help="Host destination")
@arg("binary", help="Path to build (egg)")
@command(description="Deploy a binary to a device")
def deploy(args):
    src = args.binary
    dst = "%s@%s:%s" % (RPI_USER,
                        (args.host or RPI_HOST),
                        os.path.join(RPI_HOME, "evisor.egg"))
    _scp(src, dst)


@arg("-r", "--revision", default=None, help="Version Number")
@command(description="Build EspressoVisor with a version")
def build(args):
    if __debug__:  # re-run in subprocess
        print "Executing in subprocess"
        args = [sys.executable, '-OO'] + sys.argv
        sys.exit(subprocess.call(args))

    # clean up sys.argv, kind of hacky
    sys.argv = sys.argv[:1]
    build_espressovisor(args.revision)


def init():
    cli = EZCLI()

    cli.load()
    cli.execute()
