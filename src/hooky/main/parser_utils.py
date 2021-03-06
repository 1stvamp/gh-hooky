import re

ISSUE_REGEX = re.compile(r'toward[s]* #([0-9])*', re.IGNORECASE)
HASH_REGEX = re.compile(r'#[0-9a-zA-Z+_]*', re.IGNORECASE)
USER_REGEX = re.compile(r'@[0-9a-zA-Z+_]*', re.IGNORECASE)

def parse_message(msg):
    data = {
            'issues': [],
            'hashtags': [],
            'users': [],
    }
    for text in ISSUE_REGEX.finditer(msg):
        try:
            data['issues'].append(text.group(1).replace('#',''))
        except IndexError:
            pass
    for text in HASH_REGEX.finditer(msg):
        try:
            data['hashtags'].append(text.group(0).replace('#',''))
        except IndexError:
            pass
    for text in USER_REGEX.finditer(msg):
        try:
            data['users'].append(text.group(0).replace('@',''))
        except IndexError:
            pass

    return data

