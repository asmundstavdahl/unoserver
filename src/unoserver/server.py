import argparse
import subprocess
import tempfile
from urllib import request


class UnoServer:
    def __init__(self, interface="127.0.0.1", port="2002"):
        self.interface = interface
        self.port = port

    def start(self, daemon=False):
        print("Starting unoserver.")

        with tempfile.TemporaryDirectory() as tmpuserdir:

            connection = (
                "socket,host=%s,port=%s,tcpNoDelay=1;urp;StarOffice.ComponentContext"
                % (self.interface, self.port)
            )
            tmp_uri = "file://" + request.pathname2url(tmpuserdir)

            # I think only --headless and --norestore are needed for
            # command line usage, but let's add everything to be safe.
            cmd = [
                "libreoffice",
                "--headless",
                "--invisible",
                "--nocrashreport",
                "--nodefault",
                "--nologo",
                "--nofirststartwizard",
                "--norestore",
                f"-env:UserInstallation={tmp_uri}",
                f"--accept={connection}",
            ]

            print(cmd)
            try:
                process = subprocess.Popen(cmd)
                if not daemon:
                    process.wait()
                else:
                    return process
            except Exception:
                import pdb

                pdb.set_trace()
                raise


def main():
    parser = argparse.ArgumentParser("unoserver")
    parser.add_argument(
        "--interface", default="127.0.0.1", help="The interface used by the server"
    )
    parser.add_argument("--port", default="2002", help="The port used by the server")
    args = parser.parse_args()

    server = UnoServer(args.interface, args.port)
    server.start()


if __name__ == "__main__":
    main()
