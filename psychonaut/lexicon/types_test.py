import json
from typing import List, Tuple
from .types import LexXrpcBody, LexiconDoc, LexObject
from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent.parent
LEXICONS_DIR = ROOT_DIR / "lexicons"


class TestProcedure:

    def test_lexicon_input(self):
        # Smoketest
        json_doc = _load_lexicon_doc("com", "atproto", "server", "createAccount")
        input_doc = json_doc["defs"]["main"]["input"]
        got = LexXrpcBody(**input_doc)

        assert got.encoding == "application/json"

        # schema_kludge is a LexObject
        assert isinstance(got.schema_kludge, LexObject)

        schema = got.schema_kludge
        assert schema.type == "object"
        assert schema.required == ["handle", "email", "password"]
        assert len(schema.properties) == 5

        email = schema.properties["email"]
        assert email.type == "string"

        handle = schema.properties["handle"]
        assert handle.type == "string"
        assert handle.format == "handle"

        invite_code = schema.properties["inviteCode"]
        assert invite_code.type == "string"

        password = schema.properties["password"]
        assert password.type == "string"

        recovery_key = schema.properties["recoveryKey"]
        assert recovery_key.type == "string"


    def test_lexicon_output(self):
        # Smoketest

        json_doc = _load_lexicon_doc("com", "atproto", "server", "createAccount")
        output_doc = json_doc["defs"]["main"]["output"]
        got = LexXrpcBody(**output_doc)

        assert got.encoding == "application/json"

        # schema_kludge is a LexObject
        assert isinstance(got.schema_kludge, LexObject)

        schema = got.schema_kludge
        assert schema.type == "object"
        assert schema.required == ["accessJwt", "refreshJwt", "handle", "did"]

        access_jwt = schema.properties["accessJwt"]
        assert access_jwt.type == "string"

        refresh_jwt = schema.properties["refreshJwt"]
        assert refresh_jwt.type == "string"

        handle = schema.properties["handle"]
        assert handle.type == "string"
        assert handle.format == "handle"

        did = schema.properties["did"]
        assert did.type == "string"


    def test_lexicon_doc_from_dict(self):
        json_doc = _load_lexicon_doc("com", "atproto", "server", "createAccount")
        doc = LexiconDoc(**json_doc)
        assert doc.lexicon == 1
        assert doc.id == "com.atproto.server.createAccount"
        assert doc.revision is None
        assert doc.description is None
        assert len(doc.defs) == 1

        # the type of the "main" def is "procedure"
        main = doc.defs["main"]
        assert main.type == "procedure"
        assert main.description == "Create an account."

        input = main.input
        assert input.encoding == "application/json"
        schema = input.schema_kludge
        assert schema.type == "object"
        assert schema.required == ["handle", "email", "password"]

        output = main.output
        assert output.encoding == "application/json"
        schema = output.schema_kludge
        assert schema.type == "object"
        assert schema.required == ["accessJwt", "refreshJwt", "handle", "did"]

        assert len(main.errors) == 5
        assert main.errors[0].name == "InvalidHandle"
        assert main.errors[1].name == "InvalidPassword"
        assert main.errors[2].name == "InvalidInviteCode"
        assert main.errors[3].name == "HandleNotAvailable"
        assert main.errors[4].name == "UnsupportedDomain"



def _load_lexicon_doc(*parts: Tuple[str]) -> LexiconDoc:
    parts = list(parts)
    parts[-1] = parts[-1] + ".json"
    full_path = LEXICONS_DIR.joinpath(*parts)
    with open(full_path, "r") as f:
        return json.load(f)
