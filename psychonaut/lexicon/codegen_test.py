from psychonaut.lexicon.ctx import GenCtx
from psychonaut.lexicon.types import LexBoolean, LexInteger, LexString, LexXrpcParameters
from .codegen import generate_pydantic_model
from psychonaut.util import load_test_fixture


class TestGeneratePydanticModel:
    def test_from_lex_xrpc_parameters(self, load_test_fixture):
        expected = load_test_fixture("pydantic_model_lex_xrpc_parameters.txt", False)

        ctx = GenCtx()

        lex_xrpc_parameters = LexXrpcParameters(
            description="A test request",
            required=["a_bool"],
            properties={
                "a_bool": LexBoolean(
                    description="A boolean",
                    default=True,
                    #const=False,  # TODO: const is not supported yet
                ),
                "an_int": LexInteger(
                    description="An integer",
                    default=42,
                    minimum=0,
                    maximum=100,
                    #const=42,  # TODO: const is not supported yet
                ),
                "a_string": LexString(
                    description="A string",
                    minLength=1,
                    maxLength=100,
                )
            }
        )

        src = generate_pydantic_model(ctx, "TestReq", "test 1", lex_xrpc_parameters)

        assert src == expected

