# import urllib2
import ssl
import urllib
import urllib.parse
from urllib.request import urlopen
import urllib.request
import json
import gzip

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO, BytesIO

service_url = 'https://babelfy.io/v1/disambiguate'

lang = 'EN'
key  = 'KEY'


def babelfy_entities(text, lang, key):
    params = {
        'text' : text,
        'lang' : lang,
        'key'  : key
    }

    url = service_url + '?' + urllib.parse.urlencode(params)
    # request = urllib2.Request(url)
    request = urllib.request.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    # response = urlopen(url, context=gcontext)

    response=urlopen(request, context=gcontext)
    entity_ids=[]
    if response.info().get('Content-Encoding') == 'gzip':
        # print ("we are here")
        buf = BytesIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = json.loads(f.read())

        # retrieving data
        for result in data:
            # retrieving token fragment
            tokenFragment = result.get('tokenFragment')
            tfStart = tokenFragment.get('start')
            tfEnd = tokenFragment.get('end')
            # print (str(tfStart) + "\t" + str(tfEnd))

        # retrieving char fragment
            charFragment = result.get('charFragment')
            cfStart = charFragment.get('start')
            cfEnd = charFragment.get('end')
            # print (str(cfStart) + "\t" + str(cfEnd))
            # print (str(cfStart) + "\t" + str(cfEnd)+ "\t" +text[cfStart:cfEnd+1])
            ent_word=text[cfStart:cfEnd+1]
            # retrieving BabelSynset ID
            synsetId = result.get('babelSynsetID')

            type=babelNet(synsetId, ent_word)

            if type == "GEONM":
                print ("we are not able to reach here")
                ind_entity = []
                if tfStart != tfEnd:
                    print ("this is for multi-word entity...")
                    ind_entity.append(tfStart)
                    ind_entity.append(tfEnd)
                else:
                    ind_entity.append(tfStart)
                entity_ids.append(ind_entity)
    return entity_ids



                # print (synsetId)


def babelNet(syset_ID, word):
    service_url = 'https://babelnet.io/v5/getSenses'

    lemma = word
    syn_id = str(syset_ID)
    lang = 'EN'
    key = 'f49269e8-4de9-44b9-9259-f9cad5544413'

    params = {
        'lemma': lemma,
        'id': syn_id, #"bn:02987985n",
        'searchLang': lang,
        'key': key
    }

    # url = service_url + '?' + urllib.urlencode(params)
    url = service_url + '?' + urllib.parse.urlencode(params)
    # request = urllib2.Request(url)
    request = urllib.request.Request(url)
    request.add_header('Accept-encoding', 'gzip')

    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    # response = urllib2.urlopen(request)
    response = urlopen(request, context=gcontext)

    if response.info().get('Content-Encoding') == 'gzip':
        # buf = StringIO(response.read())
        buf = BytesIO(response.read())

        f = gzip.GzipFile(fileobj=buf)
        data = json.loads(f.read())
        print (data[0]['properties']['source'])

        # retrieving BabelSense data
        for result in data:
            # lemma = result.get('lemma')
            # language = result.get('language')
            source = result.get('source')
            # print (str(source))
        return data[0]['properties']['source']