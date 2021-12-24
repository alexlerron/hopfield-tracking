import pandas as pd
import pytest
from numpy.testing import assert_array_equal
from pandas._testing import assert_frame_equal

from datasets.trackml import _transform, get_hits_trackml, get_hits_trackml_by_module, \
    get_hits_trackml_by_volume, get_hits_trackml_one_event, get_hits_trackml_one_event_by_volume, \
    get_hits_trackml_one_event_by_module

_test_event = pd.DataFrame({
    'hit_id': [1, 2, 3, 4, 5],
    'x': [1., 2., 3., 4., 5.],
    'y': [2., 3., 4., 5., 6.],
    'z': [3., 4., 5., 6., 7.],
    'volume_id': [7] * 5,
    'layer_id': [2] * 5,
    'module_id': [1] * 5,
    'particle_id': [0, 123456789012345678, 0, 123456789012345678, 987654321098765432],
    'tx': [0.1, 0.2, 0.3, 0.4, 0.5],
    'ty': [0.2, 0.3, 0.4, 0.5, 0.6],
    'tz': [0.3, 0.4, 0.5, 0.6, 0.7],
    'tpx': [11, 1.1, 22, 1.2, 1.3],
    'tpy': [22, 2.2, 33, 2.3, 2.4],
    'tpz': [33, 3.3, 44, 3.4, 3.5],
    'weight': [0, 1e-6, 0, 2e-6, 3e-6]
})

_test_blacklist = pd.DataFrame({'hit_id': [1, 5]})


def test__transform():
    events = _transform(_test_event, _test_blacklist)
    assert_frame_equal(events, pd.DataFrame({
        'hit_id': [2, 3, 4],
        'x': [2., 3., 4.],
        'y': [3., 4., 5.],
        'z': [4., 5., 6.],
        'volume_id': [7] * 3,
        'layer': [1] * 3,
        'module_id': [1] * 3,
        'track': [123456789012345678, -1, 123456789012345678],
        'tx': [0.2, 0.3, 0.4],
        'ty': [0.3, 0.4, 0.5],
        'tz': [0.4, 0.5, 0.6],
        'tpx': [1.1, 22, 1.2],
        'tpy': [2.2, 33, 2.3],
        'tpz': [3.3, 44, 3.4],
        'weight': [1e-6, 0, 2e-6]
    }))


@pytest.mark.slow
@pytest.mark.bman
def test_get_hits_trackml():
    events = get_hits_trackml()
    assert_array_equal(events.index, range(10952747))
    assert_array_equal(events.event_id.unique(), range(1000, 1100))
    assert set(events.layer.unique()) == set(range(1, 8))
    assert events.track.min() == -1
    assert events.track.dtype == 'int64'


def test_get_hits_trackml_one_event():
    events = get_hits_trackml_one_event()
    assert_array_equal(events.index, range(120940-179))
    assert_array_equal(events.event_id.unique(), 1000)
    assert set(events.layer.unique()) == set(range(1, 8))
    assert events.track.min() == -1
    assert events.track.dtype == 'int64'


@pytest.mark.slow
@pytest.mark.bman
def test_get_hits_trackml_by_volume():
    events = get_hits_trackml_by_volume()
    assert_array_equal(events.index, range(10952747))
    assert_array_equal(events.event_id.str.fullmatch(r'\d{4}-\d{1,2}'), True)
    assert set(events.layer.unique()) == set(range(1, 8))
    assert events.track.min() == -1
    assert events.track.dtype == 'int64'


def test_get_hits_trackml_one_event_by_volume():
    events = get_hits_trackml_one_event_by_volume()
    assert_array_equal(events.index, range(16873-15))
    assert events.hit_id.min() == 1
    assert events.hit_id.max() == 16873
    assert_array_equal(events.event_id, '1000-7')
    assert set(events.layer.unique()) == set(range(1, 8))
    assert events.track.min() == -1
    assert events.track.dtype == 'int64'


@pytest.mark.slow
@pytest.mark.bman
def test_get_hits_trackml_by_module():
    events = get_hits_trackml_by_module()
    assert_array_equal(events.index, range(10952747))
    assert_array_equal(events.event_id.str.fullmatch(r'\d{4}-\d{1,2}-\d{1,4}'), True)
    assert set(events.layer.unique()) == set(range(1, 8))
    assert events.track.min() == -1
    assert events.track.dtype == 'int64'


def test_get_hits_trackml_one_event_by_module():
    events = get_hits_trackml_one_event_by_module()
    # TODO: check that slicing by module makes any sense
    assert_array_equal(events.index, range(287))
    assert events.hit_id.min() == 1
    assert events.hit_id.max() == 13906
    assert_array_equal(events.event_id.str.fullmatch(r'\d{4}-\d{1,2}-\d{1,4}'), True)
    assert set(events.layer.unique()) == set(range(1, 8))
    assert events.track.min() == -1
    assert events.track.dtype == 'int64'