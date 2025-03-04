from config import load_config, _parse_args
import sys

def main(argv = sys.argv[1:]):
    # get the config data from the command-line arguments
    args = _parse_args(argv)
    config = load_config(args.config)
    
if __name__ == "__main__":
    main()