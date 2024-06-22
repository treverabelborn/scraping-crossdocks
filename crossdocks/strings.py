
def clean_str(str):
    if str is None:
        return str
    return str.replace('\r', '') \
        .replace('\n', '') \
        .replace('\t', '') \
        .strip()
