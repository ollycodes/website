import os
from jinja2 import Environment, FileSystemLoader
from markdown import markdown

def get_content(path: str) -> list:
    folderpath = path.replace("content/", "build/")
    
    files = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            filename = item.split(".")[0]
            print(f"working on: {filename}")
            filepath = os.path.join(folderpath, f"{filename}.html")
            files.append(
                {
                    "md": item_path,
                    "folderpath": folderpath,
                    "filepath": filepath,
                }
            )
        elif os.path.isdir(item_path):
            print(f"found folder: {item}/")
            files += get_content(item_path)
    return files

def update_latest():
    postpath = "content/blog/posts/"
    latest = "content/blog/latest.md"

    posts = os.listdir(postpath)
    newest_to_oldest = sorted(
        posts, 
        key=lambda post: os.path.getmtime(os.path.join(postpath, post)), 
        reverse=True
    )
    content = ""
    for post in newest_to_oldest:
        with open(postpath + post, "r") as f:
            a = f.readline().strip("\n")
            href = postpath + post
            content += f"[{a}]({href})\n"
    with open(latest, "w") as f:
            f.write(content)

def create_website() -> None:
    env = Environment(loader=FileSystemLoader("templates/"))
    base_template = env.get_template("base.html")

    files = get_content("content/")
    for file in files:
        if not os.path.exists(file["folderpath"]):
            os.makedirs(file["folderpath"])
        with open(file["md"], mode="r") as f:
            content = markdown(f.read())
            html = base_template.render(content=content)
        with open(file["filepath"], "w") as f:
            f.write(html)

if __name__ == "__main__":
    update_latest()
    create_website()
