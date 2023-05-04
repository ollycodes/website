import jinja2

env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
template = env.get_template("base.html")

filename = "build/test.html"
content = template.render(
    body_text="Hello World!"
)

with open(filename, mode="w", encoding="utf-8") as message:
    message.write(content)
    print(f"wrote {filename}")
