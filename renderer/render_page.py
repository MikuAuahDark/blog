import datetime
import html
import os
import re

import jinja2
import mistune


from typing import Protocol

SOURCE_CODE = "https://github.com/MikuAuahDark/blog/blob/master/%(id)s.md"


class Page(Protocol):
    slug: str
    title: str
    date: datetime.datetime
    last_modified: datetime.datetime | None
    content: str  # Minus the YAML header
    tags: list[str]


def _emit_html_tag(tag: str, attrs: dict[str, str], content: str | None) -> str:
    attr_str = " ".join(f'{k}="{html.escape(v)}"' for k, v in attrs.items())
    if len(attr_str) > 0:
        attr_str = " " + attr_str

    if content is not None:
        return f"<{tag}{attr_str}>{content}</{tag}>"
    else:
        return f"<{tag}{attr_str}>"


def slugify(text: str):
    slug = text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug.strip("-")


class FomanticRenderer(mistune.HTMLRenderer):
    def __init__(self, escape: bool = True, allow_harmful_protocols: bool | None = None) -> None:
        super(FomanticRenderer, self).__init__(escape, allow_harmful_protocols)
        self.heading_ids = set[str]()

    def heading(self, text: str, level: int, **attrs) -> str:
        final_attr = {"class": "ui header"}
        id: str | None = attrs.get("id")
        if id:
            final_attr["id"] = id
        else:
            id = slugify(text)
            original_id = id
            i = 1
            while id in self.heading_ids:
                id = f"{original_id}-{i}"
                i += 1

        self.heading_ids.add(id)
        final_attr["id"] = id

        a = _emit_html_tag("a", {"href": f"#{id}"}, text)
        acopy = _emit_html_tag(
            "a", {"class": "copy", "title": "Copy link to clipboard"}, '<i class="linkify icon"></i>'
        )
        return _emit_html_tag(f"h{level}", final_attr, f"{a} {acopy}") + "\n"

    def block_quote(self, text: str) -> str:
        if text.startswith("<p>[!NOTE]\n"):
            text = f"""
            <div class="ui blue icon message">
                <i class="info icon"></i>
                <div class="content">
                    <div class="header">Note</div>
                    <p>{text[11:]}
                </div>
            </div>
"""
        elif text.startswith("<p>[!TIP]\n"):
            text = f"""
            <div class="ui green icon message">
                <i class="lightbulb outline icon"></i>
                <div class="content">
                    <div class="header">Tip</div>
                    <p>{text[10:]}
                </div>
            </div>
"""
        elif text.startswith("<p>[!WARNING]\n"):
            text = f"""
            <div class="ui yellow icon message">
                <i class="exclamation triangle icon"></i>
                <div class="content">
                    <div class="header">Warning</div>
                    <p>{text[14:]}
                </div>
            </div>
"""
        elif text.startswith("<p>[!CAUTION]\n"):
            text = f"""
            <div class="ui red icon message">
                <i class="exclamation circle icon"></i>
                <div class="content">
                    <div class="header">Caution</div>
                    <p>{text[14:]}
                </div>
            </div>
"""
        else:
            text = f"<blockquote>\n{text}</blockquote>\n"
        return text

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


def render(page: Page) -> str:
    template = env.get_template("page.html")
    return template.render(
        title=page.title,
        date=page.date.isoformat(),
        last_modified=page.last_modified.isoformat() if page.last_modified else None,
        content=renderer(page.content),
        tags=page.tags,
        source=SOURCE_CODE % {"id": page.slug},
    )
