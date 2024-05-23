import re


def unwrap_tag(prefix: str, suffix: str, text: str) -> str:
    pattern = f"{prefix}(.*?){suffix}"
    content = re.compile(pattern, re.DOTALL)
    match = content.search(text)
    return match.group(1) if match else ""
