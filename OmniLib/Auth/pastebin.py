# Using pastebin instead of smtp
import httplib, urllib

def post_it(msg):    
    # private and expires in 2 mins, still not as secure as email obviously...
    params = urllib.urlencode({'paste_code': msg, 'paste_expire_date': '2M', 'paste_private': '1'})
    url = urllib.urlopen("http://pastebin.com/api_public.php", params)
    return url.read() # returns the url of the link
