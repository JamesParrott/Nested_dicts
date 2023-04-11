import json
from nested_dicts import TOMLTable, TOMLListKeyedTable


def test_simple_toml_table():

    p = TOMLTable()
    p['a'].update(
        b=2,
        c=3
    )
    p['a.d'].update(
        e=5,
        f=6
    )
    print(p)
    assert p == {'a': {'b': 2, 'c': 3, 'd': {'e': 5, 'f': 6}}}

# test_simple_toml_table()

def test_simple_toml_table_with_nested_array_of_tables():

    p = TOMLTable()
    p[['a']].update(
        b=2,
        c=3
    )
    p[['a.d']].update(
        e=5,
        f=6
    )
    print(p)
    assert p == {'a': [{'b': 2, 'c': 3, 'd': [{'e': 5, 'f': 6}]}]}


def test_toml_list_keyed_table():

    t = TOMLListKeyedTable()

    t[[1,2,3]]
    t[[1,2,3]]['test'] = 'fd'
    t[[[5,6]]]

    t[[[5,6]]].update(dict(a=1,b=2,c=3))

    t[[[5,6]]]

    t[[[5,6]]]

    assert t == {1: {2: {3: {'test': 'fd'}}}
                ,5: {6: [{}
                        ,{'a': 1
                         ,'b': 2
                         ,'c': 3
                         }
                        ,{}
                        ,{}
                        ]
                    }
                }


def test_same_as_TOML_docs_array_of_tables_first_example():
    """ https://toml.io/en/v1.0.0#array-of-tables

    [[products]]
    name = "Hammer"
    sku = 738594937

    [[products]]  # empty table within the array

    [[products]]
    name = "Nail"
    sku = 284758393

    color = "gray"
    """

    s = TOMLListKeyedTable()
    s[[['products']]].update(
    name = "Hammer",
    sku = 738594937)

    s[[['products']]]  # empty table within the array

    s[[['products']]].update(
    name = "Nail",
    sku = 284758393,

    color = "gray")

    assert s == json.loads("""
{
  "products": [
    { "name": "Hammer", "sku": 738594937 },
    { },
    { "name": "Nail", "sku": 284758393, "color": "gray" }
  ]
}""")

def test_same_as_TOML_docs_array_of_tables_second_example():
    """ https://toml.io/en/v1.0.0#array-of-tables
    
    [[fruits]]
    name = "apple"

    [fruits.physical]  # subtable
    color = "red"
    shape = "round"

    [[fruits.varieties]]  # nested array of tables
    name = "red delicious"

    [[fruits.varieties]]
    name = "granny smith"


    [[fruits]]
    name = "banana"

    [[fruits.varieties]]
    name = "plantain"
    """

    r = TOMLTable()
    r[['fruits']].update(
    name = "apple")

    r['fruits.physical'].update(  # sub table
    color = "red",
    shape = "round")

    r[['fruits.varieties']].update(  # nested array of tables
    name = "red delicious")

    r[['fruits.varieties']].update(
    name = "granny smith")


    r[['fruits']].update(
    name = "banana")

    r[['fruits.varieties']].update(
    name = "plantain")

    assert r == json.loads("""{
  "fruits": [
    {
      "name": "apple",
      "physical": {
        "color": "red",
        "shape": "round"
      },
      "varieties": [
        { "name": "red delicious" },
        { "name": "granny smith" }
      ]
    },
    {
      "name": "banana",
      "varieties": [
        { "name": "plantain" }
      ]
    }
  ]
}""")

