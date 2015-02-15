import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import argparse

# ============================================================================#
# Simple HTTP Server used for browsing file system from a browser web         #
#                                                                             #
# usage:                                                                      #
# python ServerHTTP.py [ -n port ] [ -p path ]                                #
#                                                                             #
# type "python ServerHTTP.py -h" for an help                                  #
# ============================================================================#


def parseArgs():

    argparser = argparse.ArgumentParser(description="Little http server")

    argparser.add_argument('-p', '--path', help="Path",
                           default="D:\\", dest="path")

    argparser.add_argument('-n', '--port', help="Port",
                           type=int, default=80, dest="port")

    return argparser.parse_args()


# getting arguments
args = parseArgs()
# chdir to target path
os.chdir(args.path)
# local address + specified port
server_address = ('', args.port)
# setting protocol version to HTTP/1.0
SimpleHTTPRequestHandler.protocol_version = "HTTP/1.0"
# creating server
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
# log
print("Serving on port {port} and path {path}"
      .format(port=args.port, path=args.path))
# starting server
httpd.serve_forever()
