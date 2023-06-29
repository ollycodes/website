import os, shutil
from datetime import datetime
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader
from markdown import markdown

INPUT_DIR, OUTPUT_DIR = "content/", "build/"

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
                (style := os.path.join(static_output, file))
            )
            print(f"copied {style}")

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
        ]

        patterns = {".md": ".html", INPUT_DIR: OUTPUT_DIR}
        for page in pages:
            page["htmlpath"] = page["mdpath"] = os.path.join(page["root"], page["filename"])
            for key, value in patterns.items():
                page["htmlpath"] = page["htmlpath"].replace(key, value)

        latests = get_latest_posts()
        return cls(pages, latests)

    def create(self):
        template_base = self.env.get_template("base.html")

        for page in self.pages:
            with open(page["mdpath"], "r") as f:
                page["content"] = template_base.render(content=markdown(f.read()))
            with open(page["htmlpath"], "w") as f:
                f.write(page["content"])
                print(f"created: {page['htmlpath']}")

        template_latest = self.env.get_template("latest.html")
        with open("build/blog/latest.html", "w") as f:
            f.write(template_latest.render(posts=self.latest))
        print("updated latest")

def generate_website():
    refresh_dir()
    pages = Site.get_pages()
    pages.create()

if __name__ == "__main__":
    generate_website()
