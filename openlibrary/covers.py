"""
Client for the cover api
"""


import re

import common

KEY_COVER_REGEX = "isbn|oclc|lccn|olid|id"
KEY_COVER_REGEX_OBJECT = re.compile(KEY_COVER_REGEX, re.IGNORECASE)

KEY_AUTHOR_REGEX = "olid|id"
KEY_AUTHOR_REGEX_OBJECT = re.compile(KEY_AUTHOR_REGEX, re.IGNORECASE)

SIZE_REGEX = "S|M|L"
SIZE_REGEX_OBJECT = re.compile(SIZE_REGEX)


class OpenLibraryCoversClient(common.OpenLibraryClient):

    """
    Class for the cover api
    """

    def __init__(self, base_url="http://covers.openlibrary.org/",
    **kwds):

        """
        Constructor method for the cover class
        """

        self.key = None
        self.value = None
        self.size = None

        super(OpenLibraryCoversClient, self).__init__(base_url, **kwds)

    def request_book_cover(self, key="", value="", size=""):

        """
        Request a book cover

        @param key: The key to search for. Must be a string and match
                    isbn|oclc|lccn|olid|id
        @param value: The value to search for. Must be a string.
        @param size: What size the image must have. Must be a string and match
                     S|M|L

        Returns a string.
        """

        if KEY_COVER_REGEX_OBJECT.match(key):
            self.key = key
        else:
            raise ValueError("key must be isbn, oclc, lccn, olid or id")

        if isinstance(value, str):
            self.value = value
        else:
            raise TypeError("value must be a string")

        if SIZE_REGEX_OBJECT.match(size):
            self.size = size
        else:
            raise ValueError("size must be S, M, or L")

        image = "-".join([self.value, self.size])
        image = ".".join([image, "jpg"])
        url = "/".join(["b", self.key, image])

        return super(OpenLibraryCoversClient, self).request(url, lines=True)

    def request_author_photo(self, key="", value="", size=""):

        """
        Request a author photo

        @param key: The key to search for. Must be a string and match
                    olid|id
        @param value: The value to search for. Must be a string.
        @param size: What size the image must have. Must be a string and match
                     S|M|L
        """

        if KEY_AUTHOR_REGEX_OBJECT.match(key):
            self.key = key
        else:
            raise ValueError("key must be olid or id")

        if isinstance(value, str):
            self.value = value
        else:
            raise TypeError("value must be a string")

        if SIZE_REGEX_OBJECT.match(size):
            self.size = size
        else:
            raise ValueError("size must be S, M or L")

        image = "-".join([self.value, self.size])
        image = ".".join([image, "jpg"])
        url = "/".join(["a", self.key, image])

        return super(OpenLibraryCoversClient, self).request(url, lines=True)
