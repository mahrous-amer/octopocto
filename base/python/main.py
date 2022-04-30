import sys
import time
import daemon
import asyncio
import importlib
import getopt

sys.path.insert(0, '/app/bin/')
from main import run

verbose = False
args = []

try:
  opts, args = getopt.getopt(sys.argv[1:], "hvf:a:", ["help", "verbose", "file", "args"])
except getopt.GetoptError as err:
  print( str(err) )
  usage()
  sys.exit(2)

def main():
  for o, a in opts:
    if o in ("-h", "--help"):
      print(  "Usage: " + __file__ + """ [-h] [-v] [-f]

              -h,--help   print help

              -v,--verbose    verbose

              -f,--file   set config.cfg filepath

              -a,--args   any args to your service
              """)
      sys.exit()
    elif o in ("-f", "--file"):
      FILENAME = a
    elif o in ("-v", "--verbose"):
      verbose = True
    elif o in ("-a", "--args"):
      args.append(a)

  run(args)

if __name__ == '__main__':
  main()
