import asyncio
from datetime import datetime
from typing import Any, Dict, Optional
import aiohttp
from pydantic import BaseModel
from contextlib import asynccontextmanager


@asynccontextmanager
async def retires_on_timeout(max_retries: int = 3):

    for i in range(max_retries):
        try:
            yield
            return
        except asyncio.TimeoutError as e:
            print(f"TimeoutError {i}: {e}")
            continue

    raise aiohttp.ClientTimeoutError(f"TimeoutError after {max_retries} retries")

class Session:
    def __init__(self, factory, username: str, access_jwt: str, did: str):
        self.factory = factory
        self.username = username
        self.access_jwt = access_jwt
        self.did = did

    @property
    def http(self):
        return self.factory.http_session

    async def query(self, req, max_retries=3) -> Dict[Any, Any]:
        endpoint = self.factory.atp_host + f"/xrpc/{req.xrpc_id}"

        # TODO: when?
        headers = {"Authorization": f"Bearer {self.access_jwt}"}
        params = req.dict(exclude_none=True)
        #headers = None

        async with retires_on_timeout(max_retries=max_retries):
            async with self.http.get(endpoint, params=params, headers=headers) as resp:
                resp.raise_for_status()

                doc = await resp.json()

                if "error" in doc:
                    raise Exception(doc["error"])

                return doc

    async def record(self, req) -> Dict[Any, Any]:
        endpoint = self.factory.atp_host + "/xrpc/com.atproto.repo.createRecord"
        headers = {"Authorization": f"Bearer {self.access_jwt}"}

        record = req.dict(exclude_none=True)
        if "createdAt" not in record:
            record["createdAt"] = datetime.utcnow().isoformat()
        if "$type" not in record:
            record["$type"] = req.xrpc_id

        req_data = {
            "collection": req.xrpc_id,
            "$type": req.xrpc_id,
            "repo": self.did,
            "record": record
        }

        async with retires_on_timeout():
            async with self.factory.http_session.post(
                endpoint, json=req_data, headers=headers, timeout=60
            ) as resp:
                resp.raise_for_status()

                doc = await resp.json()

                if "error" in doc:
                    raise Exception(doc["error"])

                return doc


class SessionFactory(BaseModel):
    atp_host: str
    http_session: aiohttp.ClientSession

    async def create(self, username: str, password: str):
        data = {"identifier": username, "password": password}

        endpoint = self.atp_host + "/xrpc/com.atproto.server.createSession"
        async with self.http_session.post(endpoint, json=data) as resp:
            doc = await resp.json()

        if "error" in doc:
            raise Exception(doc["error"])

        return Session(self, username, doc["accessJwt"], doc["did"])

    class Config:
        arbitrary_types_allowed = True
