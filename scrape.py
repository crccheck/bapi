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
    # status can be: active/specialevent/partialservice/outofservice/comingsoon
    status = re_status.search(lines[0]).group(1)
    lat, lng = re_point.search(lines[2]).groups()
    html = lines[4][lines[4].index('"') + 1: lines[4].rindex('"')]
    doc = fragment_fromstring('<div>{}</div>'.format(html))
    name = doc.xpath('./div[@class="markerTitle"]/h3/text()')[0]
    street, city_zip = doc.xpath('./div[@class="markerAddress"]/text()')
    city, zip = city_zip.split(', ')
    bikes, docks = doc.xpath('//div[@class="markerAvail"]//h3/text()')
    return {
        'status': status,
        'latitude': lat,
        'longitude': lng,
        'name': name,
        'street': street,
        'city': city,
        'state_zip': zip,
        'bikes': int(bikes),
        'docks': int(docks),
    }


def find_data(text):
    # trim text
    start = text.index('var icon')
    text = text[start:]
    end = text.index('}')
    lines = text[:end].strip().split('\n')
    return map(convert_raw_data, chunks(lines, 6))
