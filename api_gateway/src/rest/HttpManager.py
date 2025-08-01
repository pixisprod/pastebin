from httpx import AsyncClient, Response


class HttpManager:
    def __init__(self):
        self.__client = AsyncClient()
    

    async def get(self, url: str) -> Response:
        r = await self.__client.get(url)
        return r
    

    async def post(self, url: str, body: dict) -> Response:
        r = await self.__client.post(url, json=body)
        return r
    

    async def delete(self, url: str) -> Response:
        r = await self.__client.delete(url)
        return r
    

    async def patch(self, url: str, body: dict) -> Response:
        r = await self.__client.patch(url, json=body)
        return r

    async def close(self):
        await self.__client.aclose()
