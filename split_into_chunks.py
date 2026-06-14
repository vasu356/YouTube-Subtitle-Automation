"""
Text chunking module.

Splits a transcribed text string into smaller chunks suitable for
display as subtitle cards. Keeping chunks short (3–5 words) improves
readability, especially for fast-paced or densely-spoken audio.
"""


def split_into_chunks(text: str, max_words: int = 4) -> list[str]:
    """
    Split a string of text into chunks of at most `max_words` words.

    Args:
        text:      The input text to chunk (e.g. a Whisper segment's transcription).
        max_words: Maximum number of words per chunk. Must be >= 1. (default: 4)

    Returns:
        A list of non-empty string chunks. Returns an empty list if the
        input text is blank.

    Example:
        >>> split_into_chunks("The quick brown fox jumps over the lazy dog", max_words=4)
        ['The quick brown fox', 'jumps over the lazy', 'dog']
    """
    if not text or not text.strip():
        return []

    if max_words < 1:
        raise ValueError(f"max_words must be >= 1, got {max_words}")

    words = text.split()
    return [" ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)]
