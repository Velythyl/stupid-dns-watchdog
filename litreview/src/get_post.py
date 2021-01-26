import datetime

from litreview.src.shell_utils import get_config_dir
import subprocess
import time
import os

def get_post(title, authors, abstract, pdflink, bibtex, date, categories, args, data, format_path=None):
    assert format_path is not None

    with open(f"{get_config_dir()}/{format_path}", "r") as f:
        format = f.read()

    return eval(format).strip()