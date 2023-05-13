# Getting Started

## Installation

Nothing special here. Just use pip,

```bash
pip install psychonaut

# or, upgrade with,

pip install --upgrade psychonaut
```

Alternatively, if you only want the CLI and you have [`pipx`](https://pypa.github.io/pipx/) installed,

```bash
pipx install psychonaut

# or, upgrade with,
pipx upgrade psychonaut
```

If you want to develop the package locally, use [poetry](https://python-poetry.org/),

```
# Fetch
git clone https://github.com:jbn/psychonaut.git
cd psychonaut

# Install
poetry install

# Enter the virtualenv
poetry shell
```

## CLI Usage

Whether you used `pipx` or `pip`, you should now have the `psychonaut` command available. The first thing you should
do is configure the CLI with your credentials. You can do this by running,

```bash
psychonaut save-login you.bsky.social
```

which creates a file in your platform-dependent home directory. On Linux, this is `~/.psychonaut.json`.

Now you can use the CLI to do things like,

```bash
# Poast a new skeet.
psychonaut poast --image path_to_image.png 'hello, skeeters!'

# Get a users profile (as json)
psychonaut get-profile @you.bsky.social

# Get multiple users profiles (as json-lines)
psychonaut get-profile @you.bsky.social @me.bsky.social

# Get a users followers (as json lines)
psychonaut get-followers @you.bsky.social

# Get a users following (as json lines)
psychonaut get-following @you.bsky.social

# Get a user's DID
psychonaut resolve-handle @generativist.xyz
````


If you are interested in consuming the firehose, it 
can also do that,


```bash

# Save the firehose to binary segments like,
#
#    ./firehose-segments/YYYY-MM-DD/HH-MM-SS.length-prefixed
#
# with,
psychonaut repose-firehose-stream ./firehose-segments

# And replay them later to stdout with,
psychonaut replay-firehose-replay ./firehose-segments

# You can also combined the two with,
psychonaut repos-firehose-stream \
    --tee  \
    --tee-first-block-only \
    ./firehose-segments

# IF YOU USED AN EARLIER VERSION AND HAVE BASE64 ENCODED 
# SEGMENTS, YOU CAN CONVERT THEM TO LENGTH PREFIXED WITH,
psychonaut b64-dir-to-length-prefixed
```