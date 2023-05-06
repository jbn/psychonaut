import importlib
import os 


def test_jit():
    import psychonaut.core.jit as jit

    orig_value = os.environ.get('NUMBA_DISABLE_JIT')
    assert jit.USING_NUMBA == (orig_value is None)

    if not orig_value:
        os.environ['NUMBA_DISABLE_JIT'] = '1'
        importlib.reload(jit)
        assert not jit.USING_NUMBA

        @jit.jit(nopython=True)
        def square(x: int) -> int:
            return x * x
        
        assert square(5) == 25

    if orig_value is None:
        os.environ.pop('NUMBA_DISABLE_JIT')
        importlib.reload(jit)
