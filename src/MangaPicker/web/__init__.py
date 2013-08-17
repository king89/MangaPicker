#### MangaPicker | WEB #################################################################################
# Copyright (c) 2012 
# Author: Qingzhong Liang
# License: BSD (see LICENSE.txt for details).
# 

####################################################################################################
# Python API interface for  web services


import threading
import time
import os
import socket, urlparse, urllib, urllib2
import base64


try:
    MODULE = os.path.dirname(os.path.abspath(__file__))
except:
    MODULE = ""



#### UNICODE #######################################################################################

def decode_utf8(string):
    """ Returns the given string as a unicode string (if possible).
    """
    if isinstance(string, str):
        for encoding in (("utf-8",), ("windows-1252",), ("utf-8", "ignore")):
            try: 
                return string.decode(*encoding)
            except:
                pass
        return string
    return unicode(string)
    
def encode_utf8(string):
    """ Returns the given string as a Python byte string (if possible).
    """
    if isinstance(string, unicode):
        try: 
            return string.encode("utf-8")
        except:
            return string
    return str(string)

u = decode_utf8
s = encode_utf8

# For clearer source code:
bytestring = s

#### ASYNCHRONOUS REQUEST ##########################################################################

class AsynchronousRequest:
    
    def __init__(self, function, *args, **kwargs):
        """ Executes the function in the background.
            AsynchronousRequest.done is False as long as it is busy, but the program will not halt in the meantime.
            AsynchronousRequest.value contains the function's return value once done.
            AsynchronousRequest.error contains the Exception raised by an erronous function.
            For example, this is useful for running live web requests while keeping an animation running.
            For good reasons, there is no way to interrupt a background process (i.e. Python thread).
            You are responsible for ensuring that the given function doesn't hang.
        """
        self._response = None  # The return value of the given function.
        self._error = None  # The exception (if any) raised by the function.
        self._time = time.time()
        self._function = function
        self._thread = threading.Thread(target=self._fetch, args=(function,) + args, kwargs=kwargs)
        self._thread.start()
        
    def _fetch(self, function, *args, **kwargs):
        """ Executes the function and sets AsynchronousRequest.response.
        """
        try: 
            self._response = function(*args, **kwargs)
        except Exception, e:
            self._error = e

    def now(self):
        """ Waits for the function to finish and yields its return value.
        """
        self._thread.join(); return self._response

    @property
    def elapsed(self):
        return time.time() - self._time
    @property
    def done(self):
        return not self._thread.isAlive()
    @property
    def value(self):
        return self._response
    @property
    def error(self):
        return self._error
        
    def __repr__(self):
        return "AsynchronousRequest(function='%s')" % self._function.__name__

def asynchronous(function, *args, **kwargs):
    """ Returns an AsynchronousRequest object for the given function.
    """
    return AsynchronousRequest(function, *args, **kwargs)
    
send = asynchronous

#### URL ###########################################################################################

# User agent and referrer.
# Used to identify the application accessing the web.
USER_AGENT = ""
REFERRER = ""

# Mozilla user agent.
# Websites can include code to block out any application except browsers.
MOZILLA = "Mozilla/5.0"

# HTTP request method.
GET = "get"  # Data is encoded in the URL.
POST = "post"  # Data is encoded in the message body.

# URL parts.
# protocol://username:password@domain:port/path/page?query_string#anchor
PROTOCOL, USERNAME, PASSWORD, DOMAIN, PORT, PATH, PAGE, QUERY, ANCHOR = \
    "protocol", "username", "password", "domain", "port", "path", "page", "query", "anchor"

# MIME type.
MIMETYPE_WEBPAGE = ["text/html"]
MIMETYPE_STYLESHEET = ["text/css"]
MIMETYPE_PLAINTEXT = ["text/plain"]
MIMETYPE_PDF = ["application/pdf"]
MIMETYPE_NEWSFEED = ["application/rss+xml", "application/atom+xml"]
MIMETYPE_IMAGE = ["image/gif", "image/jpeg", "image/png", "image/tiff"]
MIMETYPE_AUDIO = ["audio/mpeg", "audio/mp4", "audio/x-aiff", "audio/x-wav"]
MIMETYPE_VIDEO = ["video/mpeg", "video/mp4", "video/quicktime"]
MIMETYPE_ARCHIVE = ["application/x-stuffit", "application/x-tar", "application/zip"]
MIMETYPE_SCRIPT = ["application/javascript", "application/ecmascript"]

def extension(filename):
    """ Returns the extension in the given filename: "cat.jpg" => ".jpg".
    """
    return os.path.splitext(filename)[1]

def urldecode(query):
    """ Inverse operation of urllib.urlencode.
        Returns a dictionary of (name, value)-items from a URL query string.
    """
    def _format(s):
        if s == "None":
            return None
        if s.isdigit(): 
            return int(s)
        try: 
            return float(s)
        except: return s
    query = [(kv.split("=") + [None])[:2] for kv in query.lstrip("?").split("&")]
    query = [(urllib.unquote_plus(bytestring(k)), urllib.unquote_plus(bytestring(v))) for k, v in query]
    query = [(u(k), u(v)) for k, v in query]
    query = [(k, _format(v) or None) for k, v in query]
    query = dict([(k, v) for k, v in query if k != ""])
    return query
    
url_decode = urldecode

def proxy(host, protocol="https"):
    """ Returns the value for the URL.open() proxy parameter.
        - host: host address of the proxy server.
    """
    return (host, protocol)

class URLError(Exception):
    pass  # URL contains errors (e.g. a missing t in htp://).
class URLTimeout(URLError):
    pass  # URL takes to long to load.
class HTTPError(URLError):
    pass  # URL causes an error on the contacted server.
class HTTP301Redirect(HTTPError):
    pass 
class URLTimeoutError:
    pass
# Too many redirects.
# The site may be trying to set a cookie and waiting for you to return it,
# or taking other measures to discern a browser from a script.
# For specific purposes you should build your own urllib2.HTTPRedirectHandler
# and pass it to urllib2.build_opener() in URL.open()

class HTTP400BadRequest(HTTPError):
    pass  # URL contains an invalid request.
class HTTP401Authentication(HTTPError):
    pass  # URL requires a login and password.
class HTTP403Forbidden(HTTPError):
    pass  # URL is not accessible (user-agent?)
class HTTP404NotFound(HTTPError):
    pass  # URL doesn't exist on the internet.
class HTTP420Error(HTTPError):
    pass  # Used by Twitter for rate limiting.
class HTTP500InternalServerError(HTTPError):
    pass  # Generic server error.
    
    
class URL:
    
    def __init__(self, string=u"", method=GET, query={}):
        """ URL object with the individual parts available as attributes:
            For protocol://username:password@domain:port/path/page?query_string#anchor:
            - URL.protocol: http, https, ftp, ...
            - URL.username: username for restricted domains.
            - URL.password: password for restricted domains.
            - URL.domain  : the domain name, e.g. nodebox.net.
            - URL.port    : the server port to connect to.
            - URL.path    : the server path of folders, as a list, e.g. ['news', '2010']
            - URL.page    : the page name, e.g. page.html.
            - URL.query   : the query string as a dictionary of (name, value)-items.
            - URL.anchor  : the page anchor.
            If method is POST, the query string is sent with HTTP POST.
        """
        self.__dict__["method"] = method  # Use __dict__ directly since __setattr__ is overridden.
        self.__dict__["_string"] = u(string)
        self.__dict__["_parts"] = None
        self.__dict__["_headers"] = None
        self.__dict__["_redirect"] = None
        if isinstance(string, URL):
            self.__dict__["method"] = string.method
            self.query.update(string.query)
        if len(query) > 0:
            # Requires that we parse the string first (see URL.__setattr__).
            self.query.update(query)
        
    def _parse(self):
        """ Parses all the parts of the URL string to a dictionary.
            URL format: protocal://username:password@domain:port/path/page?querystring#anchor
            For example: http://user:pass@example.com:992/animal/bird?species=seagull&q#wings
            This is a cached method that is only invoked when necessary, and only once.
        """
        p = urlparse.urlsplit(self._string)
        P = {PROTOCOL: p[0],  # http
             USERNAME: u"",  # user
             PASSWORD: u"",  # pass
               DOMAIN: p[1],  # example.com
                 PORT: u"",  # 992
                 PATH: p[2],  # [animal]
                 PAGE: u"",  # bird
                QUERY: urldecode(p[3]),  # {"species": "seagull", "q": None}
               ANCHOR: p[4]  # wings
        }
        # Split the username and password from the domain.
        if "@" in P[DOMAIN]:
            P[USERNAME], \
            P[PASSWORD] = (p[1].split("@")[0].split(":") + [u""])[:2]
            P[DOMAIN] = p[1].split("@")[1]
        # Split the port number from the domain.
        if ":" in P[DOMAIN]:
            P[DOMAIN], \
            P[PORT] = P[DOMAIN].split(":")
            P[PORT] = int(P[PORT])
        # Split the base page from the path.
        if "/" in P[PATH]:
            P[PAGE] = p[2].split("/")[-1]
            P[PATH] = p[2][:len(p[2]) - len(P[PAGE])].strip("/").split("/")
            P[PATH] = filter(lambda v: v != "", P[PATH])
        else:
            P[PAGE] = p[2].strip("/")
            P[PATH] = []
        self.__dict__["_parts"] = P
    
    # URL.string yields unicode(URL) by joining the different parts,
    # if the URL parts have been modified.
    def _get_string(self): return unicode(self)
    def _set_string(self, v):
        self.__dict__["_string"] = u(v)
        self.__dict__["_parts"] = None
        
    string = property(_get_string, _set_string)
    
    @property
    def parts(self):
        """ Yields a dictionary with the URL parts.
        """
        if not self._parts: self._parse()
        return self._parts
    
    @property
    def querystring(self):
        """ Yields the URL querystring: "www.example.com?page=1" => "page=1"
        """
        s = dict((bytestring(k), bytestring(v or "")) for k, v in self.parts[QUERY].items())
        s = urllib.urlencode(s)
        return s
    
    def __getattr__(self, k):
        if k in self.__dict__ : return self.__dict__[k]
        if k in self.parts    : return self.__dict__["_parts"][k]
        raise AttributeError, "'URL' object has no attribute '%s'" % k
    
    def __setattr__(self, k, v):
        if k in self.__dict__ : self.__dict__[k] = u(v); return
        if k == "string"      : self._set_string(v); return
        if k == "query"       : self.parts[k] = v; return
        if k in self.parts    : self.__dict__["_parts"][k] = u(v); return
        raise AttributeError, "'URL' object has no attribute '%s'" % k
        
    def open(self, timeout=10, proxy=None, user_agent=USER_AGENT, referrer=REFERRER, authentication=None):
        """ Returns a connection to the url from which data can be retrieved with connection.read().
            When the timeout amount of seconds is exceeded, raises a URLTimeout.
            When an error occurs, raises a URLError (e.g. HTTP404NotFound).
        """
        url = self.string
        # Use basic urllib.urlopen() instead of urllib2.urlopen() for local files.
        if os.path.exists(url):
            return urllib.urlopen(url)
        # Get the query string as a separate parameter if method=POST.          
        post = self.method == POST and self.querystring or None
        socket.setdefaulttimeout(timeout)
        if proxy:
            proxy = urllib2.ProxyHandler({proxy[1]: proxy[0]})
            proxy = urllib2.build_opener(proxy, urllib2.HTTPHandler)
            urllib2.install_opener(proxy)
        try:
            request = urllib2.Request(bytestring(url), post, {
                        "User-Agent": user_agent,
                           "Referer": referrer
                         })
            # Basic authentication is established with authentication=(username, password).
            if authentication is not None:
                request.add_header("Authorization", "Basic %s" % 
                    base64.encodestring('%s:%s' % authentication))
            return urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            if e.code == 301: raise HTTP301Redirect
            if e.code == 400: raise HTTP400BadRequest
            if e.code == 401: raise HTTP401Authentication
            if e.code == 403: raise HTTP403Forbidden
            if e.code == 404: raise HTTP404NotFound
            if e.code == 420: raise HTTP420Error
            if e.code == 500: raise HTTP500InternalServerError
            raise HTTPError
        except socket.timeout:
            raise URLTimeout
        except urllib2.URLError, e:
            if e.reason == "timed out" \
            or e.reason[0] in (36, "timed out"): 
                raise URLTimeout
            raise URLError, e.reason
        except ValueError, e:
            raise URLError, e
            
    def download(self, timeout=10, cached=True, throttle=0, proxy=None, user_agent=USER_AGENT, referrer=REFERRER, authentication=None, is_unicode=False):
        """ Downloads the content at the given URL (by default it will be cached locally).
            Unless unicode=False, the content is returned as a unicode string.
        """
#        # Filter OAuth parameters from cache id (they will be unique for each request).
#        if self._parts is None and self.method == GET and "oauth_" not in self._string:
#            id = self._string
#        else: 
#            id = repr(self.parts)
#            id = re.sub("u{0,1}'oauth_.*?': u{0,1}'.*?', ", "", id)
#        # Keep a separate cache of unicode and raw download for same URL.
#        if unicode is True:
#            id = "u" + id
#        if cached and id in cache:
#            if unicode is True:
#                return cache[id]
#            if unicode is False:
#                return cache.get(id, unicode=False)
#        t = time.time()
#        # Open a connection with the given settings, read it and (by default) cache the data.
#        data = self.open(timeout, proxy, user_agent, referrer, authentication).read()
#        if unicode is True:
#            data = u(data)
#        if cached:
#            cache[id] = data
#        if throttle:
#            time.sleep(max(throttle-(time.time()-t), 0))
#        return data
    
    def read(self, *args):
        return self.open().read(*args)
            
    @property
    def exists(self, timeout=10):
        """ Yields False if the URL generates a HTTP404NotFound error.
        """
        try: self.open(timeout)
        except HTTP404NotFound:
            return False
        except HTTPError, URLTimeoutError:
            return True
        except URLError:
            return False
        except:
            return True
        return True
    
    @property
    def mimetype(self, timeout=10):
        """ Yields the MIME-type of the document at the URL, or None.
            MIME is more reliable than simply checking the document extension.
            You can then do: URL.mimetype in MIMETYPE_IMAGE.
        """
        try: 
            return self.headers["content-type"].split(";")[0]
        except KeyError:
            return None
            
    @property
    def headers(self, timeout=10):
        """ Yields a dictionary with the HTTP response headers.
        """
        if self.__dict__["_headers"] is None:
            try:
                h = dict(self.open(timeout).info())
            except URLError:
                h = {}
            self.__dict__["_headers"] = h
        return self.__dict__["_headers"]
            
    @property
    def redirect(self, timeout=10):
        """ Yields the redirected URL, or None.
        """
        if self.__dict__["_redirect"] is None:
            try:
                r = self.open(timeout).geturl()
            except URLError:
                r = None
            self.__dict__["_redirect"] = r != self.string and r or ""
        return self.__dict__["_redirect"] or None

    def __str__(self):
        return bytestring(self.string)
            
    def __unicode__(self):
        # The string representation includes the query attributes with HTTP GET.
        # This gives us the advantage of not having to parse the URL
        # when no separate query attributes were given (e.g. all info is in URL._string):
        if self._parts is None and self.method == GET: 
            return self._string
        P = self._parts
        u = []
        if P[PROTOCOL]: 
            u.append("%s://" % P[PROTOCOL])
        if P[USERNAME]: 
            u.append("%s:%s@" % (P[USERNAME], P[PASSWORD]))
        if P[DOMAIN]:
            u.append(P[DOMAIN])
        if P[PORT]: 
            u.append(":%s" % P[PORT])
        if P[PATH]: 
            u.append("/%s/" % "/".join(P[PATH]))
        if P[PAGE] and len(u) > 0: 
            u[-1] = u[-1].rstrip("/")
        if P[PAGE]: 
            u.append("/%s" % P[PAGE])
        if P[QUERY] and self.method == GET:
            u.append("?%s" % self.querystring)
        if P[ANCHOR]: 
            u.append("#%s" % P[ANCHOR])
        u = u"".join(u)
        u = u.lstrip("/")
        return u

    def __repr__(self):
        return "URL('%s', method='%s')" % (str(self), str(self.method))

    def copy(self):
        return URL(self.string, self.method, self.query)

def download(url=u"", method=GET, query={}, timeout=10, cached=True, throttle=0, proxy=None, user_agent=USER_AGENT, referrer=REFERRER, authentication=None, is_unicode=False):
    """ Downloads the content at the given URL (by default it will be cached locally).
        Unless unicode=False, the content is returned as a unicode string.
    """
    return URL(url, method, query).download(timeout, cached, throttle, proxy, user_agent, referrer, authentication, unicode)

