from part_1_solution import (
    get_datastream,
    get_start_of_packet_marker_index
)

if __name__ == '__main__':
    _MARKER_LEN = 14
    datastream = get_datastream()
    print(get_start_of_packet_marker_index(datastream, _MARKER_LEN))
