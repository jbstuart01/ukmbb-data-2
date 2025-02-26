from argparse import ArgumentParser, Namespace
from config import load_config
from pathlib import Path
import sys
from typing import Sequence


def _parse_args(argv: Sequence[str]) -> Namespace:
    # create a parser object and expect one argument containing the path to config.toml and call it config
    parser = ArgumentParser()
    parser.add_argument("config", type = Path, help = "path to config.toml")
    
    # return the parsed arguments
    return parser.parse_args(argv)

def main(argv = sys.argv[1:]):
    # get the config data from the command-line arguments
    args = _parse_args(argv)
    config = load_config(args.config)

if __name__ == "__main__":
    main()