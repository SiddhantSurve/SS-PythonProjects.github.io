# required packages are imported
import pandas as pd
import time
import calendar
import numpy as np
import datetime
import sys


def getting_dow(str_date):
    # This function returns the weekday by applying the .weekday method to the sliced components (yy,m,dd)

    m = int(str_date[5:7])
    dd = int(str_date[8:10])
    yy = int(str_date[0:4])

    my_date = datetime.date(yy, m, dd)
    wd = my_date.weekday()
    if wd == 0:
        return 'Monday'
    if wd == 1:
        return 'Tuesday'
    if wd == 2:
        return 'Wednesday'
    if wd == 3:
        return 'Thursday'
    if wd == 4:
        return 'Friday'
    if wd == 5:
        return 'Saturday'
    if wd == 6:
        return 'Sunday'


def getting_moy(str_date):
    # This function returns the string equivalent of the month integer

    m = int(str_date[5:7])
    if m == 1:
        return 'January'
    if m == 2:
        return 'February'
    if m == 3:
        return 'March'
    if m == 4:
        return 'April'
    if m == 5:
        return 'May'
    if m == 6:
        return 'June'


def getting_hod(str_date):
    # This function is used to slice and store the hour component from the Start Time field
    hod = str_date[11:13]
    return hod


def get_pretty_hour(str_hr):
    # This function returns the corresponding time for the 24hr clock (e.g 17 = 5 pm )
    hr = int(str_hr)
    if hr < 12:
        return str(hr) + " am"
    return str(hr - 12) + " pm"


def display_data(df, current_line):
    '''Displays five lines of data if the user specifies YES.
    After displaying five lines, asks the user if they would like to see five more.
    Continues asking until they say stop.
    Args:
        df: dataframe of bikeshare data and the current line set at 0 for the first instance
    Returns:
        If the user says yes then this function returns the next five lines
            of the dataframe and then asks the question again by calling this
            function again (recursive)
        If the user says no then this function returns, but without any value
    '''
    display = input('\nWould you like to view individual trip data?'
                    ' Type \'yes\' or \'no\'.\n')
    display = display.lower()
    if display == 'yes' or display == 'y':
        print(df.iloc[current_line:current_line + 5])
        current_line += 5
        return display_data(df, current_line)
    if display == 'no' or display == 'n':
        return
    else:
        print("\nI'm sorry, I'm not sure if you wanted to see more data or not. Let's try again.")
        return display_data(df, current_line)


restart = True
while restart:
    """Prompts the user to make a selection for the desired city and loads the corresponding city csv file into a data frame.

       If the input doesn't match the necessary input values the prompt is reissued
    """

    city = input('\nHello! Let\'s explore Bikeshare Data for some US Metropolitan Cities!\n\n'
                 'Which city would you like to see data for Chicago(Chi), New York(NYC), or Washington(Wash)?\n')
    city_selected = True
    if city.lower() == 'chicago' or city == 'chi' or city == 'c':
        df = pd.read_csv('chicago.csv')
    elif city.lower() == 'new york' or city == 'ny' or city == 'nyc':
        df = pd.read_csv('new_york_city.csv')
    elif city.lower() == 'washington' or city == 'wash' or city == 'w':
        df = pd.read_csv('washington.csv')
    else:
        city_selected = False

    while city_selected is False:
        city = input(
            "That's not a valid input. Could you please re-enter the city name/abbreviations in either format mentioned above.\n")
        city_selected = True
        if city.lower() == 'chicago' or city == 'chi' or city == 'c':
            df = pd.read_csv('chicago.csv')
        elif city.lower() == 'new york' or city == 'ny' or city == 'nyc':
            df = pd.read_csv('new_york_city.csv')
        elif city.lower() == 'washington' or city == 'wash' or city == 'w':
            df = pd.read_csv('washington.csv')
        else:
            city_selected = False

    """4 new columns are created in the data frame with the respective function application
    """
    df['Day_of_Week'] = df['Start Time'].apply(getting_dow)
    df['Month_of_the_year'] = df['Start Time'].apply(getting_moy)
    df['Hour_of_the_day'] = df['Start Time'].apply(getting_hod)

    df['Start_End_Station_Pair'] = df['Start Station'] + ", " + df['End Station']

    # Asks the user for one of the three filtering criteria month,day or none

    filter = input(
        '\nHow would you like to filter the data for {}, by month, by day or none (without a filter)?\n\n'.format(city))

    if filter == 'month' or filter == 'Month' or filter == 'm':
        # Additional month filtering if the initial filter selected was month
        month_selection = input(
            'Which month would you like to see the data for, January(jan),February(feb),March(mar),April(apr),May,June(jun)?\n\n')
        if month_selection.lower() == 'jan' or month_selection == 'january':
            month_selection = 'January'
        elif month_selection.lower() == 'feb' or month_selection == 'february':
            month_selection = 'February'
        elif month_selection.lower() == 'mar' or month_selection == 'march':
            month_selection = 'March'
        elif month_selection.lower() == 'apr' or month_selection == 'april':
            month_selection = 'April'
        elif month_selection.lower() == 'may':
            month_selection = 'May'
        elif month_selection.lower() == 'june' or month_selection == 'jun':
            month_selection = 'June'

        print('Popular Times of Travel are as follows:\n')

        # Filters the loaded city dataframe by the selected month (i.e a dataframe with only the values corresponding to the selected month is created)
        month_filtered_df = df.loc[df['Month_of_the_year'] == month_selection]

        # Calculates the highest occuring day of the week for the filtered month
        dow = month_filtered_df['Day_of_Week'].mode().iloc[0]
        print(('The most popular day of the week for {} is {}').format(month_selection, dow))

        # Calculates the most occuring hour of the day
        month_filtered_df2 = month_filtered_df.loc[month_filtered_df['Day_of_Week'] == dow]
        hod = month_filtered_df2['Hour_of_the_day'].mode().iloc[0]
        hour = get_pretty_hour(hod)
        print(('The most popular hour of the day for {}s from {} is {}').format(dow, month_selection, hour))
        print('\n')

        # Displays trip statistics
        print('Popular Stations and Trip stats are as follows:\n')

        # Calculates most popular start station and returns only the first max value (i.e if there are 2 stations with same occurence count only the first max value will be returned)
        start_station = month_filtered_df['Start Station'].mode().iloc[0]
        print(('The most popular start station for {} is {}').format(month_selection, start_station))

        # Calculates most popular end station and returns only the first max value (i.e if there are 2 stations with same occurence count only the first max value will be returned)
        end_station = month_filtered_df['End Station'].mode().iloc[0]
        print(('The most popular end station for {} is {}').format(month_selection, end_station))

        # Calculates most popular station pair and returns only the first max value (i.e if there are 2 statio pairs with same occurence count only the first max value will be returned)
        start_end_station = month_filtered_df['Start_End_Station_Pair'].mode().iloc[0]
        print(('The most popular Start & End station pair for {} is {}').format(month_selection, start_end_station))
        print('\n')
        print('Trip duration statistics:\n')

        # Calculates trip duration values (total & avg trip time ) for the corresponding filtering criteria
        total = month_filtered_df['Trip Duration'].sum()
        total_trip_duration = str(datetime.timedelta(seconds=int(total)))
        mean = month_filtered_df['Trip Duration'].mean()
        mean_trip_duration = str(datetime.timedelta(seconds=int(mean)))
        print('Total trip duration: {} [D days, HH:MM:SS]'.format(total_trip_duration))
        print('Average trip duration: {} [D days, HH:MM:SS]\n'.format(mean_trip_duration))

        if city == 'Chicago' or city == 'Chi' or city == 'chi' or city == 'New York' or city == 'NY' or city == 'ny' or city == 'NYC':

            print('User Info:')
            # Displays categorical info about the users (types and counts) corresponding to the filtering criteria
            user_types = month_filtered_df['User Type'].value_counts()
            print(user_types)
            print('\n')

            gender_types = month_filtered_df['Gender'].value_counts()
            print(gender_types)
            print('\n')

            # Displays age related info corresponding to the filtering criteria
            earliest_birth_year = int(month_filtered_df['Birth Year'].min())
            latest_birth_year = int(month_filtered_df['Birth Year'].max())
            common_birth_year = int(month_filtered_df['Birth Year'].mode().iloc[0])
            print('Earliest birth year: {}'.format(earliest_birth_year))
            print('Latest birth year: {}'.format(latest_birth_year))
            print('Most common birth year: {}'.format(common_birth_year))
        else:
            print('User Info:')
            # Displays categorical info about the users (types and counts) corresponding to the filtering criteria
            user_types = month_filtered_df['User Type'].value_counts()
            print(user_types)
            print('\n')
    elif filter == 'day' or filter == 'D' or filter == 'd' or filter == 'Day':

        # Additional day filtering criteria
        day_selection = input('Which day would you like to filter the data by: Mon,Tu,Wed,Thurs,Fri,Sat,Sun?\n')
        if day_selection.lower() == 'mon':
            day_selection = 'Monday'
        elif day_selection.lower() == 'tues':
            day_selection = 'Tuesday'
        elif day_selection.lower() == 'wed':
            day_selection = 'Wednesday'
        elif day_selection.lower() == 'thurs':
            day_selection = 'Thursday'
        elif day_selection.lower() == 'fri':
            day_selection = 'Friday'
        elif day_selection.lower() == 'sat':
            day_selection = 'Saturday'
        elif day_selection.lower() == 'sun':
            day_selection = 'Sunday'

        # Stores a new data frame into the assigned variable which has been filtered based on the day selection
        day_filtered = df.loc[df['Day_of_Week'] == day_selection]

        # Required statistics are calculated
        print('Popular Times of Travel are as follows:\n')
        popular_hour_of_the_day = day_filtered['Hour_of_the_day'].mode().iloc[0]
        hour = get_pretty_hour(popular_hour_of_the_day)
        print('The most popular hour of the day for 2017 (Jan-June) is {}'.format(hour))
        print('\n')
        print('Popular Stations and Trip stats are as follows:\n')
        start_station = day_filtered['Start Station'].mode().iloc[0]
        print(('The most popular start station for 2017 (Jan-June) is {}').format(start_station))

        end_station = day_filtered['End Station'].mode().iloc[0]
        print(('The most popular end station for 2017 (Jan-June) is {}').format(end_station))

        start_end_station = day_filtered['Start_End_Station_Pair'].mode().iloc[0]
        print(('The most popular Start & End station pair for 2017 (Jan-June) is {}').format(start_end_station))
        print('\n')
        print('Trip duration statistics (Jan-June):\n')
        total = day_filtered['Trip Duration'].sum()
        total_trip_duration = str(datetime.timedelta(seconds=int(total)))
        mean = day_filtered['Trip Duration'].mean()
        mean_trip_duration = str(datetime.timedelta(seconds=int(mean)))
        print('Total trip duration: {} [D days, HH:MM:SS]'.format(total_trip_duration))
        print('Average trip duration: {} [D days, HH:MM:SS]\n'.format(mean_trip_duration))

        ''' As only the 2 city csv files contain the fields- User type and Gender, the following conditional statement ensures calculating statistics only for the relevant city files
                '''
        if city == 'Chicago' or city == 'Chi' or city == 'chi' or city == 'New York' or city == 'NY' or city == 'ny' or city == 'NYC':
            print('User Info (Jan-June):')
            user_types = day_filtered['User Type'].value_counts()
            print(user_types)
            print('\n')
            gender_types = day_filtered['Gender'].value_counts()
            print(gender_types)
            print('\n')
            earliest_birth_year = int(day_filtered['Birth Year'].min())
            latest_birth_year = int(day_filtered['Birth Year'].max())
            common_birth_year = int(day_filtered['Birth Year'].mode().iloc[0])
            print('Earliest birth year: {}'.format(earliest_birth_year))
            print('Latest birth year: {}'.format(latest_birth_year))
            print('Most common birth year: {}'.format(common_birth_year))
            print('\n')
        else:
            print('User Info (Jan-June):')
            user_types = day_filtered['User Type'].value_counts()
            print(user_types)
            print('\n')
    elif filter == 'none' or filter == 'n':

        # The original unfiltered data frame is stored into the assigned variable
        filtered_none = df

        # Required Statistics are calculated
        print('\n\nPopular Times of Travel for 2017 are as follows:\n')
        popular_month_of_year = filtered_none['Month_of_the_year'].mode().iloc[0]
        print('The most popular month of travel for 2017 (Jan-June) is {}'.format(popular_month_of_year))

        popular_day_of_the_year = filtered_none['Day_of_Week'].mode().iloc[0]
        print(('The most popular day of the year 2017 (Jan-June) is {}').format(popular_day_of_the_year))

        popular_hour_of_the_day = filtered_none['Hour_of_the_day'].mode().iloc[0]
        hour = get_pretty_hour(popular_hour_of_the_day)
        print('The most popular hour of the day for 2017 (Jan-June) is {}'.format(hour))
        print('\n')
        print('Popular Stations and Trip stats are as follows:\n')
        start_station = filtered_none['Start Station'].mode().iloc[0]
        print(('The most popular start station for 2017 (Jan-June) is {}').format(start_station))

        end_station = filtered_none['End Station'].mode().iloc[0]
        print(('The most popular end station for 2017 (Jan-June) is {}').format(end_station))

        start_end_station = filtered_none['Start_End_Station_Pair'].mode().iloc[0]
        print(('The most popular Start & End station pair for 2017 (Jan-June) is {}').format(start_end_station))
        print('\n')
        print('Trip duration statistics (Jan-June):\n')
        total = filtered_none['Trip Duration'].sum()
        total_trip_duration = str(datetime.timedelta(seconds=int(total)))
        mean = filtered_none['Trip Duration'].mean()
        mean_trip_duration = str(datetime.timedelta(seconds=int(mean)))
        print('Total trip duration: {} [D days, HH:MM:SS]'.format(total_trip_duration))
        print('Average trip duration: {} [D days, HH:MM:SS]\n'.format(mean_trip_duration))

        ''' As only the 2 city csv files contain the fields- User type and Gender, the following conditional statement ensures calculating statistics only for the relevant city files
        '''
        if city == 'Chicago' or city == 'Chi' or city == 'chi' or city == 'New York' or city == 'NY' or city == 'ny' or city == 'NYC':
            print('User Info (Jan-June):')
            user_types = filtered_none['User Type'].value_counts()
            print(user_types)
            print('\n')
            gender_types = filtered_none['Gender'].value_counts()
            print(gender_types)
            print('\n')
            earliest_birth_year = int(filtered_none['Birth Year'].min())
            latest_birth_year = int(filtered_none['Birth Year'].max())
            common_birth_year = int(filtered_none['Birth Year'].mode().iloc[0])
            print('Earliest birth year: {}'.format(earliest_birth_year))
            print('Latest birth year: {}'.format(latest_birth_year))
            print('Most common birth year: {}'.format(common_birth_year))
            print('\n')
        else:
            print('User Info (Jan-June):')
            user_types = filtered_none['User Type'].value_counts()
            print(user_types)
            print('\n')

    # Displays five lines of data at a time if the user wants
    display_data(df, 0)

    # Asks the user for further action whether to restart the program or abort
    answer = input('\nWould you like to restart the program? (Y) or (N)\n')
    if answer.lower() == 'y' or answer == 'yes':
        restart = True
    else:
        restart = False
