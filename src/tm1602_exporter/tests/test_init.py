from .. import *

import pytest
import requests


@pytest.fixture
def tcollector(monkeypatch, tmp_path):
    html_file = Path(__file__).parent.joinpath('page.html')
    c = Collector()

    c.page = html_file.read_text()
    c.seconds_between_fetch = 3600
    return c


@pytest.mark.parametrize('h, r', [
    ("Shit happens", "shit_happens"),
    ("blah 100%", "blah_100_"),
])
def test__make_header(tcollector, h, r):
    assert tcollector._make_header(h) == r


@pytest.mark.parametrize('h, r', [
    ("100 dB", "100"),
    ("100.8 Mhz", "100.8"),
])
def test__make_data(tcollector, h, r):
    assert tcollector._make_data(h) == r


def test_get_doc(tcollector):
    assert tcollector.get_doc('test') == "No Documentation"


def test_get_table0(tcollector):
    t = tcollector.get_table('Downstream')
    assert 'Downstream 1' in str(t)

    t = tcollector.get_table('Upstream')
    assert 'Upstream 1' in str(t)


def test_get_table1(tcollector, requests_mock):
    requests_mock.get(tcollector.url, text=tcollector.page)
    tcollector.page = None

    t = tcollector.get_table('Downstream')
    assert 'Downstream 1' in str(t)

    t = tcollector.get_table('Upstream')
    assert 'Upstream 1' in str(t)


def test_parse_html_table(tcollector):
    assert tcollector.parse_html_table('Downstream')[0] == {
        'channel': 'Downstream 1',
        'dcid': '6',
        'freq': '609.00 MHz',
        'power': '5.70 dBmV',
        'snr': '38.98 dB',
        'modulation': '256QAM',
        'octets': '38391590',
        'correcteds': '0',
        'uncorrectables': '0'
    }

    assert tcollector.parse_html_table('Upstream')[0] == {
        'channel': 'Upstream 1',
        'ucid': '2',
        'freq': '22.00 MHz',
        'power': '45.25 dBmV',
        'channel_type': 'DOCSIS2.0 (ATDMA)',
        'symbol_rate': '5120 kSym/s',
        'modulation': '64QAM'
        }


def test_make_metric0(tcollector):
    m = tcollector.make_metric('abc', 1.23, 'test', dict(), False)
    assert str(m) == ("Metric(abc, test, gauge, , [Sample(name='abc', labels={}, "
                      "value=1.23, timestamp=None, exemplar=None)])")


def test_make_metric1(tcollector):
    m = tcollector.make_metric('abc', 1.23, 'test', dict(), True)
    assert str(m) == ("Metric(abc, test, counter, , [Sample(name='abc_total', labels={}, "
                      "value=1.23, timestamp=None, exemplar=None)])")


def test_process_table(tcollector):
    tbl = [{
        'channel': 'Downstream 1',
        'dcid': '6',
        'freq': '609.00 MHz',
        'power': '5.70 dBmV',
    }]

    c = tcollector.process_table('prefix', tbl)

    assert len(c) == 2
    assert str(c[0]) == ("Metric(prefix_power, No Documentation, gauge, , [Sample(name='prefix_power', "
                         "labels={'dcid': '6', 'freq': '609.00 MHz'}, value=5.7, timestamp=None, exemplar=None)])")
    assert str(c[1]) == ("Metric(prefix_state, No Documentation, gauge, , [Sample(name='prefix_state', "
                         "labels={'dcid': '6', 'freq': '609.00 MHz'}, value=1, timestamp=None, exemplar=None)])")


def test_collect(tcollector):
    c = tcollector.collect()
    # FIXME

    assert len(c) == (24 * 6 +   # 24 downstream channels with 6 metrics per channel
                      4 * 3)     # 4 upstream channels with 3 metrics per channel
