
import collections

def _clamp(v, minv, maxv):
    return min(max(v, minv), maxv)


def _longest_common_prefix(lhs, rhs):
    i = 0
    for i in range(0, min(len(lhs), len(rhs))):
        if lhs[i] != rhs[i]: break
    else:
        i += 1
    if isinstance(lhs, collections.Hashable):
        return lhs[:i]
    else:
        return tuple(lhs[:i])


def _make_suffix_array(string):
    suffix_array = [i for i in range(0, len(string))]

    def suffix_array_f(idx):
        return string[idx:]
    suffix_array.sort(key=suffix_array_f)

    return suffix_array_f, len(suffix_array)


def _starts_with(full, prefix):
    if len(full) < len(prefix): return False

    for i in range(0, len(prefix)):
        if full[i] != prefix[i]:
            return False

    return True



def find_repetitions(string, minl):
    minl = _clamp(minl, 2, max(2, len(string) // 2))
    suffix_array, len_suffix_array = _make_suffix_array(string)

    patterns = {}
    for w_idx in range(0, len_suffix_array - 1):
        word = _longest_common_prefix(suffix_array(w_idx), suffix_array(w_idx+1))
        if len(word) < minl or word in patterns: continue

        patterns[word] = 1

        c_idx = w_idx - 1
        while c_idx >= 0 and _starts_with(suffix_array(c_idx), word):
            c_idx -= 1
            patterns[word] += 1

        c_idx = w_idx + 1
        while c_idx < len_suffix_array and _starts_with(suffix_array(c_idx), word):
            c_idx += 1
            patterns[word] += 1

    return patterns


