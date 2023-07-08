import aiosqlite as sql

async def connect_to_db():
    db = await sql.connect('mydatabase.db')
    cur = await db.cursor()
    await cur.execute("""CREATE TABLE if not exists users (
                chatid TEXT
                )""")
    await db.commit()



class database:
    def __init__(self) -> None:
        self.db = None
        self.cur = None

    async def connect_to_db(self):
        self.db = await sql.connect('mydatabase.db')
        self.cur = await self.db.cursor()
        await self.cur.execute("""CREATE TABLE if not exists users (
                    chatid TEXT
                    )""")
        await self.db.commit()

    async def insert_user(self, user_id : str = None):
        if user_id != None:
            await self.cur.execute(""" SELECT * FROM users WHERE chatid = ? """, (user_id,))
            result = await self.cur.fetchall()
            if len(result) < 1:
                await self.cur.execute(""" INSERT INTO users ("chatid") VALUES (?) """, (user_id,))
            await self.db.commit()
            return {"status" : True}
        else: return {"status" : False}
