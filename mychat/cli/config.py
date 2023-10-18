import typer
from typing_extensions import Annotated
from pathlib import Path
from .app import app
from ..config import EXISTING_CONFIG_FILEPATH

@app.command()
def config(
        file: Annotated[
            Path,
            typer.Argument(
                show_default=False,
                help="Configuration file path"
            )
        ]
    ):
    
    # Read raw file content
    file_content = file.read_bytes()
    
    # Write to the destination
    if not EXISTING_CONFIG_FILEPATH.is_file():
        EXISTING_CONFIG_FILEPATH.parent.mkdir(parents=True, exist_ok=True)
        EXISTING_CONFIG_FILEPATH.touch()
    EXISTING_CONFIG_FILEPATH.write_bytes(file_content)
