import sys
import time
import daemon
import asyncio
import importlib
import getopt

sys.path.insert(0, '/app/bin/')
from main import run

argv = sys.argv[1:]
args = []
filename = None
verbose = bool(None)

def usage():
  print(  "Usage: " + __file__ + """ [-h] [-v] [-f]

          -h,--help   print help

          -v,--verbose    verbose

          -f,--file   set config.cfg filepath

          -a,--args   any args to your service
          """)



def main():

  try:
    opts, args = getopt.getopt(argv, "hvf:a:", ["help", "verbose", "file", "args"])
  except getopt.GetoptError as err:
    print( str(err) )
    usage()
    sys.exit(2)

  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit()
    elif o in ("-f", "--file"):
      print(f'Setting config {a}')
      global filename
      filename = a
    elif o in ("-v", "--verbose"):
      print("Setting verbose mode ON")
      global verbose
      verbose = True
    elif o in ("-a", "--args"):
      args.insert(0, a)
      if verbose:
          print(f'Passing args: {args}')

  run(verbose, filename, args)

if __name__ == '__main__':
  main()
