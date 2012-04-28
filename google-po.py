#!/usr/bin/python
import sys
import pprint
from httplib import HTTPConnection
import urllib2
'''
Usage:
   thisfile.py django.po django2.po
   :django.po: input file
   :django2.po: output file
'''
def translate(msg):
    http = HTTPConnection('translate.google.cn')
    http.request('GET','/translate_a/t?client=t&text=%s&hl=en&sl=auto&tl=zh-CN&multires=1&otf=1&ssel=0&tsel=6&uptl=en&alttl=zh-CN&sc=1' % urllib2.quote(msg),
                headers={'user-agent': 'Mozilla/5.0 (X11; Linux i686; rv:11.0) Gecko/20100101 Firefox/11.0'})
    resp = http.getresponse()
    transed = resp.read()
    return transed.split(',')[0].strip('[').strip('"')

if __name__ == '__main__':
    input = sys.argv[1]
    output = sys.argv[2]
    
    newlines = []
    toTrans = ''
    fuzzy = False
    for line in file(input).readlines():
        if line.startswith('#, fuzzy'):
            fuzzy = True
        elif line.startswith('msgid'):
            toTrans = line[len('msgid '):].strip().strip('"')
            newlines.append(line)
        elif line.startswith('msgstr'):   
            if fuzzy :
                transed = translate(toTrans)
                newlines.append('msgstr "%s"' % transed)
                fuzzy = False
            elif line[len('msgstr '):].strip().strip('"') == '':
                transed = translate(toTrans)
                newlines.append('msgstr "%s"' % transed)
            else:
                newlines.append(line)
        else:
            newlines.append(line)
        sys.stdout.write('.')
        sys.stdout.flush()
    open(output, 'w+').writelines(newlines)
     
            
