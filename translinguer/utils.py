
class ProxyDict:
    def __getitem__(self, key):
        return key


def dict_get(d, key):
    result = d.get(key, {})
    d[key] = result
    return result


def dict_get_reversed(d, key):
    if isinstance(d, dict):
        if not hasattr(d, '__reversed_dict'):
            d.__reversed_dict = {value: key for key, value in d.items()}
        return d.__reversed_dict[key]
    elif isinstance(d, ProxyDict):
        return key
    else:
        raise ValueError(f'Unknown lang_mapper type: {d}')
