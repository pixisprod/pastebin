from httpx import AsyncClient


class NgrokManager:
    def __init__(self, http_client: AsyncClient, ngrok_api_url: str):
        self.__api_url = ngrok_api_url
        self.__http_client = http_client
        self.__http_client.base_url = self.__api_url


    async def create_tunnel(
        self, 
        address: str, 
        protocol: str, 
        name: str,
    ) -> str:
        r = await self.__http_client.post(
            url=f'/api/tunnels',
            json={
                'addr': address,
                'proto': protocol,
                'name': name,
            }
        )
        r.raise_for_status()
        return r.json()['public_url']
    

    async def close(self):
        await self.__http_client.aclose()