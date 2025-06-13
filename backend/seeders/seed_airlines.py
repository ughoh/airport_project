from backend.app.models import AirlineBase
from seed_all import seed_all

airline_data = [
    {"name": "SkyFly", "code": 101, "country": "USA"},
    {"name": "EuroWings", "code": 102, "country": "Germany"},
    {"name": "AirNova", "code": 103, "country": "Canada"},
    {"name": "PacificAir", "code": 104, "country": "Australia"},
    {"name": "FlyAsia", "code": 105, "country": "Japan"},
    {"name": "TransAtlantic", "code": 106, "country": "UK"},
    {"name": "SaharaAir", "code": 107, "country": "Morocco"},
    {"name": "NordicJet", "code": 108, "country": "Sweden"},
    {"name": "AeroLatina", "code": 109, "country": "Brazil"},
    {"name": "SilkRoute Airways", "code": 110, "country": "India"},
]


async def seed_airlines():
    await seed_all(AirlineBase, airline_data)