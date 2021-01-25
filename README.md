# litreview

Automates the creation of reports for literature reviews.

# Install

```
pip3 install lit-review
```
(Don't confound this tool with [this one](https://pypi.org/project/LitReview/).)

# Usage

Simply call

```
litreview <url> <categories>+
```

There are also a few optional arguments you can learn about by calling 

```
litreview --help
```

The most relevant are listed here:

- --pdfdirname allows you to change the (local) directory where the pdf files will be created
- --postdirname allows you to change the (local) directory where the report will be create
- --archive allows you to change the website scrapper to use
- --overwriteconf allows you to reset the configuration files to their defaults
- --configfile allows you to change the name of the config file to use
- --layoutfile allows you to change the name of the layout file to use

# Configurations

This utility will write config files to `/home/$USER/.config/litreview`. By default, the
files the script uses are `config.yaml` and `defaultlayout.md`. But you can add new config 
and layout files to `/home/$USER/.config/litreview` easily, and litreview will be able to use them.

Some use cases:
- I mostly want to review ML papers. I am going to change `config.yaml` and `defaultlayout.md` to reflect that.
But I want a slightly different layout for my RL papers, even if they use the same `config.yaml`. I can create `rlpaper.md` and call litreview with the
`--layoutfile rlpaper.md` argument whenever I review RL papers. Both of these use mostly the same `config` arguments,
so I'm fine with `config.yaml`.
- I review both biology and astrology papers. The `config` needed for these is completely different.
Astrology papers use `Arxiv`, but biology papers come from Nature (or whatever, I'm not a bio person k). 
I can set `config.yaml` to use `Arxiv` (like it does by default), and create `bio.yaml` to use Nature (and set the 
other parameters I need to review bio papers). When I review bio papers, I can call litreview with
`--configfile bio.yaml` and `biopaper.md`, if I have also created a new layout file.
- I want to make my reports link to the PDF and its annotated version. 
I can open up the layout file I am using, and write the links there in python's fstring formatting! Litreview
provieds the entire extracted data from the URL of the paper inside a `data` object along with every single argument
parsed from the command line inside a `args` object. To add this functionnality, I can simply add
    ```
  Link to the PDF: ./{args.pdfdirname}/{data.filename()}
  ```
  to the layout file.
- Okay, but I actually want to do something a bit funkier. Like, I don't know, reference the username I am using on this current computer, or something.
Well, litreview just uses fstrings for its report format. It's trivial to just add python code to the layout file.
    ```
  My username from my computer, for some reason? {subprocess.run("whoami", shell=True, unviversal_newlines=True, capture_output=True).stdout}
  ```
  You get the idea.
# Workflow

You want to review the paper with this link https://arxiv.org/abs/2006.11259. 

```
litreview https://arxiv.org/abs/2006.11259 rl ml proofs
```

This downloads the PDF for the paper found at that link and writes it
to the local `pdfs` folder under the `2006.11259` directory. It also duplicates it with a `_annotated` modifier
to the file name. This way you have a working copy to doodle in while also preserving the "clean" copy in a neat, organised way.

This also extracts a bunch of information from the link. It then writes a new report 
under the `_posts` local directory. The report's name is the date, plus `2006.11259`. The report
includes key, useful information, like the title of the paper, its authors, the date it was published, the current date,
the `rl ml proofs` categories you associated with it, and its abstract. It also sets up an area for you to write in.

# Philosophy/Why litreview instead of other tools?

The main goal of litreview is to be completely open source, and completely ***understandable***.

Litreview is incredibly easy to work on, and new extractors can be added trivially, simply by editing `litreview/src/extractor.py`.

I created this tool because I was frustrated with the other tools out there, because it was hard for me to extend their functionality to do what I wanted to do. And when they did support what I wanted,
the tools were bulky and included a billion other things. No. This is a simple, easy to use tool to help remove the overhead
associated with reviewing papers, and nothing else.

This tool is self-contained. It does not depend on firefox being installed, or Selenium, etc.

# Contribute

Currently, litreview only has an extractor for Arxiv. It would be cool to add extractors for many, many paper archives.

If you want to participate to this project, PRs are strongly encouraged.
