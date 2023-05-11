import os
import shutil
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from markdown import markdown

# for updating latest.md
def get_metadata(pages: list[dict]) -> list[dict]:
    """ retrieves title, datetime, and href. """
    date_format = "%Y-%m-%d.md"
    for page in pages:
        with open(page["mdpath"], "r") as f:
            page["title"] = f.readline().strip("\n# ")
        page["datetime"] = datetime.strptime(page["filename"], date_format)
        page["date"] = page["datetime"].strftime("%b %Y")
        page["href"] = page["htmlpath"].replace("build/", "/")
    return pages

def get_latest() -> list[dict]:
    pages = get_files("content/blog/posts/")
    pages = get_metadata(pages)
    pages = sorted(pages, key=lambda x: x['datetime'], reverse=True)

    latest = [
        {
            "title": page["title"], 
            "href": page["href"],
            "date": page["date"],
        }
        for page in pages
    ]
    return latest

def update_latest_post_entries():
    env = Environment(loader=FileSystemLoader("templates/"))
    latest_template = env.get_template("latest.html")

    posts = get_latest()
    with open("build/blog/latest.html", "w") as f:
        f.write(latest_template.render(posts=posts))
    print("updated latest")

# for regular webpages
def clean_outputDir():
    inputDir, outputDir = "content/", "build/"
    if os.path.exists(outputDir):
            shutil.rmtree(outputDir)
    [
        os.mkdir(root.replace(inputDir, outputDir)) 
        for root, _, _ in os.walk(inputDir)
    ]

def get_files(path) -> list[dict]:
    pages = [
        {
            "filename": file, 
            "mdpath": os.path.join(root, file),
            "htmlpath": htmlpath(os.path.join(root, file))
        }
        for root, _, files in os.walk(path)
        for file in files
        if files
    ]
    return pages

def htmlpath(mdpath: str) -> str:
    inputDir, outputDir = "content/", "build/"
    return mdpath.replace(".md", ".html").replace(inputDir, outputDir)

def get_md_content(pages: list[dict]) -> list[dict]:
    env = Environment(loader=FileSystemLoader("templates/"))
    base_template = env.get_template("base.html")

    for page in pages:
        with open(page["mdpath"], "r") as f:
            page["content"] = base_template.render(content=markdown(f.read()))
    return pages

def make_pages(pages: list[dict]):
    for page in pages:
        with open(page["htmlpath"], "w") as f:
            f.write(page["content"])
            print(f"created: {page['htmlpath']}")

def import_css():
    cssOutputDir = "build/static/"
    os.mkdir(cssOutputDir)
    css_files = [
        shutil.copyfile(
            os.path.join(root, file), 
            os.path.join(cssOutputDir, file)
        )
        for root, _, files in os.walk("static/")
        for file in files
        if files
    ]
    for style in css_files:
        print(f"copied {style}")

def generate_website():
    clean_outputDir()
    pages = get_files("content/")
    pages = get_md_content(pages)
    make_pages(pages)

def main():
    generate_website()
    update_latest_post_entries()
    import_css()

if __name__ == "__main__":
    main()
