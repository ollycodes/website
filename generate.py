import os
import shutil
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from markdown import markdown

# for updating latest.md

def get_metadata(pages: list[dict]) -> list[dict]:
    """ retrieves title, datetime, and href. """
    for page in pages:
        with open(page["mdpath"], "r") as f:
            page["title"] = f.readline().strip("\n# ")
        year, month, day = [
            int(x) 
            for x in page["filename"].strip(".md").split("-")
        ]
        page["datetime"] = datetime(year, month, day)
        page["href"] = page["htmlpath"].replace("build/", "/")
    return pages

def get_latest() -> list[dict]:
    pages = get_files("content/blog/posts/")
    pages = get_metadata(pages)
    pages = sorted(pages, key=lambda x: x['datetime'], reverse=True)

    latest = [
        {"title": page["title"], "href": page["href"]}
        for page in pages
    ]
    return latest

def update_latest():
    env = Environment(loader=FileSystemLoader("templates/"))
    latest_template = env.get_template("latest.html")

    latest = get_latest()
    with open("build/blog/latest.html", "w") as f:
        f.write(latest_template.render(blogs=latest))
    print("updated latest")

# for regular webpages
def get_md_content(pages: list[dict]) -> list[dict]:
    env = Environment(loader=FileSystemLoader("templates/"))
    base_template = env.get_template("base.html")

    for page in pages:
        with open(page["mdpath"], "r") as f:
            page["content"] = base_template.render(content=markdown(f.read()))
    return pages

def htmlpath(mdpath: str) -> str:
    inputDir, outputDir = "content/", "build/"
    return mdpath.replace(".md", ".html").replace(inputDir, outputDir)

def get_files(path) -> list[dict]:
    pages = [
        {
            "filename": file, 
            "mdpath": os.path.join(root, file),
            "htmlpath": htmlpath(os.path.join(root, file))
        }
        for root, _, files in os.walk(path)
        for file in files
        if file not in ("latest.md")
    ]
    return pages

def clean_outputDir():
    inputDir, outputDir = "content/", "build/"
    if os.path.exists(outputDir):
            shutil.rmtree(outputDir)
    [
        os.mkdir(root.replace(inputDir, outputDir)) 
        for root, _, _ in os.walk(inputDir)
    ]

def make_pages(pages: list[dict]):
    for page in pages:
        with open(page["htmlpath"], "w") as f:
            f.write(page["content"])
            print(f"created: {page['htmlpath']}")

def generate_website():
    clean_outputDir()
    pages = get_files("content/")
    pages = get_md_content(pages)
    make_pages(pages)

if __name__ == "__main__":
    generate_website()
    update_latest()
