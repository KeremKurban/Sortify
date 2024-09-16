import random

def merge_sort(songs, comparisons):
    if len(songs) <= 1:
        return songs

    mid = len(songs) // 2
    left = merge_sort(songs[:mid], comparisons)
    right = merge_sort(songs[mid:], comparisons)

    if left is None or right is None:
        return None

    return merge(left, right, comparisons)

def merge(left, right, comparisons):
    result = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        comparison_key = f"{left[i]['id']}:{right[j]['id']}"
        if comparison_key in comparisons:
            if comparisons[comparison_key] == left[i]['id']:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            # If we don't have a comparison, we'll need to ask the user
            return None

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def get_next_comparison(songs, comparisons):
    if len(songs) <= 1:
        return None, None

    remaining_comparisons = [
        (songs[i], songs[j])
        for i in range(len(songs))
        for j in range(i + 1, len(songs))
        if f"{songs[i]['id']}:{songs[j]['id']}" not in comparisons
    ]

    if not remaining_comparisons:
        return None, None

    song1, song2 = random.choice(remaining_comparisons)
    print(f"Next comparison: {song1['id']} vs {song2['id']}")  # Debug print
    return song1, song2