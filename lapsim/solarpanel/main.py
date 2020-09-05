# solar panel power calculations
"""The solar panel output calculator.

Calculates solar panel output by using the size and efficiency of the solar panels. This also takes 
cloud coverage into account and subtracts for small bits of likely error in hardware. It also uses 
the current location which in this case is assumed to be Austin but should be changed if not since this
data could not be scraped easily. Map of solar data can be found here: https://maps.nrel.gov/nsrdb-viewer/

    Typical usage example:

    recharge_rate = main()
"""

from bs4 import BeautifulSoup
import requests

# Small web scraping for cloud coverage
# Analying clouds: https://www.weather.gov/bgm/forecast_terms
def cloud_coverage():
    """Returns cloud coverage in the sky times 0.8 so that this can be easily imported into the performance ratio function.
    """
    request = requests.get("https://weather.com/weather/today/l/7472a7bbd3a7454aadf596f0ba7dc8b08987b1f7581fae69d8817dffffc487c2")
    soup = BeautifulSoup(request.content, 'html.parser')
    cloud_condition = soup.find('div', class_='_-_-node_modules-@wxu-components-src-organism-CurrentConditions-CurrentConditions--CurrentConditions--2_Nmm').get_text()

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
    else:
        print("WARNING: Some sort of rain, inaccurate cloud coverage estimation.")
        cloud_percent = 0.375 #if rainy, hard to calculate clouds
    
    print(f"Approximate Cloud Coverage: {cloud_percent*100} %")
    cloud_percent = cloud_percent * 0.8
    return cloud_percent

def PR_calculation():
    """Returns the solar panel's performance ratio based on cloud coverage and other assumed places of error.
    """
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
    """Calculates the solar panel's output using multiple different components.

    Returns:
        Solar panel output (energy), in kWh.
    """
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
    # % = energy/area 
    # energy ~ 1kW, 1/4 = 0.25 = 25% 
    sp_power_percent = 0.25

    A = sp_surface_area
    r = sp_power_percent
    H = 5.2 #constant

    # this one might also take trial and error to solve for, PR doesn't necessarily have a set value and is
    # used to calculate how close to actual input the solar panels are (higher is better) 
    PR = PR_calculation()
    #PR = 1.00 # turn this on for perfect conditions
    print(f"Performance Ratio: {round(PR*100, 2)} %\n")

    energy = A * r * H * PR

    print(f"Roughly {round(energy, 4)} kWh/day")
    hourly_energy = round(energy / 5.2, 4)
    print(f"In 5.2 hours of peak sunlight, roughly {hourly_energy} kWh")

    return hourly_energy


if __name__ == "__main__":
    main()
