"""
Client for the read api
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

ID_TYPE_REGEX = "isbn|lccn|oclc|olid"
ID_TYPE_REGEX_OBJECT = re.compile(ID_TYPE_REGEX, re.IGNORECASE)


class OpenLibraryReadClient(common.OpenLibraryClient):

    """
    Class for the read api
    """

    def __init__(self,
    base_url="http://openlibrary.org/api/volumes/brief/", **kwds):

        """
        Constructor method for the read class
        """

        self.id_type = None
        self.id_value = None
        self.load_json = None

        super(OpenLibraryReadClient, self).__init__(base_url, **kwds)

    def single_request(self, id_type="", id_value="", load_json=False):

        """
        Request only a single item

        @param id_type: The type to search for. Must be a string and match
                        isbn|lccn|oclc|olid
        @param id_value: The value to search for. Must be a string.
        @param load_json: Should the json be loaded into a python dict. Must be
                          a boolean. Defaults to False.

        Returns a string or a python dict, if load_json is True.
        """

        if isinstance(id_type, str):
            if ID_TYPE_REGEX_OBJECT.match(id_type):
                self.id_type = id_type
            else:
                raise ValueError("id_type must be isbn, lccn, oclc or olid")
        else:
            raise TypeError("id_type must be a string")

        if isinstance(id_value, str):
            self.id_value = id_value
        else:
            raise TypeError("id_value must be a string")

        if isinstance(load_json, bool):
            self.load_json = load_json
        else:
            raise TypeError("load_json must be a boolean")

        id_value_variable = ".".join([self.id_value, "json"])

        url = "/".join([self.id_type, id_value_variable])

        message = super(OpenLibraryReadClient, self).request(url)

        if self.load_json:
            return json.loads(message)
        else:
            return message

    def multi_request(self, requests=[], load_json=False):

        """
        Request multiple items at once.

        @param requests: The different keys and values to search for. Must be
                         a list of tuples, where the first element of the
                         tuple is the key to search for. This must be a string
                         and match isbn|lccn|oclc|olid. The second element of
                         the tuple is the value, which must be a string.
        @param load_json: Should the json be loaded into a python dict. Must be
                          a boolean. Defaults to False.

        Returns a string or a python dict, if load_json is True.
        """

        if isinstance(load_json, bool):
            self.load_json = load_json
        else:
            raise TypeError("load_json must be a boolean")

        request_list = []
        for request in requests:
            library_ids = []
            for key, value in request:
                if ID_TYPE_REGEX_OBJECT.match(key):
                    if isinstance(value, str):
                        library_ids.append(":".join([key, value]))
                    else:
                        raise TypeError("value must be a string")
                else:
                    raise ValueError("key must be isbn, lccn, oclc or olid")

            request_list.append(";".join(library_ids))

        requests = "|".join(request_list)

        url = "/".join(["json", requests])

        message = super(OpenLibraryReadClient, self).request(url)

        if load_json:
            return json.loads(message)
        else:
            return message
