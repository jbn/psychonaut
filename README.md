![Tests](https://github.com/jbn/psychonaut/actions/workflows/test.yaml/badge.svg)
[![Docs](https://readthedocs.org/projects/psychonaut/badge/?version=latest)](https://psychonaut.readthedocs.io/en/latest/?badge=latest)

![Psychonaut helmet](./psychonaut_logo.png "A helmet for the psychonaut")


# PROGRESS REPORT

- [ ] Finish pydantic validation for reference types

# What is this?

An async python sdk for Bluesky.

I used to do a pretty absurd amount of experiments with twitter's api. But musk
has decided to turn that platform into a pay-for-play version of LinkedIn
and banished all the tinkerers. So, now I'm here.

It has a bit of a weird structure. You basically do things like,

```python
async with get_simple_client_session() as sess:
    posts: GetPostsResp = await GetPostsReq(uris=[...]).do_xrpc(sess)
    ...
```

which feels backwards from the expected,

```python
async with get_simple_client_session() as sess:
    posts: GetPostsResp = await sess.do_xrpc(GetPostsReq(uris=[...]))
```

or even,

```python
async with get_simple_client_session() as sess:
    posts: GetPostsResp = await sess.get_posts(uris=[...])
```

It's kinda an artifact of the way I did code generation but I kinda like it
and fuck it S-expressions worked so there is a (completely nonsensical)
precedence. 

**And, just to clarify, every request and response gets validated against the lexicon schema**, 
which is nice (although reference types are still a WIP). Moreover, the 
generated code is auto-complete/copilot friendly. And, in theory, you could override
`do_xrpc` to do clever things like caching, instead of hacking each particular api call.

But mostly I'm lazy so this is how it is.

# Should I use this?

~~Almost certainly not. Right now it's a bucket of slop. I offer no 
guarantees about the stability of the API, the correctness of the
implementation, or the quality of the documentation.~~

If you want to use it, go ahead.

Every single api call exists with Pydantic models for requests and responses
(but with a few outstanding validations missing).

It's still unstable but I've been using it pretty regularly.

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

### Firehose

**EXTREMELY EXPERIMENTAL AND STILL NOT FINISHED**

`repos-firehose-stream` saves the raw messages for subsequent replay so you
can at least collect now and i'll get the json emit / validation working
later.

```bash
# Stream the firehose
psychonaut repos-firehose-stream stream_dir

# Stream the firehose but print to stdout too
psychonaut repos-firehose-stream --tee stream_dir

# Replay serialized
psychonaut repos-firehose-replay stream_dir

# Replay serialized file
psychonaut repos-firehose-replay stream_dir/your_stream.b64-lines
```

# How is this made?

Initially, this was a collaboration between the [atproto repo](https://github.com/bluesky-social/atproto),
me, and my friend ChatGPT (using GPT-4). I had been toying around with this 
automatic `langa`<->`langb` transpiler in [langchain](https://github.com/hwchase17/langchain).
My original goal was to jointly build that while making my python client from the `atproto`
repo. However, the fine folks at OpenAI didn't give me 
GPT-4 API access, and GPT-3 isn't quite good enough to do the job. So instead, 
this was me testing the fences "manually" (with ChatGPT). And now it's *just*
me.

This also means this project was a bit...like theft? IDK. 

Question of the generative hour: where is the boundary?

# See Also (for pythonistas)

- [arroba](https://github.com/snarfed/arroba) 
- [lexrpc](https://github.com/snarfed/lexrpc) 
- [atprotools](https://github.com/ianklatzco/atprototools) 