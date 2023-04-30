# Notes

## `black` processing

This isn't optional because it's just got good properties. But for the 
purpose of debugging, it also will fail loudly for bad syntax.

## `--remove_existing` flag

Removes the existing generated code before generating new code. This is 
helpful because intermediate files are not removed when the generator
fails, so it's somewhat debuggable.

## `--import-all-test` flag

After generating all the code, if this flag is set, the generator tries to
import each generated module. If it can't do this, something has gone wrong
so it will print out which failures and then raise an exceptino.

## TODO

- [ ] Fail the unit test if the generated code does not match what was commited.