# solar panel power calculations

from bs4 import BeautifulSoup
import requests

# Small web scraping for cloud coverage
# Analying clouds: https://www.weather.gov/bgm/forecast_terms
def cloud_coverage():
    request = requests.get("https://weather.com/weather/today/l/7472a7bbd3a7454aadf596f0ba7dc8b08987b1f7581fae69d8817dffffc487c2")
    soup = BeautifulSoup(request.content, 'html.parser')
    cloud_condition = soup.find('div', class_='_-_-components-src-organism-CurrentConditions-CurrentConditions--phraseValue--mZC_p').get_text()

    # These are approximate values as finding an actual percent to scrape didn't yeild much luck
    if cloud_condition == "Clear" or cloud_condition == "Sunny":
        cloud_percent = 0.00
    elif cloud_condition == "Mostly Clear" or cloud_condition == "Mostly Sunny":
        cloud_percent = 0.125
    elif cloud_condition == "Partly Cloudy" or cloud_condition == "Partly Sunny":
        cloud_percent = 0.375
    elif cloud_condition == "Mostly Cloudy":
        cloud_percent = 0.625
    elif cloud_condition == "Cloudy":
        cloud_percent = 0.875
    
    print(f"Approximate Cloud Coverage: {cloud_percent*100} %")
    cloud_percent = cloud_percent * 0.8
    return cloud_percent

def PR_calculation():
    '''
    PR:
    - Inverter losses (4% to 10 %)
    - Temperature losses (5% to 20%)
    - DC cables losses (1 to 3 %)
    - AC cables losses (1 to 3 %)
    - Shadings 0 % to 80% !!! (specific to each site)
    - Losses at weak radiation 3% to 7%
    - Losses due to dust, snow... (2%)
    - Other Losses (?)

    https://photovoltaic-software.com/principle-ressources/how-calculate-solar-energy-power-pv-systems
    '''
    # All these values are percentages
    # TODO: find specifics, if available, about specific effects from above
    prdata = {
        "cloud_coverage": cloud_coverage(),
        #"cloud_coverage": 0.05, #this is theoretical maximum
        "inverter_loss": 0.04,
        "dc_loss": 0.01,
        "ac_loss": 0.01,
        "weak_radiation": 0.03,
        "dust_loss": 0.02,
        "etc_loss": 0.01
    }

    PR = 1 #perfect conditions
    for itm in prdata:
        PR = PR * (1-prdata[itm])

    return PR

def main():
    '''
    E = A * r * H * PR

    E = Energy                  (kWh)
    A = surface area            (m^2)
    r = efficiency rating       (%)
    H = global radiation value  (kWh/m^2/hr)
    PR = performance ratio

    https://solarmonsters.com/help-advice/solar-panels-advice/how-many-kwh-does-a-solar-panel-produce/#tab-con-9
    '''

    sp_surface_area = 4       # (m^2)
    sp_power_percent = 0.20   # %

    A = sp_surface_area
    r = sp_power_percent
    H = 0.217 #constant

    # this one might also take trial and error to solve for, PR doesn't necessarily have a set value and is
    # used to calculate how close to actual input the solar panels are (higher is better) 
    PR = PR_calculation()
    #PR = 1.00 # (when all circumstances are perfect)
    print(f"Performance Ratio: {round(PR*100, 2)} %\n")


    energy = A * r * H * PR

    print(f"{round(energy, 4)} kWh produced")
    total_energy = energy * 6
    print(f"6 hours of sunlight yields {round(total_energy, 4)} kW, or {round(total_energy * 1000, 1)} W")

main()
