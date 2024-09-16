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

def get_next_comparison(songs):
    if len(songs) <= 1:
        return None, None

    mid = len(songs) // 2
    return songs[0], songs[mid]