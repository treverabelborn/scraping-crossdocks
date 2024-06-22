

def clean_str(str):
    if str is None:
        return str
    return str.replace('\r', ' ') \
        .replace('\n', '') \
        .replace('\t', '') \
        .replace('\xa0', '') \
        .strip()


def email_end_idx(js):
    top_level_domains = ['com`', '.COM`', '.net`', '.NET`', '.us`', '.site`', '.info`', '.ws`']

    for tld in top_level_domains:
        if tld in js:
            return js.index(tld) + len(tld)
    
    print(js)
    raise Exception('Failed to get email')


def email_start_idx(js):
    email_locator_start = 'Email Has Been Sent to '
    return js.index(email_locator_start) + len(email_locator_start)


def extract_email(js):
    return js[email_start_idx(js):email_end_idx(js)]