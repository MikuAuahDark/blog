import dataclasses
import datetime
import html
import os

import jinja2
import mistune

from typing import Protocol


class Page(Protocol):
    slug: str
    title: str
    date: datetime.datetime
    last_modified: datetime.datetime | None
    content: str  # Minus the YAML header
    tags: list[str]


@dataclasses.dataclass(kw_only=True)
class PageData:
    slug: str
    title: str
    date: str  # ISO8601
    last_modified: str | None  # ISO8601
    partial_content: str
    see_more: bool


def _emit_html_tag(tag: str, attrs: dict[str, str], content: str | None) -> str:
    attr_str = " ".join(f'{k}="{html.escape(v)}"' for k, v in attrs.items())
    if len(attr_str) > 0:
        attr_str = " " + attr_str

    if content is not None:
        return f"<{tag}{attr_str}>{content}</{tag}>"
    else:
        return f"<{tag}{attr_str}>"


class FomanticRenderer(mistune.HTMLRenderer):
    def heading(self, text: str, level: int, **attrs) -> str:
        final_attr = {"class": "ui header"}
        id = attrs.get("id")
        if id:
            final_attr["id"] = id
        return _emit_html_tag(f"h{level}", final_attr, text) + "\n"

    def image(self, text: str, url: str, title: str | None = None) -> str:
        attrs = {"class": "ui bordered rounded image", "src": self.safe_url(url), "alt": text}
        if title:
            attrs["title"] = title

        return _emit_html_tag("img", attrs, None) + "\n"

    def list(self, text: str, ordered: bool, **attrs) -> str:
        attributes = {"class": "ui list"}

        if ordered:
            start = attrs.get("start")
            if start is not None:
                attributes["start"] = start
            return _emit_html_tag("ol", attributes, text) + "\n"

        return _emit_html_tag("ul", attributes, text) + "\n"

    def table(self, text: str) -> str:
        return _emit_html_tag("table", {"class": "ui celled table"}, text) + "\n"


renderer = mistune.create_markdown(
    escape=False, renderer=FomanticRenderer(), plugins=["strikethrough", "footnotes", "table", "speedup", "abbr"]
)

env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), autoescape=False)


def render(pages: list[Page]) -> dict[str, str]:
    template = env.get_template("index.html")
    page_dc: list[PageData] = []
    for p in pages:
        # Split content by first paragraph
        content_split = p.content.split("\n\n", 1)
        partial_content: str = renderer(content_split[0])
        page_dc.append(
            PageData(
                slug=p.slug,
                title=p.title,
                date=p.date.isoformat(),
                last_modified=p.last_modified.isoformat() if p.last_modified else None,
                partial_content=partial_content,
                see_more=len(content_split) > 1,
            )
        )
    return {"index.html": template.render(pages=page_dc), ".nojekyll": ""}
