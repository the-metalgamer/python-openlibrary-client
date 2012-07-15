"""
Client for the recentchanges api
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

YEAR_REGEX = "[0-9]{4}"
YEAR_REGEX_OBJECT = re.compile(YEAR_REGEX)

MONTH_REGEX = "1[0-2]|0[1-9]"
MONTH_REGEX_OBJECT = re.compile(MONTH_REGEX)

DAY_REGEX = "3[01]|[12][0-9]|0[1-9]"
DAY_REGEX_OBJECT = re.compile(DAY_REGEX)

KIND_REGEX = "add-cover|add-book|merge-authors|update"
KIND_REGEX_OBJECT = re.compile(KIND_REGEX)


class OpenLibraryRecentChangesClient(common.OpenLibraryClient):

    """
    Class for the recentchanges api
    """

    def __init__(self, base_url="http://openlibrary.org/recentchanges",
    **kwds):

        """
        Constructor method for recentchanges class
        """

        self.kind = None
        self.year = None
        self.month = None
        self.day = None
        self.limit = None
        self.offset = None
        self.bot = None
        self.load_json = None

        super(OpenLibraryRecentChangesClient, self).__init__(base_url,
        **kwds)

    def request(self, year=None, month=None, day=None, kind=None, limit=100,
     offset=0, bot=None, load_json=False):

        """
        Request the recentchanges api

        @param year: the year to filter. Must be a string or None. Defaults to
                     None
        @param month: the month to filter. Must be a string or None. Defaults
                      to None.
        @param day: the day to filter. Must be a string or None. Defaults to
                    None.
        @param kind: filter to search for. Must be None or a string and match
                     add-cover|add-book|merge-authors|update. Defaults to None.
        @param limit: limit the results. Must be a integer an must be between 0
                      and 1000. Defaults to 100.
        @param offset: begin at which item. Must be a integer an must be
                       between 0 and 10000. Defaults to 0.
        @param bot: Include only bots if True or only humans if False. Must be
                    None or a boolean. Defaults to None
        @param load_json: Should the json be loaded into a python dict. Must be
                          a boolean. Defaults to False.

        Returns a string or a python dict, if load_json is True.
        """

        if year is not None:
            if isinstance(year, str):
                if YEAR_REGEX_OBJECT.match(year):
                    self.year = year
                    if month is not None:
                        if isinstance(month, str):
                            if MONTH_REGEX_OBJECT.match(month):
                                self.month = month
                                if day is not None:
                                    if isinstance(day, str):
                                        if DAY_REGEX_OBJECT.match(day):
                                            self.day = day
                                        else:
                                            raise ValueError("day must match 3[01]|[12][0-9]|0[1-9]")
                                    else:
                                        raise TypeError("day must be a string or None")
                                else:
                                    self.day = False
                            else:
                                raise ValueError("month must match 1[0-2]|0[1-9]")
                        else:
                            raise TypeError("month must be a string or None")
                    else:
                        self.month = False
                else:
                    raise ValueError("year must match [0-9]{4}")
            else:
                raise TypeError("year must be a string or None")
        else:
            self.year = False

        if kind is not None:
            if isinstance(kind, str):
                if KIND_REGEX_OBJECT.match(kind):
                    self.kind = kind
                else:
                    raise ValueError("kind must match add-cover|add-book|merge-authors|update")
            else:
                raise TypeError("kind must be a string")
        else:
            self.kind = False

        if isinstance(limit, int):
            if limit <= 1000:
                self.limit = limit
            else:
                raise ValueError("limit must be less or equal to 1000")
        else:
            raise TypeError("limit must be a int")

        if isinstance(offset, int):
            if offset <= 10000:
                self.offset = offset
            else:
                raise ValueError("offset must be less or equal to 10000")
        else:
            raise TypeError("offset must be a int")

        if isinstance(bot, (bool, type(None))):
            self.bot = bot
        else:
            raise TypeError("bot must be a boolean or None")

        if isinstance(load_json, bool):
            self.load_json = load_json
        else:
            raise TypeError("load_json must be a boolean")

        if self.kind:

            kind_variable = ".".join([self.kind, "json"])

            if self.year:
                if self.month:
                    if self.day:
                        url = "/".join(["", self.year,
                        self.month, self.day, kind_variable])
                    else:
                        url = "/".join(["", self.year,
                         self.month, kind_variable])
                else:
                    url = "/".join(["", self.year, kind_variable])
            else:
                url = "".join(["/", kind_variable])
        else:
            if self.year:
                if self.month:
                    if self.day:
                        day_variable = ".".join([self.day, "json"])
                        url = "/".join(["", self.year, self.month,
                                        day_variable])
                    else:
                        month_variable = ".".join([self.month, "json"])
                        url = "/".join(["", self.year, month_variable])
                else:
                    url = "".join(["/", self.year, ".json"])
            else:
                url = ".json"

        limit_variable = "=".join(["limit", str(self.limit)])

        offset_variable = "=".join(["offset", str(self.offset)])

        if self.bot == True or self.bot == False:

            bot_variable = "=".join(["bot", str(self.bot)])

            variables = "?".join([limit_variable, offset_variable,
                                  bot_variable])

        else:
            variables = "?".join([limit_variable, offset_variable])

        url = "".join([url, variables])

        message = super(OpenLibraryRecentChangesClient,
         self).request(url)

        if self.load_json:
            return json.loads(message)
        else:
            return message
