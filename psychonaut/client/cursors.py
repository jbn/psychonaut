from psychonaut.api.session import Session


async def collect_cursored(
    sess: Session,
    req,
    resp_type,
    collection_k: str,
    cursor_key="cursor",
):
    cursor, last_cursor = None, None
    while True:
        req = req.copy(update={cursor_key: cursor})
        resp = await req.do_xrpc(sess)
        assert isinstance(resp, resp_type)
        cursor = resp.cursor

        new_items = getattr(resp, collection_k)
        for item in new_items:
            yield item

        if not cursor or cursor == last_cursor or not new_items:
            break

        last_cursor = cursor