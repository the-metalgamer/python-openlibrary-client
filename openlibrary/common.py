"""
Base class
"""

import urllib2 as urllib


class OpenLibraryClient(object):

    """
    Base class for the different clients

    Don't use it directly
    """

    def __init__(self, base_url="http://openlibrary.org/api/"):

        """
        Constructor method for the base class

        @param base_url: The base url of the webservice. Must be a string.
        """

        self.base_url = base_url
        self.url = None
        self.lines = None

    def request(self, path, lines=False):

        """
        Request the the webservice for a response.

        @param path: the path of the api, must be a string
        @param lines: Read more lines at once and concatenate them, must be a
                      boolean

        Return a string.
        """

        self.url = "".join([self.base_url, path])

        if isinstance(lines, bool):
            self.lines = lines
        else:
            raise TypeError("lines must be a boolean")

        if self.lines:
            return "".join(urllib.urlopen(self.url).readlines())
        else:
            return urllib.urlopen(self.url).readline()
