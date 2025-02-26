import tomllib
from pathlib import Path
from pydantic import BaseModel

class GeminiConfig(BaseModel):
    api_key: str

class Config(BaseModel):
    gemini: GeminiConfig
    
def load_config(file: Path) -> Config:
    # if something goes wrong when trying to read the file
    if not all([file.exists(), file.is_file()]):
        raise FileNotFoundError(f"Config file {file} does not exist or is not a file.")
    # otherwise, load the data from the toml file and return it as a config object
    else:
        data = tomllib.loads(file.read_text())
        return Config(**data)