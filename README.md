![Tests](https://github.com/jbn/psychonaut/actions/workflows/test.yaml/badge.svg)


![Psychonaut helmet](./psychonaut_logo.png "A helmet for the psychonaut")


# PROGRESS REPORT

- [x] Parse the Lexicons with PyDantic
- [ ] Generate code from the Lexicons
    - [x] Generate files
    - [ ] Generate Fields from full Lexicon spec
        - [x] Generate code for queries
        - [ ] Generate code for records
        - [ ] Generate code for the procedures
    - [ ] Generate f: (Session, Req) -> Resp helper functions

# What is this?

An async python client for Bluesky.

I used to do a pretty absurd amount of experiments with twitter's api. But musk
has decided to turn that platform into a pay-for-play version of LinkedIn
and banished all the tinkerers. So, now I'm here.

# Should I use this?

Almost certainly not. Right now it's a bucket of slop. I offer no 
guarantees about the stability of the API, the correctness of the
implementation, or the quality of the documentation. 

If you want to use it, go ahead,

```bash
# In your venv or mamba env or whatever
pip install psychonaut
```

to use it as a library. This also installs the `psychonaut` command line tool.

```bash
psychonaut --help

# Temporary login
export BSKY_USERNAME=yourusername
export BSKY_PASSWORD=yourpassword

# Permanent login (~/.psychonaut.json)
psychonaut save-login yourusername 

psychonaut poast "hey look, an annoying cron job"
```

But definitely be mindful of the version because I'm going to break your code.

Alternatively, just use [pipx](https://pypa.github.io/pipx/)

```bash
pipx install psychonaut

export BSKY_USERNAME=yourusername
export BSKY_PASSWORD=yourpassword

psychonaut poast "hell yea, pipx"
```

# How is this made?

This is a collaboration between the [atproto repo](https://github.com/bluesky-social/atproto),
me, and my friend ChatGPT (using GPT-4). I've been toying around with this 
automatic `langa`<->`langb` transpiler in [langchain](https://github.com/hwchase17/langchain).
My original goal was to jointly build that while making my python client from the `atproto`
repo. However, the fine folks at OpenAI have decided to *still* not grant me access to 
GPT-4 in the API, and GPT-3 isn't quite good enough to do the job. So instead, 
this was me testing the fences "manually" (with ChatGPT.)

This also means this project is a bit...like theft? IDK. 

Question of the generative hour: where is the boundary?

# See Also (for pythonistas)

- [lexrpc](https://github.com/snarfed/lexrpc) (almost certainly better designed then mine)
- [atprotools](https://github.com/jbn/psychonaut/) *unstable*