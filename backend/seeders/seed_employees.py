from backend.app.models import EmployeesBase, Departaments
from seed_all import seed_all

employees_data = [
    {
        "first_name": "Anna",
        "last_name": "Kovalchuk",
        "position": "Security Officer",
        "departament": Departaments.security,
        "contact_info": "+380501234567"
    },
    {
        "first_name": "Dmytro",
        "last_name": "Shevchenko",
        "position": "Check-In Agent",
        "departament": Departaments.check_in,
        "contact_info": "+380931234567"
    },
    {
        "first_name": "Iryna",
        "last_name": "Melnyk",
        "position": "Boarding Agent",
        "departament": Departaments.boarding,
        "contact_info": "+380671234567"
    },
    {
        "first_name": "Oleh",
        "last_name": "Bondarenko",
        "position": "Maintenance Engineer",
        "departament": Departaments.maintenance,
        "contact_info": "+380631234567"
    },
    {
        "first_name": "Yulia",
        "last_name": "Kravets",
        "position": "ATC Specialist",
        "departament": Departaments.air_traffic_control,
        "contact_info": "+380661234567"
    },
    {
        "first_name": "Serhii",
        "last_name": "Tkachenko",
        "position": "Baggage Handler",
        "departament": Departaments.baggage,
        "contact_info": "+380681234567"
    },
    {
        "first_name": "Olena",
        "last_name": "Lysenko",
        "position": "Customs Officer",
        "departament": Departaments.customs,
        "contact_info": "+380991234567"
    },
    {
        "first_name": "Mykola",
        "last_name": "Petrenko",
        "position": "Cleaner",
        "departament": Departaments.cleaning,
        "contact_info": "+380951234567"
    },
    {
        "first_name": "Kateryna",
        "last_name": "Sydorenko",
        "position": "Administrator",
        "departament": Departaments.administration,
        "contact_info": "+380441234567"
    },
    {
        "first_name": "Volodymyr",
        "last_name": "Ivanov",
        "position": "Catering Manager",
        "departament": Departaments.catering,
        "contact_info": "+380721234567"
    }
]


async def seed_employees():
    await seed_all(EmployeesBase, employees_data)
