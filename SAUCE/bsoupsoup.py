from bs4 import BeautifulSoup as bsoup
import re
import optim_selena
import json
from pprint import pprint


# ill try polymorphism


def tag_text(obj, hpat, element, flag=''):
    if flag == 'tags':
        fList = []
        data = obj.find_all(element, href=re.compile(hpat))
        for iterable in data:
            lTag = iterable.text.strip().lower()
            if lTag == 'tags':
                continue
            fList.append(lTag)
        return fList
    if flag == 'author':
        data = obj.find(element, href=re.compile(hpat))
        return data.text.strip()
    if flag == 'description':
        data = obj.find(element, property=hpat)
        return data['content'].strip()
    if flag == 'title':
        data = obj.find(element, property=hpat)
        return data['content'].strip()
    if flag == 'url':
        data = obj.find(element, property=hpat)
        return data['content'].strip()


# def tag_text(obj, hpat, element='a', author=False):
#     if author:
#         data = obj.find(element, href= re.compile(hpat))
#     return data.text.strip()


# def tag_text(obj,hpat, element = 'meta', description=False):
#     if description:
#         data = obj.find(element, property=hpat)
#     return data['content'].strip()


# def tag_text(obj, hpat, element='meta', title=False):
#     if title:
#         data = obj.find(element, property=hpat)
#     return data['content'].strip()


# def tag_text(obj, hpat, element='meta', url=False):
#     if url:
#         data = obj.find(element, property=hpat)
#     return data['content'].strip()

def jsonextract(obj, patdic, dname=''):
    """
    The parser will spit out dictionary with the following properties:
     NAME,
     TAGS,
      DESCRIPTION,
      AUTHOR,
      ARTIST,
      status=0.note

    """

    meta = {}
    linkElem = 'a'
    metaElem = 'meta'

    meta['title'] = tag_text(obj, patdic['title'], metaElem, flag='title')
    meta['author'] = tag_text(obj, patdic['author'], linkElem, flag='author')
    meta['url'] = tag_text(obj, patdic['url'], metaElem, flag='url')
    meta['description'] = tag_text(obj, patdic['description'], metaElem, flag='description')
    meta['tags'] = tag_text(obj, patdic['tags'], linkElem, flag='tags')
    return meta


def Emetadata(doujname):
    hrefPat = {"tags": "/tags/*",
               "artist": "/artists/*",
               "author": "/artists/*",
               "title": "og:title",
               "description": "og:description",
               "url": "og:url"}

    out = optim_selena.htmlParse(doujname)
    fakkuHtml, url = out
    metadata = {}
    tags = []


    print(f'Looking for metadata: {doujname} in {url}')
    doc = bsoup(fakkuHtml, "html.parser")

    # # will only search for href
    try:
        metadata = jsonextract(doc, hrefPat)
    except:
        None
        print(f'[FAILED]{doujname} could not be parsed. Reason: 404 return')
        # will occur when the entry can't be found in fakku

    return metadata


if __name__ == '__main__':
    pprint(Emetadata("Size Complex"))
    # pprint(Emetadata('There\'s a Reason It\'s Out of Service'))
