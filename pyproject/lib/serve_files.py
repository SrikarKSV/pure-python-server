from jinja2 import Template
from pathlib import Path


def render_template(file):
    templates_directory = Path.cwd() / "pyproject" / "templates"
    print(templates_directory)
    with open(templates_directory / file, "r", encoding="utf-8") as f:
        template = Template(f.read())
        html = template.render()
        return [bytes(html, "utf-8")]
