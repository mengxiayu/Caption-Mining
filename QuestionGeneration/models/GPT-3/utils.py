import logging
from pathlib import Path
import pandas as pd

from rich.logging import RichHandler

def setup_logger(log_dir: str):
    """Create log directory and logger."""
    Path(log_dir).mkdir(exist_ok=True, parents=True)
    log_path = str(Path(log_dir) / "log.txt")
    handlers = [logging.FileHandler(log_path), RichHandler(rich_tracebacks=True)]
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(module)s] [%(levelname)s] %(message)s",
        handlers=handlers,
    )

def read_data_infer(
    data_dir: str,
    sep_tok: str = ".",
    nan_tok: str = "nan",
):
    """Read data for inference."""
    data_path = Path(data_dir)
    data_path = data_path / "extracted_sentences.txt"
    data = pd.read_csv(data_path, sep='\t')
    
    return data['sentence'].values
