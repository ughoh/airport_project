from backend.app import db_helper


async def seed_all(table, data):
    async with db_helper.session_factory() as session:
        result = await session.execute(table.__table__.select())
        existing = result.first()

        if not existing:
            session.add_all([table(**item) for item in data])
            await session.commit()
