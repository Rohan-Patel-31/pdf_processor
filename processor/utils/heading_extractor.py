import re

def extract_chapter_headings(pages):
    headings = []
    pattern = re.compile(r'^\s*(\d{1,2}[\.\)]?)\s+([A-Z].{5,})$', re.MULTILINE)

    for idx, page in enumerate(pages):
        matches = pattern.findall(page)
        for match in matches:
            heading = f"{match[0]} {match[1]}".strip()
            headings.append((heading, idx))
    
    return headings
