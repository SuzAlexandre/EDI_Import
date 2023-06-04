# This is a sample Python script.
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import sqlite3


def set_database_structure():
    # here to create new database structure in order to save all assignments
    connection_obj = sqlite3.connect('machining_capacity.db')

    # cursor object
    cursor_obj = connection_obj.cursor()

    # Drop the GEEK table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS program_list")

    # Creating table
    table = """ CREATE TABLE GEEK (
                Email VARCHAR(255) NOT NULL,
                First_Name CHAR(25) NOT NULL,
                Last_Name CHAR(25),
                Score INT
            ); """

    cursor_obj.execute(table)

    print("Table is Ready")

    # Close the connection
    connection_obj.close()
    pass

def daily_output(cycle_time, parts_per_cycle, open_time_minutes=3*7.5*60, oee=0.8, assignment_level=1):
    # Calculate daily output based on oee
    # cycle time is in seconds
    # oee is a percentage

    # in case oee provided is over 1
    while oee > 1:
        oee = oee/100

    # in case the oee is negative, will add a standard value of 80%
    if oee < 0:
        oee = .80

    capacity = int(open_time_minutes * 60 * oee * parts_per_cycle / cycle_time)*assignment_level

    return capacity



def update_production_plan():
    pass


def calculate_capacity():
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # define test length
    length = 365

    # periods means how many dates you want
    date_list = pd.date_range(start=datetime.today(),
                              periods=length,
                              freq='D')

    date_list = pd.to_datetime(date_list)

    # Create here a data frame example
    data = {'Shipment Date': date_list,
            'edi_requirements': np.random.randint(0, 1200, length),
            'daily_capacity': [daily_output(600, 4)]*length}

    print(f'Daily output: {daily_output(600, 4)} sets per day')

    # Create the pandas DataFrame with column name is provided explicitly
    df = pd.DataFrame(data)

    # calculate sum of values, grouped by week
    weekly = df.groupby(pd.Grouper(key='Shipment Date', freq="M")).sum()  # DataFrameGroupBy (grouped by Month)
    weekly.index = weekly.index.strftime('%B')

    # setup plot size
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # create plot
    fig, ax = plt.subplots()

    # adding plots
    weekly['edi_requirements'].plot(kind='bar', color='red')
    weekly['daily_capacity'].plot(kind='line', marker='.', color='black', ms=10)
    plt.xticks(rotation=90)  # Rotates X-Axis Ticks by 45-degrees

    plt.show()
