def split_into_chunks(text, max_words=4):
    """
    Split text into chunks of 3-4 words maximum.
    """
    words = text.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
