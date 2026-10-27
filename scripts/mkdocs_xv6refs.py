"""MkDocs hook: expand <!-- xv6ref: path#symbol --> into code excerpts + GitHub links."""

from pathlib import Path
import sys

from mkdocs.exceptions import PluginError

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import xv6refs  # noqa: E402

_COMMIT: str | None = None


def on_pre_build(config) -> None:
    global _COMMIT
    try:
        _COMMIT = xv6refs.read_xv6_commit()
    except xv6refs.RefError as exc:
        raise PluginError(str(exc)) from exc


def on_page_markdown(markdown: str, page, config, files) -> str:
    doc_rel = f"docs/{page.file.src_uri}"
    try:
        return xv6refs.expand_markdown_refs(markdown, doc_rel=doc_rel, commit=_COMMIT)
    except xv6refs.RefError as exc:
        raise PluginError(str(exc)) from exc
