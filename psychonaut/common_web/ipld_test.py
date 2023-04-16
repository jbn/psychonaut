from .ipld import json_to_ipld, ipld_to_json, ipld_equals


def test_ipld():
    person = {
        "name": "Alice",
        "age": 30,
        "friend": {
            "/": {
                "$link": "bafyreih3j6mikj3ocg2reh4ox62uthv7g5rgl6yvbdg3qkbhaya5omazie"  
            }
        }
    }

    person_ipld = json_to_ipld(person)
    person_json = ipld_to_json(person_ipld)
    assert ipld_equals(person, person_json)