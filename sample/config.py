import tomllib
from pathlib import Path
from pydantic import BaseModel
from argparse import ArgumentParser, Namespace
from pathlib import Path
from pydantic import BaseModel
from typing import Sequence
    
class GeminiConfig(BaseModel):
    api_key: str

class SchemaConfig(BaseModel):
    db_schema: str

class Config(BaseModel):
    gemini: GeminiConfig
    sql: SchemaConfig
    
def _parse_args(argv: Sequence[str]) -> Namespace:
    # create a parser object and expect one argument containing the path to config.toml and call it config
    parser = ArgumentParser()
    parser.add_argument("config", type = Path, help = "path to config.toml")
    
    # return the parsed arguments
    return parser.parse_args(argv)

def load_config(file: Path) -> Config:
    # if something goes wrong when trying to read the file
    if not all([file.exists(), file.is_file()]):
        raise FileNotFoundError(f"Config file {file} does not exist or is not a file.")
    # otherwise, load the data from the toml file and return it as a config object
    else:
        data = tomllib.loads(file.read_text())
        return Config(**data) 