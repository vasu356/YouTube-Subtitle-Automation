def distribute_timestamps(segment, chunks):
    """
    Distribute the segment's duration across chunks proportionally by word count.
    """
    total_duration = segment["end"] - segment["start"]
    total_words = len(segment["text"].split())
    words_per_chunk = [len(chunk.split()) for chunk in chunks]
    total_words_in_chunks = sum(words_per_chunk)

    chunk_durations = [(words / total_words_in_chunks) * total_duration for words in words_per_chunk]
    chunk_timestamps = []
    current_time = segment["start"]

    for duration, chunk in zip(chunk_durations, chunks):
        end_time = current_time + duration
        chunk_timestamps.append({"text": chunk, "start": current_time, "end": end_time})
        current_time = end_time

    return chunk_timestamps