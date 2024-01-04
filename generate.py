import os, shutil
from datetime import datetime
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader
from markdown import Markdown

INPUT_DIR, OUTPUT_DIR = "content/", "build/"
IGNORE_LIST = [".pdf", ".html"]

def refresh_dir():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    for root, _, _ in os.walk(INPUT_DIR):
        os.mkdir(root.replace(INPUT_DIR, OUTPUT_DIR))
    print(f"Cleaned {OUTPUT_DIR}")

    os.mkdir(static_output := OUTPUT_DIR + "static/")
    for root, _, files in os.walk("static/"):
        for file in files:
            shutil.copyfile(
                os.path.join(root, file),
                os.path.join(static_output, file)
            )
            print(f"copied {file} to {static_output}")

    for root, _, files in os.walk(INPUT_DIR):
        for file in files:
            if any(ext in file for ext in IGNORE_LIST):
                shutil.copyfile(
                    os.path.join(root, file),
                    os.path.join(OUTPUT_DIR, file)
                )
                print(f"copied {file} to {OUTPUT_DIR}")

def get_latest_posts():
    date_format = "%Y-%m-%d.md"
    posts = [
        {
            "path": os.path.join(root, file),
            "date": datetime.strptime(file, date_format),
        }
        for root, _, files in os.walk(INPUT_DIR)
        if "posts" in root
        for file in files
    ]
    for post in posts:
        with open(post["path"], "r") as f:
            post["title"] = f.readline().strip("\n# ")
        post["href"] = post["path"].lstrip("content").replace(".md", ".html")
        post["fdate"] = post["date"].strftime("%b %Y")
    return sorted(posts, key=lambda x: x["date"], reverse=True)

@dataclass
class Site:
    pages: list[dict]
    latest: list[dict]
    env: Environment = Environment(loader=FileSystemLoader("templates/"))

    @classmethod
    def get_pages(cls):
        pages = [
            {"root": root, "filename": file}
            for root, _, files in os.walk(INPUT_DIR)
            if files for file in files
            if not any(ext in file for ext in IGNORE_LIST)
        ]

        patterns = {".md": ".html", INPUT_DIR: OUTPUT_DIR}
        for page in pages:
            page["htmlpath"] = page["mdpath"] = os.path.join(page["root"], page["filename"])
            for key, value in patterns.items():
                page["htmlpath"] = page["htmlpath"].replace(key, value)

        latest = get_latest_posts()
        return cls(pages, latest)

    def create(self):
        base_template = self.env.get_template("base.html")
        md = Markdown(extensions=['markdown.extensions.attr_list'])

        for page in self.pages:
            with open(page["mdpath"], "r") as f:
                page["content"] = base_template.render(content=md.convert((f.read())))
            with open(page["htmlpath"], "w") as f:
                f.write(page["content"])
                print(f"created: {page['htmlpath']}")

        latest_template = self.env.get_template("latest.html")
        with open(os.path.join(OUTPUT_DIR, "blog/latest.html"), "w") as f:
            f.write(latest_template.render(posts=self.latest))
        print("updated latest")

def generate_website():
    refresh_dir()
    pages = Site.get_pages()
    pages.create()

if __name__ == "__main__":
    generate_website()
