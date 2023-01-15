import re


def remove_whitespace(value):
    value = re.sub(r"\s", "", value).replace("[", "").replace("]", "")
    return value


def none_to_empty_string(value):
    value = value.strip() if value is not None else ""
    return value


def extensions_to_string(value):
    ci_market_separation = value.split("/")[-1].split(".")[0]
    market_separation = {"co": "코스닥", "u": "유가증권", "f": "코넥스", "b": "비상장", "k": "K-OTC"}
    return market_separation.get(ci_market_separation, "")


def ci_list_type(value):
    ci_list_type = "신규상장" if extensions_to_string(value) in ("코스닥", "유가증권") else "이전상장"
    return ci_list_type


def one_millon_won_to_float(value):
    value = value.replace(",", "").replace("백만원", "").strip()
    if not value:
        return 0.0
    return int(value) / 10e1


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
        match = re.search(r"\d+", value)
        if match is None:
            return 0.0
        value = match.group()
        value = float(value)
        return value / 100


def string_rate_to_float(value):
    if value:
        value = value.replace(" ", "").replace("%", "")
        return float(value)
    return 0.0


def ci_po_expected_amount(value):
    return ""


def only_digits(value):
    if isinstance(value, str):
        return "".join(re.findall(r"\d+", value))


def only_digits_to_int(value):
    if isinstance(value, str):
        if value == "":
            return 0
        value = "".join(re.findall(r"\d+", value))
        if value == "":
            return 0
    return value


def only_digits_to_float(value):
    if isinstance(value, str):
        if value == "":
            return 0.0
        value = value.strip().replace(" ", "").replace("%", "")
        return float(value)
    return value


def empty_string_to_float(value):
    if isinstance(value, str) and value == "":
        return 0.0


def string_percentage_to_float(value):
    if isinstance(value, str):
        result = float(re.search(r"\d+\.\d+", value).group())
        return result
    return value


def string_capital_to_float(value):
    if isinstance(value, float) or isinstance(value, int):
        return value
    return float(re.sub(r"[^\d]", "", value))


def string_stocks_to_int(value):
    if isinstance(value, str):
        value = re.sub(r"[^\d]", "", value)
    return int(value) if value else 0


def range_of_digits(value):
    return re.sub(r"[\xa0억원원]", "", value)
