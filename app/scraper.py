# Placeholder 'scraper' that would normally fetch data from the web.
# Here we just simulate returning hospital & disease info.
def get_hospital_info():
    return [
        {"name": "City General Hospital", "beds": 220, "icu_beds": 20, "location": "Downtown"},
        {"name": "Green Valley Clinic", "beds": 40, "icu_beds": 2, "location": "Green Valley"},
    ]

def get_disease_facts(disease: str):
    facts = {
        "flu": "Flu is a contagious respiratory illness caused by influenza viruses.",
        "covid-19": "COVID-19 is caused by SARS-CoV-2; vaccination reduces severe disease.",
    }
    return facts.get(disease.lower(), "No facts available.")
