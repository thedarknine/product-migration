"""File utility tool."""

import os
from sources.utilities import logs

logger = logs.get_logger()


def get_content(filename: str, filepath: str) -> str:
    """Get content of file.

    Args:
        filename (str): File name
        filepath (str): File path

    Returns:
        str: Content of file
    """
    try:
        content = ""
        with open(
            os.path.join(filepath, filename),
            "rt",
            encoding=os.getenv("ENCODING", "utf-8"),
        ) as inputfile:
            content = inputfile.read()
            inputfile.close()
        return content
    except FileNotFoundError:
        logger.error("File not found: %s", filename)
        return None
