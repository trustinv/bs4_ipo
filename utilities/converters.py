import re


# def represent_ci_name_n_code(value):
#     match = re.search(r"(\S+)\s+(\d+)", value)
#     b, c = match.group(1), match.group(2)
#     return b, c


# def allow_koreans_letters(value):
#     # Define a regular expression pattern to match non-Korean characters
#     pattern = re.compile("[^\u3131-\u3163\uac00-\ud7a3]+")

#     # Use the sub method to replace all non-Korean characters with an empty string
#     return pattern.sub("", value)


def none_to_empty_string(value):
    value = value if value is not None else ""
    return value.strip()


def extensions_to_string(value):
    ci_market_separation = value.split("/")[-1].split(".")[0]
    market_separation = {"co": "코스닥", "u": "유가증권", "f": "코넥스", "b": "비상장", "k": "K-OTC"}
    return market_separation.get(ci_market_separation, "")


def ci_list_type(value):
    ci_list_type = "신규상장" if extensions_to_string(value) in ("코스닥", "유가증권") else "이전상장"
    return ci_list_type


def one_millon_won_to_float(value):
    if not isinstance(value, float):
        value = re.sub(r"\xa0백만원", "", value)
        value = value.replace(",", "")
        return float(int(int(value) / 100))
    return 0.0


def dot_dash_to_slash(value):
    if isinstance(value, str):
        value = re.sub(r"[.-]", "/", value)
        return value
    return ""


def month_to_int(value):
    if isinstance(value, int):
        return value
    value = re.search(r"\d+", value).group()
    return int(value)


def worker_to_int(value):
    if isinstance(value, str):
        value = re.sub(r"(\d+)명", r"\1", value)
        return int(value)
    return 0


def string_rate_to_percentage(value):
    if not isinstance(value, float):
        value = re.search(r"\d+", value).group()
        value = float(value)
        return value / 100
    return value


def string_rate_to_float(value):
    if not isinstance(value, float):
        value = re.search(r"\d+", value).group()
        value = float(value)
        return value
    return float(value)


def ci_po_expected_amount(value):
    return ""


def only_digits(value):
    return "".join(re.findall(r"\d+", value))


def empty_string_to_float(value):
    if isinstance(value, str) and value == "":
        return 0.0


def string_percentage_to_float(value):
    return float(re.search(r"\d+\.\d+", value).group())


def string_capital_to_float(value):
    if isinstance(value, float) or isinstance(value, int):
        return value
    return float(re.sub(r"[^\d]", "", value))


def string_stocks_to_int(value):
    if isinstance(value, str):
        value = re.sub(r"[^\d]", "", value)
    return int(value) if value else 0
