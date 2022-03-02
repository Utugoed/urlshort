from app.db.connection import get_db


class Redirects:
    @staticmethod
    async def insert_redirect(link: str, ip: str):
        db = await get_db()
        redirects = db.redirects
        await redirects.insert_one({"link": link, "ip": ip})
