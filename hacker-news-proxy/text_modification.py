import re


def add_trademark(content):
    # Добавление символа "™" только после слов из шести буквенных символов, которые не следуют непосредственно за знаком пунктуации
    modified_content = re.sub(r'(?<!\W)\b[A-Za-z]{6}\b', r'\g<0>™', content)
    return modified_content
