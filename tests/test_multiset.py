# -*- coding: utf-8 -*-
import itertools
import pytest
import sys
try:
    from collections.abc import Iterable, Mapping, MutableMapping, Sized, Container
except ImportError:
    from collections import Iterable, Mapping, MutableMapping, Sized, Container

import multiset
from multiset import Multiset, FrozenMultiset, BaseMultiset


def test_missing():
    m = Multiset()
    assert m[object()] == 0

@pytest.mark.parametrize('iterable',
    [
        'abc',
        'babccaad',
        range(100),
        itertools.chain.from_iterable(itertools.repeat(n, n) for n in range(1, 10)),
    ]
)  # yapf: disable
def test_iter(MultisetCls, iterable):
    iter1, iter2 = itertools.tee(iterable, 2)
    m = MultisetCls(iter1)
    expected = sorted(iter2)
    assert sorted(m) == expected
    assert len(m) == len(expected)


def test_setitem():
    m = Multiset()
    assert len(m) == 0

    with pytest.raises(TypeError):
        m[1] = 'a'

    m[1] = 2
    assert m[1] == 2
    assert 1 in m
    assert len(m) == 2

    m[1] = 0
    assert m[1] == 0
    assert 1 not in m
    assert len(m) == 0

    assert 2 not in m
    m[2] = 0
    assert m[2] == 0
    assert 2 not in m
    assert len(m) == 0

    m[3] = -1
    assert m[3] == 0
    assert 3 not in m
    assert len(m) == 0


def test_len(MultisetCls):
    m = MultisetCls()
    assert len(m) == 0

    m = MultisetCls('abc')
    assert len(m) == 3

    m = MultisetCls('aa')
    assert len(m) == 2


def test_bool(MultisetCls):
    assert bool(MultisetCls()) is False
    assert bool(MultisetCls('a')) is True


@pytest.mark.parametrize(
    '   initial,    add,                    result',
    [
        ('aab',     ['abc'],                list('aaabbc')),
        ('aab',     [''],                   list('aab')),
        ('aab',     [{'a': 2, 'b': 1}],     list('aaaabb')),
        ('aab',     [{}],                   list('aab')),
        ('aab',     [{'c': 0}],             list('aab')),
        ('a',       [Multiset('a')],        list('aa')),
        ('ab',      [Multiset()],           list('ab')),
        ('ab',      [],                     list('ab')),
        ('ab',      ['a', 'bc'],            list('aabbc')),
        ('ab',      [{}, ''],               list('ab')),
        ('ab',      [{'c': 1}, {'d': 0}],   list('abc')),
    ]
)  # yapf: disable
def test_update(initial, add, result):
    ms = Multiset(initial)
    ms.update(*add)
    assert sorted(ms) == result
    assert len(ms) == len(result)


@pytest.mark.parametrize(
    '   initial,    add,                    result',
    [
        ('aab',     ['abc'],                list('aabc')),
        ('aab',     [''],                   list('aab')),
        ('aab',     [{'a': 2, 'b': 1}],     list('aab')),
        ('aab',     [{}],                   list('aab')),
        ('aab',     [{'c': 0}],             list('aab')),
        ('a',       [Multiset('a')],        list('a')),
        ('ab',      [Multiset()],           list('ab')),
        ('ab',      [],                     list('ab')),
        ('ab',      ['a', 'bc'],            list('abc')),
        ('ab',      [{}, ''],               list('ab')),
        ('ab',      [{'c': 1}, {'d': 0}],   list('abc')),
        ('ab',      ['aa'],                 list('aab')),
    ]
)  # yapf: disable
def test_union_update(initial, add, result):
    ms = Multiset(initial)
    ms.union_update(*add)
    assert sorted(ms) == result
    assert len(ms) == len(result)


def test_union_update_error():
    with pytest.raises(TypeError):
        Multiset().union_update(None)


def test_ior():
    m = Multiset('ab')

    with pytest.raises(TypeError):
        m |= 'abc'

    m |= Multiset('abc')
    assert sorted(m) == list('abc')


@pytest.mark.parametrize(
    '   initial,    args,                   result',
    [
        ('aab',     ['abc'],                list('ab')),
        ('aab',     [''],                   list()),
        ('aab',     [{'a': 2, 'b': 1}],     list('aab')),
        ('aab',     [{}],                   list()),
        ('aab',     [{'c': 0}],             list()),
        ('a',       [Multiset('a')],        list('a')),
        ('ab',      [Multiset()],           list()),
        ('ab',      [],                     list('ab')),
        ('ab',      ['a', 'bc'],            list()),
        ('ab',      ['a', 'aab'],           list('a')),
        ('ab',      [{}, ''],               list()),
        ('ab',      [{'c': 1}, {'d': 0}],   list()),
        ('ab',      ['aa'],                 list('a')),
    ]
)  # yapf: disable
def test_intersection_update(initial, args, result):
    ms = Multiset(initial)
    ms.intersection_update(*args)
    assert sorted(ms) == result
    assert len(ms) == len(result)


def test_iand():
    m = Multiset('aabd')

    with pytest.raises(TypeError):
        m &= 'abc'

    m &= Multiset('abc')
    assert sorted(m) == list('ab')


@pytest.mark.parametrize(
    '   initial,    other,                result',
    [
        ('aab',     'bc',                 list('aa')),
        ('aab',     'cd',                 list('aab')),
        ('aab',     'a',                  list('ab')),
        ('aab',     'aa',                 list('b')),
        ('aab',     '',                   list('aab')),
        ('aab',     {'a': 2, 'b': 1},     list()),
        ('aab',     {},                   list('aab')),
        ('aab',     {'c': 0},             list('aab')),
        ('a',       Multiset('a'),        list()),
        ('ab',      Multiset(),           list('ab')),
        ('ab',      'aa',                 list('b')),
    ]
)  # yapf: disable
def test_difference_update(initial, other, result):
    ms = Multiset(initial)
    ms.difference_update(other)
    assert sorted(ms) == result
    assert len(ms) == len(result)


def test_isub():
    m = Multiset('aabd')

    with pytest.raises(TypeError):
        m -= 'abc'

    m -= Multiset('abc')
    assert sorted(m) == list('ad')


@pytest.mark.parametrize(
    '   initial,    other,                result',
    [
        ('aab',     'bc',                 list('aac')),
        ('aab',     'cd',                 list('aabcd')),
        ('aab',     'a',                  list('ab')),
        ('aab',     'aa',                 list('b')),
        ('aab',     '',                   list('aab')),
        ('aab',     {'a': 2, 'b': 1},     list()),
        ('aab',     {},                   list('aab')),
        ('aab',     {'c': 0},             list('aab')),
        ('a',       Multiset('a'),        list()),
        ('ab',      Multiset(),           list('ab')),
        ('ab',      'aa',                 list('ab')),
    ]
)  # yapf: disable
def test_symmetric_difference_update(initial, other, result):
    ms = Multiset(initial)
    ms.symmetric_difference_update(other)
    assert sorted(ms) == result
    assert len(ms) == len(result)


def test_ixor():
    m = Multiset('aabd')

    with pytest.raises(TypeError):
        m ^= 'abc'

    m ^= Multiset('abc')
    assert sorted(m) == list('acd')


@pytest.mark.parametrize(
    '   initial,    factor,               result',
    [
        ('aab',     2,                    list('aaaabb')),
        ('a',       3,                    list('aaa')),
        ('abc',     0,                    list()),
        ('abc',     1,                    list('abc'))
    ]
)  # yapf: disable
def test_times_update(initial, factor, result):
    ms = Multiset(initial)
    ms.times_update(factor)
    assert sorted(ms) == result
    assert len(ms) == len(result)


def test_times_update_error():
    with pytest.raises(ValueError):
        Multiset().times_update(-1)


def test_imul():
    m = Multiset('aab')

    with pytest.raises(TypeError):
        m *= 'a'

    with pytest.raises(ValueError):
        m *= -1

    m *= 2
    assert sorted(m) == list('aaaabb')


def test_add():
    m = Multiset('aab')
    assert len(m) == 3

    with pytest.raises(ValueError):
        m.add('a', 0)

    assert 'c' not in m
    m.add('c')
    assert 'c' in m
    assert m['c'] == 1
    assert len(m) == 4

    assert 'd' not in m
    m.add('d', 42)
    assert 'd' in m
    assert m['d'] == 42
    assert len(m) == 46

    m.add('c', 2)
    assert m['c'] == 3
    assert len(m) == 48


def test_remove():
    m = Multiset('aaaabbc')

    with pytest.raises(KeyError):
        m.remove('x')

    with pytest.raises(ValueError):
        m.remove('a', -1)

    assert len(m) == 7

    assert 'c' in m
    count = m.remove('c')
    assert 'c' not in m
    assert count == 1
    assert len(m) == 6

    assert 'b' in m
    count = m.remove('b')
    assert 'b' not in m
    assert count == 2
    assert len(m) == 4

    assert 'a' in m
    count = m.remove('a', 0)
    assert 'a' in m
    assert count == 4
    assert m['a'] == 4
    assert len(m) == 4

    assert 'a' in m
    count = m.remove('a', 1)
    assert 'a' in m
    assert count == 4
    assert m['a'] == 3
    assert len(m) == 3

    count = m.remove('a', 2)
    assert 'a' in m
    assert count == 3
    assert m['a'] == 1
    assert len(m) == 1


def test_delitem():
    m = Multiset('aaaabbc')

    with pytest.raises(KeyError):
        del m['x']

    assert len(m) == 7

    assert 'c' in m
    del m['c']
    assert 'c' not in m
    assert len(m) == 6

    assert 'b' in m
    del m['b']
    assert 'b' not in m
    assert len(m) == 4

    assert 'a' in m
    del m['a']
    assert 'a' not in m
    assert len(m) == 0


def test_discard():
    m = Multiset('aaaabbc')

    with pytest.raises(ValueError):
        m.discard('a', -1)

    assert len(m) == 7

    assert 'c' in m
    count = m.discard('c')
    assert 'c' not in m
    assert count == 1
    assert len(m) == 6

    assert 'b' in m
    count = m.discard('b')
    assert 'b' not in m
    assert count == 2
    assert len(m) == 4

    assert 'a' in m
    count = m.discard('a', 0)
    assert 'a' in m
    assert count == 4
    assert m['a'] == 4
    assert len(m) == 4

    assert 'a' in m
    count = m.discard('a', 1)
    assert 'a' in m
    assert count == 4
    assert m['a'] == 3
    assert len(m) == 3

    count = m.discard('a', 2)
    assert 'a' in m
    assert count == 3
    assert m['a'] == 1
    assert len(m) == 1


@pytest.mark.parametrize(
    '   set1,       set2,           disjoint',
    [
        ('aab',     'a',            False),
        ('aab',     'ab',           False),
        ('a',       'aab',          False),
        ('aab',     'c',            True),
        ('aab',     '',             True),
        ('',        'abc',          True),
    ]
)  # yapf: disable
def test_isdisjoint(MultisetCls, set1, set2, disjoint):
    ms = MultisetCls(set1)

    if disjoint:
        assert ms.isdisjoint(set2)
        assert ms.isdisjoint(iter(set2))
    else:
        assert not ms.isdisjoint(set2)
        assert not ms.isdisjoint(iter(set2))



@pytest.mark.parametrize(
    '   initial,    args,                   expected',
    [
        ('aab',     ['abc'],                list('aabc')),
        ('aab',     [''],                   list('aab')),
        ('aab',     [{'a': 2, 'b': 1}],     list('aab')),
        ('aab',     [{}],                   list('aab')),
        ('aab',     [{'c': 0}],             list('aab')),
        ('a',       [Multiset('a')],        list('a')),
        ('ab',      [Multiset()],           list('ab')),
        ('ab',      [],                     list('ab')),
        ('ab',      ['a', 'bc'],            list('abc')),
        ('ab',      [{}, ''],               list('ab')),
        ('ab',      [{'c': 1}, {'d': 0}],   list('abc')),
        ('ab',      ['aa'],                 list('aab')),
    ]
)  # yapf: disable
def test_union(MultisetCls, initial, args, expected):
    ms = MultisetCls(initial)
    result = ms.union(*args)
    assert sorted(result) == expected
    assert len(result) == len(expected)
    assert isinstance(result, MultisetCls)
    assert result is not ms


def test_union_error(MultisetCls):
    with pytest.raises(TypeError):
        MultisetCls().union(None)


def test_or(MultisetCls):
    ms = MultisetCls('ab')

    with pytest.raises(TypeError):
        _ = ms | 'abc'

    result = ms | MultisetCls('abc')
    assert sorted(result) == list('abc')
    assert isinstance(result, MultisetCls)
    assert result is not ms


@pytest.mark.parametrize(
    '   initial,    args,                   expected',
    [
        ('aab',     ['abc'],                list('aaabbc')),
        ('aab',     [''],                   list('aab')),
        ('aab',     [{'a': 2, 'b': 1}],     list('aaaabb')),
        ('aab',     [{}],                   list('aab')),
        ('aab',     [{'c': 0}],             list('aab')),
        ('a',       [Multiset('a')],        list('aa')),
        ('ab',      [Multiset()],           list('ab')),
        ('ab',      [],                     list('ab')),
        ('ab',      ['a', 'bc'],            list('aabbc')),
        ('ab',      [{}, ''],               list('ab')),
        ('ab',      [{'c': 1}, {'d': 0}],   list('abc')),
        ('aa',      [{'a': -1}],            list('a')),
        ('aa',      [{'a': -2}],            list()),
        ('aa',      [{'a': -3}],            list()),
    ]
)  # yapf: disable
def test_combine(MultisetCls, initial, args, expected):
    ms = MultisetCls(initial)
    result = ms.combine(*args)
    assert sorted(result) == expected
    assert len(result) == len(expected)
    assert isinstance(result, MultisetCls)
    assert result is not ms


def test_add_op(MultisetCls):
    ms = MultisetCls('aab')

    with pytest.raises(TypeError):
        _ = ms + 'abc'

    result = ms + MultisetCls('abc')
    assert sorted(result) == list('aaabbc')
    assert isinstance(result, MultisetCls)
    assert result is not ms


@pytest.mark.parametrize(
    '   initial,    args,                   expected',
    [
        ('aab',     ['abc'],                list('ab')),
        ('aab',     [''],                   list()),
        ('aab',     [{'a': 2, 'b': 1}],     list('aab')),
        ('aab',     [{}],                   list()),
        ('aab',     [{'c': 0}],             list()),
        ('a',       [Multiset('a')],        list('a')),
        ('ab',      [Multiset()],           list()),
        ('ab',      [],                     list('ab')),
        ('ab',      ['a', 'bc'],            list()),
        ('ab',      ['a', 'aab'],           list('a')),
        ('ab',      [{}, ''],               list()),
        ('ab',      [{'c': 1}, {'d': 0}],   list()),
        ('ab',      ['aa'],                 list('a')),
    ]
)  # yapf: disable
def test_intersection(MultisetCls, initial, args, expected):
    ms = MultisetCls(initial)
    result = ms.intersection(*args)
    assert sorted(result) == expected
    assert len(result) == len(expected)
    assert isinstance(result, MultisetCls)
    assert result is not ms


def test_and(MultisetCls):
    ms = MultisetCls('aabd')

    with pytest.raises(TypeError):
        _ = ms & 'abc'

    result = ms & MultisetCls('abc')
    assert sorted(result) == list('ab')
    assert isinstance(result, MultisetCls)
    assert result is not ms


@pytest.mark.parametrize(
    '   initial,    other,                expected',
    [
        ('aab',     'bc',                 list('aa')),
        ('aab',     'cd',                 list('aab')),
        ('aab',     'a',                  list('ab')),
        ('aab',     'aa',                 list('b')),
        ('aab',     '',                   list('aab')),
        ('aab',     {'a': 2, 'b': 1},     list()),
        ('aab',     {},                   list('aab')),
        ('aab',     {'c': 0},             list('aab')),
        ('a',       Multiset('a'),        list()),
        ('ab',      Multiset(),           list('ab')),
        ('ab',      'aa',                 list('b')),
    ]
)  # yapf: disable
def test_difference(MultisetCls, initial, other, expected):
    ms = MultisetCls(initial)
    result = ms.difference(other)
    assert sorted(result) == expected
    assert len(result) == len(expected)
    assert isinstance(result, MultisetCls)
    assert result is not ms


def test_sub(MultisetCls):
    ms = MultisetCls('aabd')

    with pytest.raises(TypeError):
        _ = ms - 'abc'

    result = ms - MultisetCls('abc')
    assert sorted(result) == list('ad')
    assert isinstance(result, MultisetCls)
    assert result is not ms


@pytest.mark.parametrize(
    '   initial,    other,                expected',
    [
        ('aab',     'bc',                 list('aac')),
        ('aab',     'cd',                 list('aabcd')),
        ('aab',     'a',                  list('ab')),
        ('aab',     'aa',                 list('b')),
        ('aab',     '',                   list('aab')),
        ('aab',     {'a': 2, 'b': 1},     list()),
        ('aab',     {},                   list('aab')),
        ('aab',     {'c': 0},             list('aab')),
        ('a',       Multiset('a'),        list()),
        ('ab',      Multiset(),           list('ab')),
        ('ab',      'aa',                 list('ab')),
    ]
)  # yapf: disable
def test_symmetric_difference(MultisetCls, initial, other, expected):
    ms = MultisetCls(initial)
    result = ms.symmetric_difference(other)
    assert sorted(result) == expected
    assert len(result) == len(expected)
    assert isinstance(result, MultisetCls)
    assert result is not ms


def test_xor(MultisetCls):
    ms = MultisetCls('aabd')

    with pytest.raises(TypeError):
        _ = ms ^ 'abc'

    result = ms ^ MultisetCls('abc')
    assert sorted(result) == list('acd')
    assert isinstance(result, MultisetCls)
    assert result is not ms


@pytest.mark.parametrize(
    '   initial,    factor,               expected',
    [
        ('aab',     2,                    list('aaaabb')),
        ('a',       3,                    list('aaa')),
        ('abc',     0,                    list()),
        ('abc',     1,                    list('abc')),
    ]
)  # yapf: disable
def test_times(MultisetCls, initial, factor, expected):
    ms = MultisetCls(initial)

    result = ms.times(factor)

    assert sorted(result) == expected
    assert len(result) == len(expected)
    assert isinstance(result, MultisetCls)
    assert result is not ms


def test_times_error(MultisetCls):
    with pytest.raises(ValueError):
        _ = MultisetCls().times(-1)


def test_mul(MultisetCls):
    ms = MultisetCls('aab')

    with pytest.raises(TypeError):
        _ = ms * 'a'

    result = ms * 2
    assert sorted(result) == list('aaaabb')
    assert isinstance(result, MultisetCls)
    assert result is not ms


@pytest.mark.parametrize(
    '   set1,       set2,       issubset',
    [
        ('a',       'abc',      True),
        ('abc',     'abc',      True),
        ('',        'abc',      True),
        ('d',       'abc',      False),
        ('abcd',    'abc',      False),
        ('aabc',    'abc',      False),
        ('abd',     'abc',      False),
        ('a',       '',         False),
        ('',        'a',        True)
    ]
)  # yapf: disable
def test_issubset(MultisetCls, set1, set2, issubset):
    ms = MultisetCls(set1)
    if issubset:
        assert ms.issubset(set2)
    else:
        assert not ms.issubset(set2)


def test_le(MultisetCls):
    set1 = MultisetCls('ab')
    set2 = MultisetCls('aab')
    set3 = MultisetCls('ac')

    assert set1 <= set2
    assert not set2 <= set1
    assert set1 <= set1
    assert set2 <= set2
    assert not set1 <= set3
    assert not set3 <= set1


@pytest.mark.skipif(sys.version_info < (3, 0), reason="Comparison is broken in Python 2")
def test_le_error(MultisetCls):
    with pytest.raises(TypeError):
        MultisetCls('ab') <= 'x'


def test_lt(MultisetCls):
    set1 = MultisetCls('ab')
    set2 = MultisetCls('aab')
    set3 = MultisetCls('ac')

    assert set1 < set2
    assert not set2 < set1
    assert not set1 < set1
    assert not set2 < set2
    assert not set1 <= set3
    assert not set3 <= set1


@pytest.mark.skipif(sys.version_info < (3, 0), reason="Comparison is broken in Python 2")
def test_lt_error(MultisetCls):
    with pytest.raises(TypeError):
        MultisetCls('ab') < 'x'


@pytest.mark.parametrize(
    '   set1,       set2,       issubset',
    [
        ('abc',     'a',        True),
        ('abc',     'abc',      True),
        ('abc',     '',         True),
        ('abc',     'd',        False),
        ('abc',     'abcd',     False),
        ('abc',     'aabc',     False),
        ('abc',     'abd',      False),
        ('a',       '',         True),
        ('',        'a',        False)
    ]
)  # yapf: disable
def test_issuperset(MultisetCls, set1, set2, issubset):
    ms = MultisetCls(set1)
    if issubset:
        assert ms.issuperset(set2)
    else:
        assert not ms.issuperset(set2)


def test_ge(MultisetCls):
    set1 = MultisetCls('ab')
    set2 = MultisetCls('aab')
    set3 = MultisetCls('ac')

    assert set1 >= set1
    assert not set1 >= set2
    assert not set1 >= set3

    assert set2 >= set1
    assert set2 >= set2
    assert not set2 >= set3

    assert not set3 >= set1
    assert not set3 >= set2
    assert set3 >= set3


@pytest.mark.skipif(sys.version_info < (3, 0), reason="Comparison is broken in Python 2")
def test_ge_error(MultisetCls):
    with pytest.raises(TypeError):
        MultisetCls('ab') >= 'x'


def test_gt(MultisetCls):
    set1 = MultisetCls('ab')
    set2 = MultisetCls('aab')
    set3 = MultisetCls('ac')

    assert not set1 > set1
    assert not set1 > set2
    assert not set1 > set3

    assert set2 > set1
    assert not set2 > set2
    assert not set2 > set3

    assert not set3 > set1
    assert not set3 > set2
    assert not set3 > set3


@pytest.mark.skipif(sys.version_info < (3, 0), reason="Comparison is broken in Python 2")
def test_gt_error(MultisetCls):
    with pytest.raises(TypeError):
        MultisetCls('ab') > 'x'


def test_compare_with_set(MultisetCls):
    assert MultisetCls('ab') <= set('ab')
    assert MultisetCls('b') <= set('ab')
    assert MultisetCls('ab') >= set('ab')
    assert MultisetCls('abb') >= set('ab')
    assert set('ab') <= MultisetCls('abb')
    assert set('b') <= MultisetCls('aab')
    assert not set('ab') >= MultisetCls('aab')
    assert set('ab') <= MultisetCls('aab')
    assert set('ab') >= MultisetCls('ab')


def test_eq_set(MultisetCls):
    multisets = ['', 'a', 'ab', 'aa']
    sets = ['', 'a', 'ab']

    for i, ms in enumerate(multisets):
        ms = MultisetCls(ms)
        for j, s in enumerate(sets):
            s = set(s)
            if i == j:
                assert ms == s
                assert s == ms
            else:
                assert not ms == s
                assert not s == ms


@pytest.mark.parametrize('MultisetCls2', [Multiset, FrozenMultiset])
def test_eq(MultisetCls, MultisetCls2):
    assert not MultisetCls('ab') == MultisetCls2('b')
    assert not MultisetCls('ab') == MultisetCls2('a')
    assert MultisetCls('ab') == MultisetCls2('ab')
    assert MultisetCls('aab') == MultisetCls2('aab')
    assert not MultisetCls('aab') == MultisetCls2('abb')
    assert not MultisetCls('ab') == 'ab'


def test_ne_set(MultisetCls):
    multisets = ['', 'a', 'ab', 'aa']
    sets = ['', 'a', 'ab']

    for i, ms in enumerate(multisets):
        ms = MultisetCls(ms)
        for j, s in enumerate(sets):
            s = set(s)
            if i == j:
                assert not ms != s
                assert not s != ms
            else:
                assert ms != s
                assert s != ms


@pytest.mark.parametrize('MultisetCls2', [Multiset, FrozenMultiset])
def test_ne(MultisetCls, MultisetCls2):
    assert MultisetCls('ab') != MultisetCls2('b')
    assert MultisetCls('ab') != MultisetCls2('a')
    assert not MultisetCls('ab') != MultisetCls2('ab')
    assert not MultisetCls('aab') != MultisetCls2('aab')
    assert MultisetCls('aab') != MultisetCls2('abb')
    assert MultisetCls('ab') != 'ab'


def test_copy(MultisetCls):
    ms = MultisetCls('abc')

    ms_copy = ms.copy()

    assert ms == ms_copy
    assert ms is not ms_copy
    assert isinstance(ms_copy, MultisetCls)


def test_bool(MultisetCls):
    assert MultisetCls('abc')
    assert not MultisetCls()
    assert not MultisetCls({})
    assert not MultisetCls([])


def test_dict_methods(MultisetCls):
    ms = MultisetCls('aab')
    assert ms.get('a', 5) == 2
    assert ms.get('b', 5) == 1
    assert ms.get('c', 5) == 5

    ms = MultisetCls.from_elements('abc', 2)
    assert ['a', 'a', 'b', 'b', 'c', 'c'] == sorted(ms)
    assert isinstance(ms, MultisetCls)


def test_mutating_dict_methods():
    ms = Multiset('aab')

    assert ms.pop('a', 5) == 2
    assert ms.pop('c', 3) == 3
    assert ['b'] == sorted(ms)

    assert ms.setdefault('b', 5) == 1
    assert ms.setdefault('c', 3) == 3
    assert ['b', 'c', 'c', 'c'] == sorted(ms)


@pytest.mark.parametrize('parent', [Iterable, Mapping, Sized, Container])
def test_instance_check(MultisetCls, parent):
    assert isinstance(MultisetCls(), parent)


def test_mutable_instance_check():
    assert isinstance(Multiset(), MutableMapping)


@pytest.mark.parametrize(
    '   elements,   items',
    [
        ('',        []),
        ('a',       [('a', 1)]),
        ('ab',      [('a', 1), ('b', 1)]),
        ('aab',     [('a', 2), ('b', 1)]),
    ]
)  # yapf: disable
def test_items(MultisetCls, elements, items):
    ms = MultisetCls(elements)

    assert sorted(ms.items()) == items


@pytest.mark.parametrize(
    '   elements,   distinct_elements',
    [
        ('',        []),
        ('a',       ['a']),
        ('ab',      ['a', 'b']),
        ('aab',     ['a', 'b']),
        ('aabbb',   ['a', 'b']),
    ]
)  # yapf: disable
def test_distinct_elements(MultisetCls, elements, distinct_elements):
    ms = MultisetCls(elements)

    assert sorted(ms.distinct_elements()) == distinct_elements


@pytest.mark.parametrize(
    '   elements,   multiplicities',
    [
        ('',        []),
        ('a',       [1]),
        ('ab',      [1, 1]),
        ('aab',     [1, 2]),
        ('aabbb',   [2, 3]),
    ]
)  # yapf: disable
def test_multiplicities(MultisetCls, elements, multiplicities):
    ms = MultisetCls(elements)

    assert sorted(ms.multiplicities()) == multiplicities


def test_base_error():
    with pytest.raises(TypeError):
        _ = BaseMultiset()


def test_frozen_hash_equal():
    ms1 = FrozenMultiset('ab')
    ms2 = FrozenMultiset('ab')

    assert hash(ms1) == hash(ms2)
