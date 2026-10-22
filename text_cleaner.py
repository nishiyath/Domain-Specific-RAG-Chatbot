import re


def clean_text(text):
    # Replace repeated spaces and line breaks with one space
    text = re.sub(r"\s+", " ", text)

    # Remove spaces at the beginning and end
    text = text.strip()

    return text
