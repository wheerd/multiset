"""Failed updates must not leave the stored size out of sync with the items."""
import pytest

from multiset import Multiset


@pytest.mark.parametrize('method', ['update', 'union_update'])
@pytest.mark.parametrize('initial', ['', 'aab'])
@pytest.mark.parametrize('bad_operand', [
    {'a': 4, 'c': None},
    {'a': 4, 'c': object()},
])
def test_invalid_count_preserves_size_invariant(method, initial, bad_operand):
    ms = Multiset(initial)
    with pytest.raises(TypeError):
        getattr(ms, method)(bad_operand)
    assert len(ms) == sum(ms.multiplicities())
    assert len(list(ms)) == len(ms)
    assert bool(ms) == bool(list(ms))
    ms.add('d')
    assert len(ms) == sum(ms.multiplicities())
    del ms['a']
    assert len(ms) == sum(ms.multiplicities())


@pytest.mark.parametrize('method', ['update', 'union_update'])
def test_later_invalid_operand_preserves_earlier_size(method):
    ms = Multiset('a')
    with pytest.raises(TypeError):
        getattr(ms, method)({'b': 2}, None)
    assert ms == Multiset('abb')
    assert len(ms) == 3


@pytest.mark.parametrize('method', ['update', 'union_update'])
def test_empty_update_and_normal_updates(method):
    ms = Multiset('aab')
    getattr(ms, method)()
    assert ms == Multiset('aab')
    getattr(ms, method)({'c': 3})
    assert len(ms) == 6
    assert sum(ms.multiplicities()) == 6
