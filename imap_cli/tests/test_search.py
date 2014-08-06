# -*- coding: utf-8 -*-


"""Test helpers"""


import datetime
import imaplib
import unittest

from imap_cli import search
from imap_cli import tests


class SearchTests(unittest.TestCase):
    def setUp(self):
        imaplib.IMAP4_SSL = tests.ImapConnectionMock()

    def test_basic_search(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.login()

        assert search.create_search_criterion() == ['ALL']

    def test_create_search_criteria_by_date(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.login()

        date = datetime.datetime(1989, 1, 3)
        search_criterion = search.create_search_criterion(date=date)
        assert search_criterion == ['SINCE 03-Jan-1989']

        search_criterion = search.create_search_criterion_by_date(date, relative='BEFORE')
        assert search_criterion == 'BEFORE 03-Jan-1989'

        search_criterion = search.create_search_criterion_by_date(date, relative='ON')
        assert search_criterion == 'ON 03-Jan-1989'

        search_criterion = search.create_search_criterion_by_date(date, relative='SINCE')
        assert search_criterion == 'SINCE 03-Jan-1989'

        search_criterion = search.create_search_criterion_by_date(date, relative='BEFORE', sent=True)
        assert search_criterion == 'SENTBEFORE 03-Jan-1989'

        search_criterion = search.create_search_criterion_by_date(date, relative='ON', sent=True)
        assert search_criterion == 'SENTON 03-Jan-1989'

        search_criterion = search.create_search_criterion_by_date(date, relative='SINCE', sent=True)
        assert search_criterion == 'SENTSINCE 03-Jan-1989'

    def test_create_search_criteria_by_size(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.login()

        size = 3141592
        search_criterion = search.create_search_criterion(size=size)
        assert search_criterion == ['LARGER "3141592"']

        search_criterion = search.create_search_criterion_by_size(size, relative='SMALLER')
        assert search_criterion == 'SMALLER "3141592"'

        search_criterion = search.create_search_criterion_by_size(size, relative='LARGER')
        assert search_criterion == 'LARGER "3141592"'

        search_criterion = search.create_search_criterion_by_size(size, relative='Anything')
        assert search_criterion == 'LARGER "3141592"'

    def test_create_search_criteria_by_tag(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.login()

        tags = ['seen']
        search_criterion = search.create_search_criterion(tags=tags)
        assert search_criterion == ['SEEN']

        tags = ['testTag']
        search_criterion = search.create_search_criterion(tags=tags)
        assert search_criterion == ['KEYWORD "testTag"']

        tags = ['seen', 'testTag']
        search_criterion = search.create_search_criterion(tags=tags)
        assert search_criterion == ['(SEEN KEYWORD "testTag")']

    def test_create_search_criteria_by_text(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.login()

        text = 'CONTENT'
        search_criterion = search.create_search_criterion(text=text)
        assert search_criterion == ['BODY "CONTENT"']

    def test_execute_simple_search(self):
        self.imap_account = imaplib.IMAP4_SSL()
        self.imap_account.login()

        assert search.fetch_uids(self.imap_account) == ['1']
