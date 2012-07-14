
"""
Client for the book api
"""

import re

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        print "Unable to find json module"
        raise

import common

BIBKEYS_REGEX = "ISBN|OCLC|LCCN|OLID"
BIBKEYS_REGEX_OBJECT = re.compile(BIBKEYS_REGEX, re.IGNORECASE)

FORMAT_REGEX = "json|javascript"
FORMAT_REGEX_OBJECT = re.compile(FORMAT_REGEX, re.IGNORECASE)

JSCMD_REGEX = "viewapi|data|details"
JSCMD_REGEX_OBJECT = re.compile(JSCMD_REGEX, re.IGNORECASE)


class OpenLibraryBooksClient(common.OpenLibraryClient):

    """
    Class for the book api
    """

    def __init__(self, **kwds):

        """
        Constructor method of the books class
        """

        self.bibkeys = None
        self.jscmd = None
        self.load_json = None
        self.format_ = None

        super(OpenLibraryBooksClient, self).__init__(**kwds)

    def request(self, bibkeys=[], format_="json", jscmd="viewapi",
    load_json=False):

        """
        Request the book api

        @param bibkeys: the different bibkeys to search for. Must be a list of
                        tuples, where the first element of the tuple is the key
                        to search for. This must be a string and
                        match ISBN|OCLC|LCCN|OLID. The second element of the
                        tuple is the value, which must be a string.
        @param format_: the response format, must be a string and match
                        json|javascript, defaults to json.
        @param jscmd: what details should be in the response. Must be a string
                      and match viewapi|data|details". Defaults to viewapi.
        @param load_json: Should the json be loaded into a python dict. Must be
                          a boolean. Defaults to False.

        Returns a string or a python dict, if load_json is True.
        """

        self.bibkeys = []

        if isinstance(bibkeys, list):
            try:
                for key, value in bibkeys:
                    if BIBKEYS_REGEX_OBJECT.match(key):
                        if isinstance(value, str):
                            self.bibkeys.append(":".join([key, value]))
                        else:
                            raise TypeError("value must be a string")
                    else:
                        raise ValueError("key must be ISBN, OCLC, LCCN or OLID")
            except ValueError:
                raise ValueError("There are no tuples in the list")
        else:
            raise TypeError("bibkeys must be a list")

        self.bibkeys = ",".join(self.bibkeys)

        if FORMAT_REGEX_OBJECT.match(format_):
            self.format_ = format_
        else:
            raise ValueError("response_format must be json or javascript")

        if JSCMD_REGEX_OBJECT.match(jscmd):
            self.jscmd = jscmd
        else:
            raise ValueError("jscmd must be viewapi, data or details")

        if isinstance(load_json, bool):
            self.load_json = load_json
        else:
            raise TypeError("load_json must be a boolean")

        bibkeys_variable = "=".join(["bibkeys", self.bibkeys])

        jscmd_variable = "=".join(["jscmd", self.jscmd])

        format_variable = "=".join(["format", self.format_])

        variables = "&".join([bibkeys_variable, jscmd_variable, format_variable])

        url = "?".join(["books", variables])

        message = super(OpenLibraryBooksClient, self).request(url)

        if self.load_json and self.format_ == "json":
            return json.loads(message)
        else:
            return message
