def get_datastream() -> str:
    with open('input.txt') as f:
        return f.read()


def has_duplicate(s: str):
    return len(s) == len(set(s))



def get_start_of_packet_marker_index(datastream: str, marker_len: int) -> int:
    for i in range(marker_len-1, len(datastream)):
        if has_duplicate(datastream[i-(marker_len-1):i+1]):
            print(f'marker: {datastream[i-(marker_len-1):i+1]}')
            return i+1
    raise Exception(f'No start of packet marker found in {datastream}')


if __name__ == '__main__':
    _MARKER_LEN = 4
    assert get_start_of_packet_marker_index('nppdvjthqldpwncqszvftbrmjlhg', _MARKER_LEN) == 6
    datastream = get_datastream()
    print(get_start_of_packet_marker_index(datastream, _MARKER_LEN))