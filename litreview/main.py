from litreview.src.argparser import get_args
from litreview.src.extractor import Arxiv
from litreview.src.get_post import get_post
from litreview.src.shell_utils import download_pdf, copy_file, run, get_config_dir
from litreview.src.utils import makedirs


def doit(args):

    data = Arxiv(args.paperurl)

    print(args.postdirname)

    print(data.pdflink())
    print(data.bibtex())
    print(data.abstract())
    print(data.authors())
    print(data.title())
    print(data.date())
    print(args.categories)

    filepath = download_pdf(data.pdflink(), data.filename())

    pdfpath = f"./{args.pdfdirname}/{data.filename()}"
    with makedirs(pdfpath):
        copy_file(filepath, f"{pdfpath}/{data.filename()}.pdf")
        copy_file(filepath, f"{pdfpath}/{data.filename()}_annotated.pdf")

    # with makedirs(args.postdirname):

    the_post = get_post(data.title(), data.authors(), data.abstract(), data.pdflink(), data.bibtex(), data.date(),
                     args.categories, args, data, args.layout)

    import datetime
    with makedirs(f"./{args.postdirname}"):
        with open(f"./{args.postdirname}/{datetime.date.today().strftime('%Y-%m-%d')}-{data.filename()}.md", "w") as f:
            f.write(the_post)

def mkconf(args):
    configdir = get_config_dir()
    from os import path

    if args.overwriteconf:
        run(f"rm -rf {configdir}", shell=True)

    if path.exists(f"{configdir}/config.yaml"):
        return

    import pathlib
    current_path = pathlib.Path(__file__).parent.absolute()

    current_path = str(current_path)

    with makedirs(f"{configdir}"):
        run(f"cp {current_path}/config.yaml {configdir}/", shell=True)
        run(f"cp {current_path}/defaultlayout.md {configdir}/", shell=True)

def main():
    args = get_args()
    mkconf(args)
    doit(args)


if __name__ == "__main__":
    main()