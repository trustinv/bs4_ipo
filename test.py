import re


def extract_string(text):
    # Case 1: / between characters
    match = re.search(r"(?<=://)[^/]*", text)
    if match:
        return match.group(0)
    else:
        match = re.search(r"[/]*([^/]+)[/]*", s)
        if match:
            return match.group(1)
        else:
            return ""


# print(extract_string("s://maum.ai/"))  # 예상 결과: maum.ai
# print(extract_string("/picogram.com"))  # 예상 결과: picogram.com
# print(extract_string("picogram.com/"))  # 예상 결과: picogram.com
# print(extract_string("안녕"))  # ""

import re


def extract_string(s):
    match = re.search(r"[/]*([^/]+)[/]*", s)
    if match:
        return match.group(1)
    else:
        return None


print(extract_string("/picogram.com"))  # Expected result: picogram.com
print(extract_string("picogram.com/"))  # Expected result: picogram.com
