import sublime
import json
import os

def _is_ST2():
    return (int(sublime.version()) < 3000)

if _is_ST2():
    from urllib import urlencode
    from urllib import urlopen
else:
    try:
        from urlparse import urlencode
        from urllib2 import urlopen
    except ImportError:
        from urllib.parse import urlencode
        from urllib.request import urlopen

def getResponse(server, text, language, disabledRules, credentialsFile):
    payload = {
        'language': language,
        'text': text.encode('utf8'),
        'preferredVariants': 'en-GB,pt-BR',
        'disabledRules': ','.join(disabledRules),
        'enabledOnly': 'false'
    }
    server, payload = _getCredentials(server, payload, credentialsFile)
    content = _post(server, payload)
    if content:
        j = json.loads(content.decode('utf-8'))
        print(j["software"])
        return j['matches']
    else:
        return None

# internal functions:

def _getCredentials(server, payload, credentialsFile):
    if os.path.exists(credentialsFile):
        credentials = json.load(open(credentialsFile, 'r'))
        payload['username'] = credentials['username']
        payload['apiKey'] = credentials['apiKey']
        server = credentials['url']
    return server, payload

def _post(server, payload):
    data = urlencode(payload).encode('utf8')
    try:
        content = urlopen(server, data).read()
        return content
    except IOError:
        return None
