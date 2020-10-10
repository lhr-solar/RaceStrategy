import os
import inputs

import pandas as pd


user_inputs = inputs.get_inputs()
strat_list = user_inputs['strategy'].split(",") # account for commas
if ("all" in strat_list[0].lower()):
    directory_path = os.path.dirname(os.path.abspath(__file__)) 
    new_path = os.path.join(directory_path, "stratlist.txt")
    
    strat_list.clear()
    with open(new_path) as f: # read from input.txt
        lines = f.readlines()
        for line in lines:
            strat_list.append(line.strip() + ".csv")
    f.close()

csv_files = []
# index = 0
for csv in strat_list:
    csv_files.append(pd.read_csv(csv))
    # index = index + 1

main_df = pd.concat(csv_files, axis=1)

print(main_df)

main_df.to_csv('sim.csv', index=False)   

