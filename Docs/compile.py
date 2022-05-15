#!/bin/python3

import subprocess
import json
import os
import re
import shutil
import sys

class Page:
    def __init__(self) -> None:
        self.file : str = ""
        self.subPages : dict[str, Page] = {}
        self.order : list[str] = []
        self.name : str = ""
        self.level : int = 0

def cleanName(fname : str) -> str:
    fname = os.path.splitext(os.path.basename(fname))[0]

    # Clean leading digits
    m : re.Match = re.match(r'[0-9]', fname)
    if m:
        fname = fname[m.end():]

    # Clean underscores
    fname = fname.translate(fname.maketrans("_", " ")).strip()

    return fname


def safeName(name : str) -> str:
    return name.translate(name.maketrans(" ", "_")).lower()

def getSource(path : str, level : int = 0) -> Page:
    src = Page()
    src.name = cleanName(path)
    src.level = level

    if os.path.isdir(path):

        for subname in os.listdir(path):
            subpath = path + "/" + subname

            # order
            if os.path.basename(subpath) == "_order.txt":
                with open(subpath) as file:
                    for l in file.read().splitlines():
                        src.order.append(l)

            # main file
            elif cleanName(subpath) == src.name:
                src.file = subpath
            # sub pages
            elif os.path.isdir(subpath) or subpath.endswith(".md"):
                src.subPages[cleanName(subpath)] = getSource(subpath, level+1)
    else:
        src.file = path
        

    return src

def getHtmlContents(src: Page, urlPrefix = "", index = 0, indent=0) -> str:
    ret = ""
    indentstr = 4*indent*" "
            

    i = 0
    for s in src.order:
        i += 1

        if s in src.subPages.keys():
            subpage = src.subPages[s]

            if subpage.file != "":
                ret += indentstr+f'<li><a href="{urlPrefix+safeName(subpage.name)}.html">{str(i)} {subpage.name}</a>\n'
            else:
                ret += indentstr+f'<li>{str(i)} {subpage.name}\n'

            if len(subpage.order) > 0:
                ret += indentstr+f'<ul>\n'
                ret += getHtmlContents(subpage, urlPrefix+"", i, indent+1)
                ret += indentstr+f'</ul>\n'

            ret += indentstr+f'</li>\n'
        else:
            raise RuntimeError(f"subpage {s} doesn not exist")

    return ret

def toHtml(src: Page, current: Page, srcdir: str, targetdir: str):

    # Get template
    templ : str = ""
    with open(srcdir+"/template.html") as file:
        templ = file.read()
    
    # Convert current file
    if current.file != "":
        result = subprocess.run(["pandoc", current.file, "--to", "html"], stdout=subprocess.PIPE)
        pageContent : str = result.stdout.decode("utf8")

        tableOfContents = getHtmlContents(src, index = 1, indent=2)

        htmlstr = templ
        htmlstr = htmlstr.replace("(TITLE)", current.name)
        htmlstr = htmlstr.replace("(MAIN_CONTENT)", pageContent)
        htmlstr = htmlstr.replace("(NAVIGATION_SIDEBAR)", tableOfContents)

        with open(targetdir+"/"+safeName(current.name)+".html", "w") as outfile:
            outfile.write(htmlstr)

    # convert sub pages
    for name, subpage in current.subPages.items():
        toHtml(src, subpage, srcdir, targetdir)



def main():

    srcdir = sys.argv[1]
    targetdir = sys.argv[2]
    
    src = getSource(srcdir, -1)

    print(json.dumps(src, indent=4, sort_keys=True, default=lambda o: getattr(o, '__dict__', str(o))))
    print(getHtmlContents(src, index = 1))

    toHtml(src, src, srcdir, targetdir)
    shutil.copy2(srcdir+"/style.css", targetdir+"/style.css")


main()