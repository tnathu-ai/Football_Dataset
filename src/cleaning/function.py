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


def style(table):
    """
    quick styling
    style: https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.background_gradient.html
    color: https://matplotlib.org/stable/tutorials/colors/colormaps.html
    """
    view = table.style.background_gradient(cmap='Pastel1')
    return view

def rename_cols(df):
    rename_cols = ['league_division', 'match_date', 'home_team', 'away_team', 
                                     'full_time_home_team_goals', 'full_time_away_team_goals', 'full_time_result', 'half_time_home_team_goals', 
                                     'half_time_away_team_goals', 'half_time_result', 'referee', 'home_shots', 'away_shots', 
                                     'home_shots_on_target', 'away_shots_on_target', 'home_fouls_committed', 'away_fouls_committed', 
                                     'home_corners', 'away_corners', 'home_yellow_cards', 'away_yellow_cards', 'home_red_cards', 'away_red_cards', 
                                     'bet365_home_win_odds', 'bet365_draw_odds', 'bet365_away_win_odds', 
                                     'bet&win_home_win_odds', 'bet&win_draw_odds', 'bet&win_away_win_odds', 
                                     'interwetten_home_win_odds', 'interwetten_draw_odds', 'interwetten_away_win_odds', 
                                     'ladbrokes_home_win_odds', 'ladbrokes_draw_odds', 'ladbrokes_away_win_odds', 
                                     'pinnacle_home_win_odds', 'pinnacle_draw_odds', 'pinnacle_away_win_odds', 
                                     'william_hill_home_win_odds', 'william_hill_draw_odds', 'william_hill_away_win_odds', 
                                     'vc_bet_home_win_odds', 'vc_bet_draw_odds', 'vc_bet_away_win_odds', 
                                     'no_betbrain_bookmakers_calculated_odds_averages_maximums', 
                                     'betbrain_maximum_home_win_odds', 'betbrain_average_home_win_odds', 'betbrain_maximum_draw_odds', 
                                     'betbrain_average_draw_win_odds', 'betbrain_maximum_away_win_odds', 'betbrain_average_away_win_odds', 
                                     'no_betbrain_bookmakers_calculated_over/under_2.5_goals_averages_maximums', 
                                     'betbrain_maximum_over_2.5_goals', 'betbrain_average_over_2.5_goals', 'betbrain_maximum_under_2.5_goals', 
                                     'betbrain_average_under_2.5_goals', 'no_betbrain_bookmakers_asian_handicap_averages_maximums', 
                                     'betbrain_size_handicap_home', 'betbrain_maximum_asian_handicap_home_odds', 'betbrain_average_asian_handicap_home_odds', 
                                     'betbrain_maximum_asian_handicap_away_odds', 'betbrain_average_asian_handicap_away_odds', 'PSCH', 'PSCD', 'PSCA']
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


"""
 Impute missing values by taking category-specific numerical and categorical imputations
 Credit: https://towardsdatascience.com/pandas-tricks-for-imputing-missing-data-63da3d14c0d6
 """


def impute_numerical(df, categorical_column, numerical_column):
    frames = []
    # within a for-loop we can define column-specific data frames:
    for i in list(set(df[categorical_column])):
        df_category = df[df[categorical_column] == i]
        # we can fill the missing values in these column-specific data frames with their respective median of numerical column:
        if len(df_category) > 1:
            # checking the length of the data frame within the for loop
            # imputing with the column-specific median if the length is greater than one
            df_category[numerical_column].fillna(df_category[numerical_column].median(), inplace=True)
        else:
            # If the length is equal to 1 we impute with the median across all countries
            df_category[numerical_column].fillna(df[numerical_column].median(), inplace=True)
        # We then append the result to a list we’ll call “frames”
        frames.append(df_category)
        final_df = pd.concat(frames)
    return final_df


def impute_categorical(df, categorical_column1, categorical_column2):
    cat_frames = []
    for i in list(set(df[categorical_column1])):
        df_category = df[df[categorical_column1] == i]
        if len(df_category) > 1:
            df_category[categorical_column2].fillna(df_category[categorical_column2].mode()[0], inplace=True)
        else:
            df_category[categorical_column2].fillna(df[categorical_column2].mode()[0], inplace=True)
        cat_frames.append(df_category)
        # concatenate the resulting list of data frames:
        cat_df = pd.concat(cat_frames)
    return cat_df




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
    
    
def write_interim_path(df, csv_name): 
    # set the path of the cleaned data to data 
    interim_data_path = os.path.join(os.path.pardir, '..', 'data','interim', 'national_leagues')

    write_interim_path = os.path.join(interim_data_path, csv_name)
    
    # To write the data from the data frame into a file, use the to_csv function.
    df.to_csv(write_interim_path, index=False)
    print(f'cleaned {csv_name} data was successfully saved!\n\n\n')