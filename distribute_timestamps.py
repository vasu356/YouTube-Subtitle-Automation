"""
Timestamp distribution module.

Given a Whisper segment (which has a single start/end timestamp for a
potentially long phrase) and a list of word chunks derived from it,
this module distributes the segment's duration across the chunks
proportionally by word count.

This is a best-effort approximation — Whisper's segment-level timestamps
don't carry per-word timing when word_timestamps=False. The proportional
distribution produces smooth, readable subtitles in practice.
"""


def distribute_timestamps(segment: dict, chunks: list[str]) -> list[dict]:
    """
    Distribute a Whisper segment's time range across a list of text chunks.

    Each chunk receives a slice of the total segment duration, proportional
    to its word count relative to all words across all chunks combined.
    This ensures longer chunks stay on screen longer, and shorter ones
    appear and disappear faster — matching natural reading pace.

    Args:
        segment: A Whisper segment dict with keys:
                   - 'text'  (str)   : Full text of the segment.
                   - 'start' (float) : Start time in seconds.
                   - 'end'   (float) : End time in seconds.
        chunks:  List of text strings to assign timestamps to.
                 Typically produced by split_into_chunks().

    Returns:
        A list of dicts, one per chunk, each with:
            - 'text'  (str)   : The chunk text.
            - 'start' (float) : Start time in seconds.
            - 'end'   (float) : End time in seconds.
        Returns an empty list if `chunks` is empty.

    Example:
        >>> seg = {"text": "hello world foo bar", "start": 0.0, "end": 4.0}
        >>> chunks = ["hello world", "foo bar"]
        >>> distribute_timestamps(seg, chunks)
        [{'text': 'hello world', 'start': 0.0, 'end': 2.0},
         {'text': 'foo bar',     'start': 2.0, 'end': 4.0}]
    """
    if not chunks:
        return []

    total_duration = segment["end"] - segment["start"]
    words_per_chunk = [len(chunk.split()) for chunk in chunks]
    total_words = sum(words_per_chunk)

    # Guard against a zero-word edge case (shouldn't happen after split, but be safe)
    if total_words == 0:
        equal_duration = total_duration / len(chunks)
        result = []
        current_time = segment["start"]
        for chunk in chunks:
            result.append({
                "text":  chunk,
                "start": current_time,
                "end":   current_time + equal_duration,
            })
            current_time += equal_duration
        return result

    result = []
    current_time = segment["start"]

    for chunk, word_count in zip(chunks, words_per_chunk):
        chunk_duration = (word_count / total_words) * total_duration
        end_time = current_time + chunk_duration
        result.append({"text": chunk, "start": current_time, "end": end_time})
        current_time = end_time

    return result
