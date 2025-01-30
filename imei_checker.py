import aiohttp
from config import IMEI_API_KEY, IMEI_API_URL
import json


async def check_imei(imei):
    headers = {
        "Authorization": f"Bearer {IMEI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "deviceId": imei,
        "serviceId": 12
    })

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(IMEI_API_URL, headers=headers, data=payload) as response:
                if response.status == 403:
                    return {"error": "Ошибка 403: Доступ запрещен. Проверьте токен."}
                if response.status != 200:
                    return {"error": f"Ошибка {response.status}: {await response.text()}"}

                return await response.json()
        except Exception as e:
            return {"error": f"Ошибка соединения: {str(e)}"}
