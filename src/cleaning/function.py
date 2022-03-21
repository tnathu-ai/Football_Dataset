# import libraries general libraries
import pandas as pd
import numpy as np

# Modules for data visualization
import seaborn as sns
import matplotlib.pyplot as plt

import os

from scipy.stats import kurtosis, skew

pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', 200)

plt.rcParams['figure.figsize'] = [6, 6]

# ignore DeprecationWarning Error Messages
import warnings

warnings.filterwarnings('ignore')




def rename_cols(df):
    rename_cols = ['league_division', 'match_date', 'home_team', 'away_team', 
                                     'full_time_home_team_goals', 'full_time_away_team_goals', 'full_time_result', 'half_time_home_team_goals', 
                                     'half_time_away_team_goals', 'half_time_result', 'home_shots', 'away_shots', 
                                     'home_shots_on_target', 'away_shots_on_target', 'home_fouls_committed', 'away_fouls_committed', 
                                     'home_corners', 'away_corners', 'home_yellow_cards', 'away_yellow_cards', 'home_red_cards', 'away_red_cards', 'season']
    df.columns = rename_cols

def whitespace_remover(df):
    """
    The function will remove extra leading and trailing whitespace from the data.
    Takes the data frame as a parameter and checks the data type of each column.
    If the column's datatype is 'Object.', apply strip function; else, it does nothing.
    Use the whitespace_remover() process on the data frame, which successfully removes the extra whitespace from the columns.
    https://www.geeksforgeeks.org/pandas-strip-whitespace-from-entire-dataframe/
    """
    # iterating over the columns
    for i in df.columns:

        # checking datatype of each columns
        if df[i].dtype == 'str':

            # applying strip function on column
            df[i] = df[i].map(str.strip)
        else:
            # if condition is False then it will do nothing.
            pass




def profile_summary(dataset, plot=False):

    pf = pd.DataFrame({'Attribute': "",
                       'Type': "",
                       'Num. Missing Values': [],
                       'Num. Unique Values': [],
                       'Sknewness': [],
                       'Kurtosis': []
                       })

    rows = []

    for attribute in list(dataset.select_dtypes(include=[
            np.number]).columns.values):

        att_type = dataset[attribute].dtype

        unique_values = pd.unique(dataset[attribute])

        num_missing = sum(pd.isnull(dataset[attribute]))

        sk = skew(dataset[attribute].values, axis=None, nan_policy='omit')

        ct = kurtosis(dataset[attribute].values, axis=None, nan_policy='omit')

        row = [attribute, att_type, num_missing, len(unique_values), sk, ct]

        rows.append(row)

    for attribute in list(dataset.select_dtypes(exclude=[
            np.number]).columns.values):

        att_type = dataset[attribute].dtype

        unique_values = pd.unique(dataset[attribute])

        num_missing = sum(pd.isnull(dataset[attribute]))

        sk = "N/A"

        ct = "N/A"

        row = [attribute, att_type, num_missing, len(unique_values), sk, ct]

        rows.append(row)

    for row in rows:

        pf.loc[len(pf)] = row

        if plot:

            print("Frequency plot per attribute")

            for attribute in dataset.columns:

                unique_values = pd.unique(dataset[attribute])

                num_missing = sum(pd.isnull(dataset[attribute]))

                print('Attribute: %s\nNumber of unique values: %d\nNumber '
                      'of missing values: '
                      '%d\nUnique values:' %
                      (attribute, len(unique_values), num_missing))

                print('\nFrequency plot:\n')

                d = (pd.DataFrame(dataset[attribute].value_counts()))

                ax = sns.barplot(x="index", y=attribute,
                                 data=(d).reset_index())

                ax.set(xlabel=attribute, ylabel='count')

                ax.grid(b=True, which='major', color='w', linewidth=1.0)

                ax.set_xticklabels(
                    labels=d.sort_index().index.values, rotation=90)

                plt.show()

    print("Profiling datasets")

    print(pf.to_string())
    
    
def write_interim_path(df, csv_name, folder_name): 
    # set the path of the cleaned data to data 
    interim_data_path = os.path.join(os.path.pardir, '..', 'data','interim', folder_name)

    write_interim_path = os.path.join(interim_data_path, csv_name)
    
    # To write the data from the data frame into a file, use the to_csv function.
    df.to_csv(write_interim_path, index=False)
    print(f'cleaned {csv_name} data was successfully saved!\n\n\n')


    
    