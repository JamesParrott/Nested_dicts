from nested_dicts import (NestedDefaultsDict
                         ,ListKeyedDict
                         ,ListKeyedNestedDefaultsDict
                         ,list_keyed_from_nested_dict_and_lists
                         ,DottedKeyedNestedDefaultsDict
                         )


def test_simple_nested_default_dict():
    ndd = NestedDefaultsDict()
    ndd[1][2][3] = 98
    ndd['a']
    
    assert ndd == {1: {2: {3: 98}}
                  ,'a': {}
                  }

TEST_NESTED_DICT = {4: {'r' : 67, 23: 'se', 'we': {'a' : 123}}}


def test_nested_default_dict_preserves_nested_dict():

    ndd = NestedDefaultsDict.from_nested_dict(TEST_NESTED_DICT)
    assert ndd == TEST_NESTED_DICT

def test_list_keyed_dict_preserves_nested_dict_and_returns_correct_vals():

    lkd = ListKeyedDict.from_nested_dict(TEST_NESTED_DICT)
    assert lkd[[4,'we','a']] == 123
    assert lkd == TEST_NESTED_DICT

def test_list_keyed_nested_defaults_dict_preserves_nested_dict():

    lkndd = ListKeyedNestedDefaultsDict.from_nested_dict(TEST_NESTED_DICT)
    assert lkndd == TEST_NESTED_DICT

def test_list_keyed_nested_defaults_dict_can_be_defined_from_lists_of_keys():
    lkndd = ListKeyedNestedDefaultsDict()
    lkndd[[1,2,3]] = 98
    lkndd[[4,5,6]]
    assert lkndd == {1: {2: {3: 98}}
                    ,4: {5: {6: {}}}
                    }

    lkndd[[4,5,6]] = 'rtt'
    lkndd['a']
    assert lkndd == {1: {2: {3: 98}}
                    ,4: {5: {6: 'rtt'}}
                    ,'a': {}
                    }

TEST_NESTED_DICTS_AND_LISTS = {4: [dict(a=1, b=2, c=3), {'r' : 67, 23: 'se', 'we': {'a' : 123}}]}

def test_list_keyed_from_nested_dict_and_lists_preserves_nested_lists_and_keys():
    lolknd = list_keyed_from_nested_dict_and_lists(TEST_NESTED_DICTS_AND_LISTS)
    assert lolknd == TEST_NESTED_DICTS_AND_LISTS

def test_dotted_keys_set_item():
    
    d = DottedKeyedNestedDefaultsDict()
    d['k.sub_dict_key'] = 'v'
    assert d == {'k': {'sub_dict_key': 'v'}}

SIMPLE_DICT_FROM_README = {'k': {'sub_dict_key': 'v'}}

def test_readmeNestedDefaultsDict():
    d = NestedDefaultsDict()
    d['k']['sub_dict_key'] = 'v'
    assert d == SIMPLE_DICT_FROM_README


def test_readmeListKeyedDict():
    d = ListKeyedDict.from_nested_dict({'k': {'sub_dict_key': 'v'}})
    d[['k', 'sub_dict_key']]
    assert d == SIMPLE_DICT_FROM_README

def test_readmeListKeyedNestedDefaultsDict():
    d = ListKeyedNestedDefaultsDict()
    d[['k', 'sub_dict_key']] = 'v'
    assert d == SIMPLE_DICT_FROM_README

def test_readmeDottedKeyedNestedDefaultsDict():
    d = DottedKeyedNestedDefaultsDict()
    d['k.sub_dict_key'] = 'v'
    assert d == SIMPLE_DICT_FROM_README
