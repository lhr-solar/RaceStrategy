# solar panel power calculations
"""The solar panel output calculator.

Calculates solar panel output by using the size and efficiency of the solar panels. This also takes 
cloud coverage into account and subtracts for small bits of likely error in hardware. It also uses 
the current location which in this case is assumed to be Austin but should be changed if not since this
data could not be scraped easily. Map of solar data can be found here: https://maps.nrel.gov/nsrdb-viewer/

    Typical usage example:

    recharge_rate = main()
"""

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests


def time_mult(start, end, starting_time, labels):
    all_times = []

    for i in range(start, end):
        if(starting_time == "normal"):
            time = labels[i % 12].find("h2", class_="DetailsSummary--daypartName--2FBp2").get_text()
        else:
            time = starting_time

        if(time == "11 am" or time == "12 pm" or time == "1 pm" or time == "2 pm" or time == "3 pm"):
            time_mult = 1
        elif(time == "10 am" or time == "4 pm"):
            time_mult = 0.75
        elif(time == "9 am" or time == "5 pm"):
            time_mult = 0.5
        elif(time == "8 am" or time == "6 pm"):
            time_mult = 0.25
        else:
            time_mult = 0

        all_times.append(time_mult)
    
    return all_times



# Small web scraping for cloud coverage
# Analying clouds: https://www.weather.gov/bgm/forecast_terms
def cloud_coverage(cloud_data, start, end, labels):
    """Returns cloud coverage in the sky times 0.8 so that this can be easily imported into the performance ratio function.
    """

    total_cloud = []

    for i in range(start, end):
        cloud_condition = labels[i % 12].find("span", class_="DetailsSummary--extendedData--365A_").get_text()

        # These are approximate values as finding an actual percent to scrape didn't yeild much luck
        if cloud_data == 1:
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
                # print("WARNING: Some sort of rain, inaccurate cloud coverage estimation.")
                cloud_percent = 0.375
        else:
            cloud_percent = cloud_data

        cloud_percent = cloud_percent * 0.8

        total_cloud.append(cloud_percent)

    return total_cloud
        
    

def PR_calculation(cloud_data, start, end, labels):
    """Returns the solar panel's performance ratio based on cloud coverage and other assumed places of error.
    """
    '''
    PR:
    - Inverter losses (4% to 10 %)
    - Temperature losses (5% to 20%)
    - DC cables losses (1 to 3 %)
    - AC cables losses (1 to 3 %)
    - Shadings 0 % to 80% !!! (specific to each site)l
    - Losses at weak radiation 3% to 7%
    - Losses due to dust, snow... (2%)
    - Other Losses (?)

    https://photovoltaic-software.com/principle-ressources/how-calculate-solar-energy-power-pv-systems
    '''

    total_PR = []

    # All these values are percentages
    # TODO: find specifics, if available, about specific effects from above
    cloud_coverage_data = cloud_coverage(cloud_data, start, end, labels)

    for i in range(start, end):
        prdata = {
            "cloud_coverage": cloud_coverage_data[i],
            "inverter_loss": 0.04,
            "dc_loss": 0.01,
            "ac_loss": 0.01,
            "weak_radiation": 0.03,
            "dust_loss": 0.02,
            "etc_loss": 0.01
        }

        PR = 1 #perfect conditions
        for itm in prdata:
            PR *= (1-prdata[itm])

        total_PR.append(PR)

    return total_PR

def main(cloud_data, starting_time, start, end):
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

    request = requests.get("https://weather.com/weather/hourbyhour/l/7472a7bbd3a7454aadf596f0ba7dc8b08987b1f7581fae69d8817dffffc487c2")
    soup = BeautifulSoup(request.content, 'html.parser')
    labels = soup.find_all("summary", class_="Disclosure--Summary--UuybP DaypartDetails--Summary--3IBUr Disclosure--hideBorderOnSummaryOpen--ZdSDc")

    A = 4       # (m^2)
    r = 0.25    # energy ~ 1kW, 1/4 = 0.25 = 25%
    H = 5.2     #constant
    PR = PR_calculation(cloud_data, start, end, labels)

    time_multiplier = time_mult(start, end, starting_time, labels)

    total_energy = []

    for i in range(start, end):
        energy = A * r * H * PR[i] * time_multiplier[i]

        # print("\nWEATHER UPDATE:")
        # print(f"Roughly {round(energy, 4)} kWh/day")
        hourly_energy = round(energy / 5.2, 4)
        # print(f"In 5.2 hours of peak sunlight, roughly {hourly_energy} kWh")

        total_energy.append(hourly_energy)
    
    return total_energy


if __name__ == "__main__":
    main()
