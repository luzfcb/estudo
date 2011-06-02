#!/usr/bin/python
import StringIO
from translate.storage import po
from django.utils import simplejson
import sys, os, re, urllib
from htmlentitydefs import name2codepoint


 
def htmldecode(text):
        """Decode HTML entities in the given text."""
        if type(text) is unicode:
                uchr = unichr
        else:
                uchr = lambda value: value > 255 and unichr(value) or chr(value)
        def entitydecode(match, uchr=uchr):
                entity = match.group(1)
                if entity.startswith('#x'):
                        return uchr(int(entity[2:], 16))
                elif entity.startswith('#'):
                        return uchr(int(entity[1:]))
                elif entity in name2codepoint:
                        return uchr(name2codepoint[entity])
                else:
                        return match.group(0)
        charrefpat = re.compile(r'&(#(\d+|x[\da-fA-F]+)|[\w.:-]+);?')
        return charrefpat.sub(entitydecode, text)

def get_translation(sl, tl, text):
    """
    Response is in the format
   '{"responseData": {"translatedText":"Ciao mondo"}, "responseDetails": null, "responseStatus": 200}''' 
    """
    if text.startswith('"'): text = text[1:-1]
    params = {'v':'1.0', 'q': text.encode('utf-8')}
    try:
        result = simplejson.load(urllib.urlopen('http://ajax.googleapis.com/ajax/services/language/translate?%s&langpair=%s%%7C%s' % (urllib.urlencode(params), sl, tl)))
    except IOError, e:
        print e
        return ""
    else:
        try:
            status = result['responseStatus']
        except KeyError:
            status = -1
        if status == 200:
            return result['responseData']['translatedText']
        else:
            print "Error %s: Translating string %s" % (status, text)
            return ""

def translate_po(file, sl, tl):
    openfile = po.pofile(open(file))
    nb_elem = len(openfile.units)
    moves = 1
    cur_elem = 0
    for unit in  openfile.units:
        # report progress
        cur_elem += 1
        s = "\r%f %% - (%d msg processed out of %d) " \
            % (100 * float(cur_elem) / float(nb_elem), cur_elem, nb_elem)
        sys.stderr.write(s)
        if not unit.isheader():
            if len(unit.msgid):
                if unit.msgstr==[u'""']:
                    moves += 1
                    unit.msgstr = ['"%s"' % htmldecode(get_translation(sl, tl, x)) for x in unit.msgid ]
        if not bool(moves % 50):
            print "Saving file..."
            openfile.save()
    openfile.save()


def translate_all(from_lang):

        #create file-like string to capture output
        codeOut = StringIO.StringIO()
        codeErr = StringIO.StringIO()

        ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
        if not os.path.exists(os.path.join(ROOT_DIR, 'locale')):
            os.mkdir(os.path.join(ROOT_DIR, 'locale'))
            command = os.path.join(ROOT_DIR, 'manage.py makemessages -l en pt-br es')
            print command
            # capture output and errors
            sys.stdout = codeOut
            sys.stderr = codeErr

            exec 'python '.command

            # todo
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            s = codeErr.getvalue()

            print "error:\n%s\n" % s

            s = codeOut.getvalue()

            print "output:\n%s" % s

            codeOut.close()
            codeErr.close()


            

        LOCALE_PATH = os.path.join(ROOT_DIR, 'locale')
        for language in os.listdir(LOCALE_PATH):

            print('language = %s', language)
            
            lang_path = os.path.join(LOCALE_PATH, language)
            print('lang_path = %s', language)

            lang_LC_MESSAGES = os.path.join(lang_path , 'LC_MESSAGES')
            print('lang_LC_MESSAGES = %s', lang_LC_MESSAGES)


            file_lang_path = os.path.join(lang_LC_MESSAGES, 'django.po')
            print('file_lang_path = %s', file_lang_path)

            print('Translating %s, from %s to %s' %(file_lang_path, from_lang, language))
            translate_po(file_lang_path , from_lang, language)

#        in_pofile = os.path.abspath(sys.argv[1])
#        from_lang = sys.argv[2]
#        to_lang = sys.argv[3]
#        print('Translating %s to %s' %(from_lang,  to_lang))
#        translate_po(in_pofile, from_lang, to_lang)
#        print('Translation done')

if __name__ == "__main__":

#    if len(sys.argv) < 4 or \
#       not os.path.exists(sys.argv[1]):
#        sys.stderr.write("""
#utilizacao : python autotranslate.py arquivo.po linguagem_origem linguagem_destino
#exemplo de utilizacao: python autotranslate.py django.po pt en
#""")
#        sys.exit(1)
#    else:
#

        translate_all(sys.argv[2])
