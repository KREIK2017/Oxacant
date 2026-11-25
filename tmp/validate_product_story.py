from pathlib import Path
from lxml import html

files = [
    Path("dist/index.html"),
    Path("handoff/oxacant-advertorial-v2/index.html"),
]

for path in files:
    document = html.fromstring(path.read_text(encoding="utf-8"))
    stories = document.xpath("//section[contains(concat(' ', normalize-space(@class), ' '), ' product-story ')]")
    story = stories[0] if stories else None
    ids = [node.get("id") for node in document.xpath("//*[@id]")]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    children = [node.get("class") for node in story.xpath("./section")] if story is not None else []
    print(
        path,
        "product_story=", story is not None,
        "children=", children,
        "benefits=", len(document.xpath("//*[contains(concat(' ', normalize-space(@class), ' '), ' product-benefits ')]//li")),
        "duplicate_ids=", duplicates,
    )
