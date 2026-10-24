"""Turn one dataset card into simple, countable features, and a 0-6 documentation checklist score."""
import re

def split_card(text):
    """A Hugging Face card = a YAML block between '---' lines (metadata) + free-text markdown."""
    m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n?(.*)", text, re.S)
    return (m.group(1), m.group(2)) if m else ("", text)

def has(pattern, text): return bool(re.search(pattern, text, re.I))

def card_features(text):
    meta, body = split_card(text)
    words = len(re.findall(r"\w+", body))
    f = {
        "has_card": int(len(text.strip()) > 0),
        "log_words": float(__import__("math").log1p(words)),
        "n_headings": len(re.findall(r"^#{1,4} ", body, re.M)),
        "has_code_or_table": int("```" in body or "|---" in body or "| ---" in body),
        "meta_license": int(has(r"^license\s*:", meta) or has(r"^license_name\s*:", meta)),
        "meta_tasks": int(has(r"^task_categories\s*:", meta)),
        "meta_language": int(has(r"^language\s*:", meta)),
        "meta_size": int(has(r"^size_categories\s*:", meta)),
        "text_source": int(has(r"source|collected|curat|scrap|generated|annotat|derived from", body)),
        "text_intended_use": int(has(r"intended use|use case|direct use|uses\b|designed for|can be used", body)),
        "text_limitations": int(has(r"limitation|bias|risk|caveat|known issue|out-of-scope|ethic", body)),
        "text_citation": int(has(r"citation|bibtex|@misc|@article|@inproceedings|cite", body)),
    }
    # The checklist: six yes/no questions a would-be user would ask of a card.
    f["checklist"] = (f["meta_license"] + f["text_source"] + f["text_intended_use"]
                      + f["text_limitations"] + f["text_citation"] + int(words >= 100))
    return f
