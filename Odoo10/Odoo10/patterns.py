
def _clamp(v, minv, maxv):
    return min(max(v, minv), maxv)


def _longest_common_prefix(lhs, rhs):
    i = 0
    for i in range(0, min(len(lhs), len(rhs))):
        if lhs[i] != rhs[i]: break
    else:
        i = i + 1
    return tuple(lhs[:i])

def startswith(full, prefix):
    if len(full) < len(prefix): 
        return False
    for i in range(0, len(prefix)):
        if prefix[i] != full[i]: 
            return False
    return True

def _make_suffix_array(string):
    suffix_array = [i for i in range(0, len(string))]
    def suffix_key(i):
        return string[i:]
    suffix_array.sort(key=suffix_key)
    return suffix_array

def find_repetitions(string, minl):
    minl = _clamp(minl, 2, len(string) // 2)
    suffix_array = _make_suffix_array(string)

    patterns = {}
    for w_idx in range(0, len(suffix_array) - 1):
        word = _longest_common_prefix(string[suffix_array[w_idx]:], string[suffix_array[w_idx+1]:])
        if len(word) < minl or word in patterns: continue

        patterns[word] = 1

        c_idx = w_idx - 1
        while c_idx >= 0 and startswith(string[ suffix_array[c_idx]: ], word):
            c_idx = c_idx - 1
            patterns[word] = patterns[word] + 1

        c_idx = w_idx + 1
        while c_idx < len(suffix_array) and startswith(string[ suffix_array[c_idx]: ], word):
            c_idx = c_idx + 1
            patterns[word] = patterns[word] + 1

    return patterns

print(find_repetitions([1,1,1,1,1,1,1,1,1], 2))
