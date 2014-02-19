import re


re_status = re.compile(r'marker\-(\w+)\.png')
re_point = re.compile(r'LatLng.([\d.-]+), ([\d.-]+)\)')


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.

    http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def convert_raw_data(lines):
    # assert len(lines) == 6
    status = re_status.search(lines[0]).group(1)
    lat, lng = re_point.search(lines[2]).groups()
    return {
        'status': status,
        'latitude': lat,
        'longitude': lng,
    }


def find_data(text):
    # trim text
    start = text.index('var icon')
    text = text[start:]
    end = text.index('}')
    lines = text[:end].strip().split('\n')
    return map(convert_raw_data, chunks(lines, 6))
