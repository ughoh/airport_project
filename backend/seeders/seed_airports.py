from backend.app.models import AirportBase
from seed_all import seed_all

airport_data = [
    {"name": "John F. Kennedy International", "city": "New York", "country": "USA", "iata_code": "JFK", "icao_code": "KJFK"},
    {"name": "Heathrow", "city": "London", "country": "UK", "iata_code": "LHR", "icao_code": "EGLL"},
    {"name": "Haneda", "city": "Tokyo", "country": "Japan", "iata_code": "HND", "icao_code": "RJTT"},
    {"name": "Frankfurt", "city": "Frankfurt", "country": "Germany", "iata_code": "FRA", "icao_code": "EDDF"},
    {"name": "Charles de Gaulle", "city": "Paris", "country": "France", "iata_code": "CDG", "icao_code": "LFPG"},
    {"name": "Dubai International", "city": "Dubai", "country": "UAE", "iata_code": "DXB", "icao_code": "OMDB"},
    {"name": "Changi", "city": "Singapore", "country": "Singapore", "iata_code": "SIN", "icao_code": "WSSS"},
    {"name": "São Paulo–Guarulhos", "city": "São Paulo", "country": "Brazil", "iata_code": "GRU", "icao_code": "SBGR"},
    {"name": "O'Hare", "city": "Chicago", "country": "USA", "iata_code": "ORD", "icao_code": "KORD"},
    {"name": "Incheon", "city": "Seoul", "country": "South Korea", "iata_code": "ICN", "icao_code": "RKSI"},
]


async def seed_airports():
    await seed_all(AirportBase, airport_data)
