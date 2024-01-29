import emoji


def convert_emoji_to_text(emoji_text):
    text_with_aliases = emoji.demojize(emoji_text)
    return text_with_aliases


if __name__ == "__main__":
    emoji_text = "I love Python! 😍🐍✌🏻"
    converted_text = convert_emoji_to_text(emoji_text)
    print("Original Text:", emoji_text)
    print("Converted Text:", converted_text)
