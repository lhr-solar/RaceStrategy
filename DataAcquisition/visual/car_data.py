import pandas
import pandas as pd
import csv


class ParseData:
    # titles =['t','lap','pos_x','pos_y','x','v','a_long','a_lat','cell_temp','cell_soc','rotor_temp_f','rotor_heat_f','rotor_temp_r','rotor_heat_r','FIN','FON','RIN','RON','yaw','pitch','roll','field_weakening','frdf','fldf','rrdf','rldf','long_cf_f_inside','long_cf_f_outside','long_cf_r_inside','long_cf_r_outside','lat_cf_f_inside','lat_cf_f_outside','lat_cf_r_inside','lat_cf_r_outside','max_lat_force_f','max_long_force_f','max_lat_force_r','max_long_force_r','front_lat_force','front_long_force','rear_lat_force','rear_long_force','max_motor_power','motor_speed_limited','traction_limited','motor_eff','battery_Re','battery_heat_removed','cell_heat_w','battery_heat_w','battery_current','cell_current','battery_vout','power_battery','a_long_g','a_lat_g','dW_lon','dW_lat_f','dW_lat_r','dW_spr_f','dW_geo_f','dW_uns_f','dW_spr_r','dW_geo_r','dW_uns_r','dW_spr_x','dW_geo_x','dW_uns_rx','dW_uns_fx','weight','motor_torque','motor_rpm','power_driving','power_motor','power_inverter','motor_heat_w','inv_heat_w','downforce','dragforce','sideforce','v_mph']
    def __init__(self,filename):
        self.data = pandas.read_csv(filename)
        self.titles = self.data.columns.values.tolist()

    # selects rows over a range of values specified by lower_bound and upper_bound
    # stored in a dictonary where the key is the name of the data ex: battery_current, sideforce
    # def get_range(self, lower_bound, upper_bound, column_name):
    #     my_dict = {}
    #     selected = self.data.loc[(self.data[column_name] >= lower_bound) &
    #                         (self.data[column_name] <= upper_bound)]
    #
    #     for index in range(len(self.titles)):
    #         selected = self.data.loc[(self.data[column_name] >= lower_bound) &
    #                             (self.data[column_name] <= upper_bound)]
    #         selected = selected.iloc[:, index].tolist()
    #         current_title = self.titles[titleindex]
    #         index = index + 1
    #         titleindex = titleindex + 1
    #         my_dict[current_title] = selected
    #     return (my_dict)


    # selects row over a range of values specified by value and returns a dictionary with the value stored where the key is the name of the data
    # ex: battery_current, sideforce
    # def get_values(self, value, column_name):
    #     my_dict = {}
    #     for i in range(self.titles):
    #         selected = self.data.loc[(self.data[column_name] == value)]
    #         selected = selected.iloc[:, i].tolist()
    #         current_title = self.titles[titleindex]
    #         iindex = iindex + 1
    #         titleindex = titleindex + 1
    #         my_dict[current_title] = selected
    #     return (my_dict)

    # returns all the values in the column in a list
    def get_var(self, column_name):
        col = self.data[column_name]
        vals = col.tolist()
        return vals

    # gets a single return value given a column name and value
    def get_single_value(self, search_col_name, value, res_col_name):
        selected = self.data.loc[(self.data[search_col_name] == value)]
        i = 0
        while res_col_name != self.titles[i]:
            i = i + 1
        value = selected.iloc[:, i]
        return (selected)



