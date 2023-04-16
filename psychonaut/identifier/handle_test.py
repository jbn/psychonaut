import pytest

from .handle import (
    ensure_valid_handle,
    ensure_valid_handle_regex,
    ensure_handle_service_constraints,
    normalize_and_ensure_valid_handle,
    InvalidHandleError,
)


def expect_valid(h: str):
    ensure_valid_handle(h)
    ensure_valid_handle_regex(h)

def expect_invalid(h: str):
    with pytest.raises(InvalidHandleError):
        ensure_valid_handle(h)
    with pytest.raises(InvalidHandleError):
        ensure_valid_handle_regex(h)


class TestHandleValidation:

    def test_valid_handles(self):
        long_handle = 'shoooort' + ('.loooooooooooooooooooooooooong' * 8) + '.test'  
        assert len(long_handle) == 253

        valid_handles = [
            'A.ISI.EDU',
            'XX.LCS.MIT.EDU',
            'SRI-NIC.ARPA',
            'john.test',
            'jan.test',
            'a234567890123456789.test',
            'john2.test',
            'john-john.test',
            'john.bsky.app',
            'jo.hn',
            'a.co',
            'a.org',
            'joh.n',
            'j0.h0',
            long_handle,
            'jaymome-johnber123456.test',
            'jay.mome-johnber123456.test',
            'john.test.bsky.app',
            'laptop.local',
            'laptop.arpa',
            'john.t',
        ]
        for handle in valid_handles:
            expect_valid(handle)


    def test_puny_handles(self):
        valid_punycode_handles = ['xn--ls8h.test', 'xn--bcher-kva.tld']
        for handle in valid_punycode_handles:
            expect_valid(handle)

    def test_throws_on_invalid_handles(self):
        expect_invalid('did:thing.test')
        expect_invalid('did:thing')
        expect_invalid('john-.test')
        expect_invalid('john.0')
        expect_invalid('john.-')
        expect_invalid('short.' + 'o' * 64 + '.test')
        expect_invalid('short' + '.loooooooooooooooooooooooong' * 10 + '.test')
        long_handle = 'shooooort' + '.loooooooooooooooooooooooooong' * 8 + '.test'
        assert len(long_handle) == 254
        expect_invalid(long_handle)
        expect_invalid('xn--bcher-.tld')
        expect_invalid('john..test')
        expect_invalid('jo_hn.test')
        expect_invalid('-john.test')
        expect_invalid('.john.test')
        expect_invalid('jo!hn.test')
        expect_invalid('jo%hn.test')
        expect_invalid('jo&hn.test')
        expect_invalid('jo@hn.test')
        expect_invalid('jo*hn.test')
        expect_invalid('jo|hn.test')
        expect_invalid('jo:hn.test')
        expect_invalid('jo/hn.test')
        expect_invalid('john💩.test')
        expect_invalid('bücher.test')
        expect_invalid('john .test')
        expect_invalid('john.test.')
        expect_invalid('john')
        expect_invalid('john.')
        expect_invalid('.john')
        expect_invalid('john.test.')
        expect_invalid('.john.test')
        expect_invalid(' john.test')
        expect_invalid('john.test ')
        expect_invalid('joh-.test')
        expect_invalid('john.-est')
        expect_invalid('john.tes-')

    def test_allows_onion_tor_handles(self):
        expect_valid('expyuzz4wqqyqhjn.onion')
        expect_valid('friend.expyuzz4wqqyqhjn.onion')
        expect_valid('g2zyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion')
        expect_valid('friend.g2zyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion')
        expect_valid('friend.g2zyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion')
        expect_valid('2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion')
        expect_valid('friend.2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion')

    def test_correctly_validates_corner_cases_modern_vs_old_rfc(self):
        expect_valid('12345.test')
        expect_valid('8.cn')
        expect_valid('4chan.org')
        expect_valid('4chan.o-g')
        expect_valid('blah.4chan.org')
        expect_valid('thing.a01')
        expect_valid('120.0.0.1.com')
        expect_valid('0john.test')
        expect_valid('9sta--ck.com')
        expect_valid('99stack.com')
        expect_valid('0ohn.test')
        expect_valid('john.t--t')
        expect_valid('thing.0aa.thing')

        expect_invalid('cn.8')
        expect_invalid('thing.0aa')
        expect_invalid('thing.0aa')

    def test_does_not_allow_ip_addresses_as_handles(self):
        expect_invalid('127.0.0.1')
        expect_invalid('192.168.0.142')
        expect_invalid('fe80::7325:8a97:c100:94b')
        expect_invalid('2600:3c03::f03c:9100:feb0:af1f')

    def test_is_consistent_with_examples_from_stackoverflow(self):
        ok_stackoverflow = [
            'stack.com',
            'sta-ck.com',
            'sta---ck.com',
            'sta--ck9.com',
            'stack99.com',
            'sta99ck.com',
            'google.com.uk',
            'google.co.in',
            'google.com',
            'maselkowski.pl',
            'm.maselkowski.pl',
            'xn--masekowski-d0b.pl',
            'xn--fiqa61au8b7zsevnm8ak20mc4a87e.xn--fiqs8s',
            'xn--stackoverflow.com',
            'stackoverflow.xn--com',
            'stackoverflow.co.uk',
            'xn--masekowski-d0b.pl',
            'xn--fiqa61au8b7zsevnm8ak20mc4a87e.xn--fiqs8s',
        ]

        for domain in ok_stackoverflow:
            expect_valid(domain)

        bad_stackoverflow = [
            '-notvalid.at-all',
            '-thing.com',
            'www.masełkowski.pl.com',
        ]

        for domain in bad_stackoverflow:
            expect_invalid(domain)


class TestServiceConstraintsAndNormalization:
    domains = ['.bsky.app', '.test']

    def test_throw_on_handles_that_violate_service_constraints(self):
        def expect_throw(handle, err):
            with pytest.raises(Exception, match=err):
                ensure_handle_service_constraints(handle, self.domains)

        expect_throw('john.bsky.io', 'Not a supported handle domain')
        expect_throw('john.com', 'Not a supported handle domain')
        expect_throw('j.test', 'Handle too short')
        expect_throw('uk.test', 'Handle too short')
        expect_throw('john.test.bsky.app', 'Invalid characters in handle')
        expect_throw('about.test', 'Reserved handle')
        expect_throw('atp.test', 'Reserved handle')
        expect_throw('barackobama.test', 'Reserved handle')


    def test_normalizes_handles(self):
        normalized = normalize_and_ensure_valid_handle('JoHn.TeST')
        assert normalized == 'john.test'


    def test_throws_on_invalid_normalized_handles(self):
        with pytest.raises(InvalidHandleError):
            normalize_and_ensure_valid_handle('JoH!n.TeST')
