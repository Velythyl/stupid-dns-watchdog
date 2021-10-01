import datetime

from litreview.src.shell_utils import get_config_dir
import subprocess
import time
import os

def get_post(title, authors, abstract, pdflink, bibtex, date, categories, args, format_path=None):
    assert format_path is not None

    with open(f"{get_config_dir()}/{format_path}", "r") as f:
        format = f.read()

    return apply_variables(title, authors, abstract, pdflink, bibtex, date, categories, args, format)

def get_special_variables(title, authors, abstract, pdflink, bibtex, date, categories, args):
    x = vars(args)

    for key, VAL in x.items():
        parsed = get_special_variable(title, authors, abstract, pdflink, bibtex, date, categories, args, VAL)

        x[key] = parsed
    import argparse
    return argparse.Namespace(**x)


def get_special_variable(title, authors, abstract, pdflink, bibtex, date, categories, args, EVAL_STRING):
    if isinstance(EVAL_STRING, str):
        if EVAL_STRING.startswith("{") and EVAL_STRING.endswith("}"):
            parsed = apply_variables(title, authors, abstract, pdflink, bibtex, date, categories, args, f"f\"{EVAL_STRING}\"")
            import re
            parsed = re.sub(r"\s", "_", parsed)
            return parsed
    return EVAL_STRING

def apply_variables(title, authors, abstract, pdflink, bibtex, date, categories, args, EVAL_STRING):
    return eval(EVAL_STRING).strip()