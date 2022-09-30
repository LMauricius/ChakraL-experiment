#!/bin/python3

import subprocess
import json
import os
import re
import shutil
import sys
from typing import List

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

def getSourceStructure(path : str, level : int = 0) -> Page:
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
                src.subPages[cleanName(subpath)] = getSourceStructure(subpath, level+1)
    else:
        src.file = path
        

    return src

def getHtmlContents(src: Page, urlPrefix = "", index = 0, indent=0, current="") -> str:
    ret = ""
    indentstr = 4*indent*" "
            

    i = 0
    for s in src.order:
        i += 1

        if s in src.subPages.keys():
            subpage = src.subPages[s]

            if subpage.name.lower() == current.lower():
                ret += indentstr+f'<li><b>{str(i)} {subpage.name}</b>\n'
            elif subpage.file != "":
                ret += indentstr+f'<li><a href="{urlPrefix+safeName(subpage.name)}.html">{str(i)}&nbsp{subpage.name}</a>\n'
            else:
                ret += indentstr+f'<li>{str(i)}&nbsp{subpage.name}\n'

            if len(subpage.order) > 0:
                ret += indentstr+f'<ul>\n'
                ret += getHtmlContents(subpage, urlPrefix+"", i, indent+1, current)
                ret += indentstr+f'</ul>\n'

            ret += indentstr+f'</li>\n'
        else:
            raise RuntimeError(f"subpage {s} does not exist")

    return ret

def buildHtmlChunks(src: Page, currentPage: Page, srcdir: str, builddir: str, syntaxDefs: "list[str]"):
    
    # Convert current file
    if currentPage.file != "":
        outfilename = builddir+"/"+safeName(currentPage.name)+".html"
        print(f"Checking chunk {outfilename}...")
        if (not os.path.exists(outfilename)) or os.path.getmtime(currentPage.file) > os.path.getmtime(outfilename):
            #print(["pandoc", currentPage.file, "--to", "html", "--highlight-style", f"{builddir}/highlight.theme"] + [x for d in syntaxDefs for x in ("--syntax-definition", d)])
            result = subprocess.run(["pandoc", currentPage.file, "--to", "html", "--highlight-style", f"{builddir}/highlight.theme"] + [x for d in syntaxDefs for x in ("--syntax-definition", d)], stdout=subprocess.PIPE)
            pageContent : str = result.stdout.decode("utf8")

            print(f"Generating chunk {outfilename}...")
            with open(outfilename, "w+") as outfile:
                outfile.write(pageContent)
                print(f"Generated chunk {outfilename}")
        else:
            print(f"Generating not needed")

    # convert sub pages
    for name, subpage in currentPage.subPages.items():
        buildHtmlChunks(src, subpage, srcdir, builddir, syntaxDefs)

def buildHtmlFile(templ : str, src: Page, infilename: str, outfilename: str):
    currentName = cleanName(infilename)
    tableOfContents = getHtmlContents(src, index = 1, indent=2, current = currentName)

    with open(infilename, "r") as file:
        pageContent = file.read()

        htmlstr = templ
        htmlstr = htmlstr.replace("(TITLE)", currentName)
        htmlstr = htmlstr.replace("(MAIN_CONTENT)", pageContent)
        htmlstr = htmlstr.replace("(NAVIGATION_SIDEBAR)", tableOfContents)

        with open(outfilename, "w+") as outfile:
            outfile.write(htmlstr)




def main():

    srcdir = sys.argv[1]
    targetdir = sys.argv[2]
    builddir = sys.argv[3]
    themestyle = sys.argv[4]

    # list syntaxdefs
    syntaxDefs = []
    for subname in os.listdir(srcdir+"/syntaxparsers"):
        infilename = srcdir + "/syntaxparsers/" + subname
        if not os.path.isdir(subname):
            syntaxDefs.append(infilename)

    # save theme
    result = subprocess.run(["pandoc", "--print-highlight-style", themestyle], stdout=subprocess.PIPE)
    with open(f"{builddir}/highlight.theme", 'w+') as ofile:
        ofile.write(result.stdout.decode("utf8"))
    subprocess.run(["pandoc", f"--template={srcdir}/pandoc-template-syntax.css", srcdir+"/pandoc-used-syntax-blocks.md", "--highlight-style", f"{builddir}/highlight.theme", "-o", targetdir+"/syntax_style.css"] + [x for d in syntaxDefs for x in ("--syntax-definition", d)])
    
    # get source
    src = getSourceStructure(srcdir+"/content", -1)

    # Get template
    templ : str = ""
    with open(srcdir+"/template.html") as file:
        templ = file.read()

    #print(json.dumps(src, indent=4, sort_keys=True, default=lambda o: getattr(o, '__dict__', str(o))))
    #print(getHtmlContents(src, index = 1))

    # Check if the file structure has changed
    unselectedContents = getHtmlContents(src, index = 1, indent=2, current = "")
    contentsUpdated = True
    if os.path.exists(builddir+"/cached-contents.html"):
        with open(builddir+"/cached-contents.html", "r") as file:
            if file.read() == unselectedContents:
                contentsUpdated = False
    if contentsUpdated:
        with open(builddir+"/cached-contents.html", "w+") as file:
            file.write(unselectedContents)
    
    if contentsUpdated:
        print("Contents changed, rebuilding all...")

    # Build html files in /build dir
    buildHtmlChunks(src, src, srcdir+"/content", builddir, syntaxDefs)

    # Generate final html in target dir and copy needed files
    for subname in os.listdir(builddir):
        infilename = builddir + "/" + subname
        if subname.endswith(".html") and subname != "cached-contents.html" and not os.path.isdir(subname):
            outfilename = targetdir + "/" + subname
            if contentsUpdated or (not os.path.exists(outfilename)) or os.path.getmtime(infilename) > os.path.getmtime(outfilename):
                print(f"Building {outfilename}")
                buildHtmlFile(templ, src, infilename, outfilename)
        
    shutil.copy2(srcdir+"/style.css", targetdir+"/style.css")


main()