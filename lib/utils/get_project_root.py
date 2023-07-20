import pathlib

def get_project_root() -> pathlib.Path:
    """Returns project root folder."""
    return pathlib.Path(__file__).parent.parent.parent