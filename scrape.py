import re
from lxml.html import fragment_fromstring


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
    html = lines[4][lines[4].index('"') + 1: lines[4].rindex('"')]
    doc = fragment_fromstring('<div>{}</div>'.format(html))
    location_bit = doc.xpath('//div[@class="location"]')[0]
    location_bits = location_bit.xpath('.//text()')
    if len(location_bits) == 4:
        name, street, city, zip = location_bits
    else:
        # XXX untested
        name, street, city_zip = location_bits
        city, zip = city_zip.split(', ', 2)
    avail = doc.xpath('//div[@class="avail"]/strong/text()')
    return {
        'status': status,
        'latitude': lat,
        'longitude': lng,
        'name': name,
        'street': street,
        'city': city,
        'state_zip': zip,
        'bikes': int(avail[0]),
        'docks': int(avail[1]),
    }


def find_data(text):
    # trim text
    start = text.index('var icon')
    text = text[start:]
    end = text.index('}')
    lines = text[:end].strip().split('\n')
    return map(convert_raw_data, chunks(lines, 6))
