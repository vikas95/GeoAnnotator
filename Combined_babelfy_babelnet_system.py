# import urllib2
import ssl
import urllib
import urllib.parse
from urllib.request import urlopen
import urllib.request
import json
import gzip
from BabelNet_BabelFy_functions import babelfy_entities, babelNet

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO, BytesIO

service_url = 'https://babelfy.io/v1/disambiguate'

text = 'February and April 2017, about 4.9 million people, over 40 percent of total population, are estimated to be severely food insecure and this figure is projected to reach 5.5 million people at the peak of the lean season in July. Although most food insecure ' \
       'people are concentrated in the Greater Upper Nile region, food security has drastically deteriorated in former Northern Bahr el Ghazal State and the Greater Equatoria Region.'
lang = 'EN'
key  = 'KEY'


text = ""
text_file=open("Test_small_V1.txt","r")
out_file=open("Babelfy_Babelnet_output.txt","w")
for line in text_file:
    words=line.strip().split()
    if len(words)>0:
       text += words[0] + " "
    else:
       entities = babelfy_entities(text, lang, key)
       all_words=text.split()
       index=0
       print ("why the hell are we getting ",entities)
       for ind, entity_ind in enumerate(entities):
           while index < entity_ind[0]:
                 out_file.write(all_words[index]+" " + "O" +"\n")
                 index+=1
           entity_name = ""
           for ent_ind in entity_ind:
               index+=1
               entity_name += all_words[ent_ind]
               entity_name+=" "
           entity_name+="LOCATION" + "\n"
           out_file.write(entity_name)

       out_file.write("\n")
       text=""


"""
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
                ind_entity = []
                if tfStart != tfEnd:
                    ind_entity.append(tfStart)
                    ind_entity.append(tfEnd)
                entity_ids.append(ind_entity)




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
"""

