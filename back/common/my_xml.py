import json

import xmltodict


def xml_to_dict(xml_str):
    data_orderedD = xmltodict.parse(xml_str)
    return json.loads(json.dumps(data_orderedD, indent=4))


def dicttoxml(dict_data):
    return xmltodict.unparse(dict_data, pretty=True, encoding='utf-8')


if __name__ == '__main__':
    # obj=XmlDict(moviesFilePath)
    xml_string = """
    <xml>
<appid>wxd930ea5d5a258f4f</appid>
<mch_id>10000100</mch_id>
<device_info>1000</device_info>
<body>test</body>
<nonce_str>ibuaiVcKdpRxkhJA</nonce_str>
<sign>9A0A8659F005D6984697E2CA0A9CF3B7</sign>
</xml>"""

    print(xml_to_dict(xml_string))
    print(dicttoxml({"nihao": {"ty": "leixing", "fuoran": "feichang"}}))
