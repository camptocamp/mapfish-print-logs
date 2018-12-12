PAGE_SIZE2NAME = {
    # taken from https://github.com/itext/itextpdf/blob/develop/itext/src/main/java/com/itextpdf/text/PageSize.java
    '420x595': 'A5',
    '595x842': 'A4',
    '842x1191': 'A3',
    '1191x1684': 'A2',
    '1684x2384': 'A1',
    '2384x3370': 'A0',

    '498x708': 'B5',
    '708x1000': 'B4',
    '1000x1417': 'B3',
    '1417x2004': 'B2',
    '2004x2834': 'B1',
    '2834x4008': 'B0',

    '283x416': 'Postcard',
    '522x756': 'Executive',
    '540x720': 'Note',
    '612x792': 'Letter',
    '612x1008': 'Legal',
    '792x1224': 'Tabloid'
}


def page_size2fullname(dico):
    height = str(dico['height'])
    width = str(dico['width'])
    size = 'x'.join(sorted([width, height]))
    return PAGE_SIZE2NAME.get(size, size) + \
        (' portrait' if height > width else ' landscape')


def page_size2name(dico):
    height = str(dico['height'])
    width = str(dico['width'])
    size = 'x'.join(sorted([width, height]))
    return PAGE_SIZE2NAME.get(size, size)


def quote_like(text):
    return text.replace("%", r"\%").replace("_", r"\_")
