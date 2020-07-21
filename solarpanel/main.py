# solar panel power calculations

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
    # all of these values are approximate
    # TODO: find specifics, if available, about specific effects from above
    cloud_coverage = 0.30 # %
    inverter_loss = 0.05 # %
    dc_loss = 0.02 # %
    ac_loss = 0.02 # %
    weak_radiation = 0.03 # %
    dust_loss = 0.02 # %
    etc_loss = 0.01 # %

    PR = 1 * (1-cloud_coverage) * (1-inverter_loss) * (1-dc_loss) * (1-ac_loss) * (1-weak_radiation) * (1-dust_loss) * (1-etc_loss)
    PR = round(PR, 5)
    print(f"{PR} is the PR")
    return PR

def main():
    '''
    E = A * r * H * PR

    E = Energy                  (kW)
    A = surface area            (m^2)
    r = efficiency rating       (%)
    H = global radiation value  (kWh/m^2/hr)
    PR = performance ratio

    https://solarmonsters.com/help-advice/solar-panels-advice/how-many-kwh-does-a-solar-panel-produce/#tab-con-9
    '''

    sp_power_rating = 20    # (watts)
    sp_surface_area = 100   # (m^2)

    A = sp_surface_area
    r = sp_power_rating / sp_surface_area
    H = 0.217
    # this one might also take trial and error to solve for, PR doesn't necessarily have a set value and is
    # used to calculate how close to actual input the solar panels are (higher is better) 
    PR = PR_calculation()

    Energy = A * r * H * PR
    Energy = round(Energy, 5)

    print (f"{Energy} kWh produced")

main()
