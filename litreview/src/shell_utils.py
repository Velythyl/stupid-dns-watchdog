import subprocess
import pathlib




def run(command, shell=False, capture_output=True):
    r = subprocess.run(command, shell=shell, capture_output=capture_output, check=True, universal_newlines=True)
    return r.stdout

def get_config_dir():
    return run("echo $HOME", shell=True).replace("\n", "") + "/.config/litreview"


def download_pdf(pdflink, filename):
    filepath = f"/tmp/{filename}"
    download = run(
        ["wget", "--user-agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36", "-O", filepath, pdflink],
        capture_output=False
    )
    return filepath


def copy_file(filepath, newpath):
    return run(["cp", filepath, newpath])
