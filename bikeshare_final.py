import time
import datetime
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

print('-'*50)
print('\nHello fellow bikeshare data nerd! Let\'s explore some US bikeshare data.')
print('This application has data for Chicago, New York City and Washington.\n')

def get_filters():
    """
    The get_filters function asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ''
    month_pref = ''
    day_pref = ''

    # While loop to obtain user city preference.
    while city not in CITY_DATA.keys():
        try:
            city = input('Please enter which city\'s data you would like to see: ').lower()
            if city in (CITY_DATA.keys()):
                print('\nYou have chosen: ', city.title())
            else:
                print('\nSorry, That\'s not a valid city name. \nPlease select either Chicago, New York City or Washington.')
        except Exception as e:
            print(e)

    print('\nThis app has data available for the first six months of 2017.')

    # While loop to obtain user month preference.
    while month_pref not in ('A', 'a', '1', '2', '3', '4', '5', '6'):
        month_pref = input("\nPlease select a month or choose A to not filter by month:\n\t"
                "A = All months\n\t1 = January\n\t2 = February\n\t3 = March\n\t4 = April\n\t"
                "5 = May\n\t6 = June\n>>  ")
        if month_pref not in ('A', 'a', '1', '2', '3', '4', '5', '6'):
            print("Sorry, that's not a valid option. Please indicate the month number or 'A' for all.")
    print('-'*50)

    # While loop to obtain user day preference.
    while day_pref not in ('A', 'a', '1', '2', '3', '4', '5', '6', '7'):
        day_pref = input("\nPlease select a day of the week or choose A to not filter by day:\n\t"
                  "A = All days\n\t1 = Sunday\n\t2 = Monday\n\t3 = Tuesday\n\t4 = Wednesday\n\t"
                  "5 = Thursday\n\t6 = Friday\n\t7 = Saturday\n>>  ")
        if day_pref not in ('A', 'a', '1', '2', '3', '4', '5', '6', '7'):
            print("\nSorry, that's not a valid option. Please indicate the day number or 'A' for all.")
    if day_pref not in ('A', 'a'):
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        day_pref = days[int(day_pref) - 1]
    print('-'*50)
    return city, month_pref, day_pref


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    print('\nThere are {} total rows of data for {}.'.format(len(df),city))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract the month number and weekday name into new separate columns
    df['Month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    # apply month filter (if applicable) to update the new dataframe
    if month not in ('A', 'a'):
        df = df[df['Month'] == int(month)]

    # apply day of week filter (if applicable) to update the new dataframe
    if day not in ('A', 'a'):
        df = df[df['day_of_week'] == day.title()]

    print('\nThere are {} rows of data for {} after applying the selected month '
    'and day of week filters.'.format(len(df), city))

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args:
        (dataframe) df - containing city data filtered by month and day

    Returns:
        Travel time statistics as console output.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    # df['Start Time'] = pd.to_datetime(df['Start Time'])

    # convert month from a number to its corresponding english name
    # README -- Reviewed strftime on docs.python.org after finding on Stackoverflow.
    df['month'] = df['Start Time'].dt.strftime("%B")

    # find and display the busiest month
    busiest_month = str(df['month'].mode()[0])
    print('Busiest Month: {}'.format(busiest_month))

    # find and display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    busiest_day = str(df['day_of_week'].mode()[0])
    print('Busiest Day of Week: {}'.format(busiest_day))
    # README -- Found strftime("%A") function on Stackoverflow.com
    # README -- https://stackoverflow.com/questions/9847213/how-do-i-get-the-day-of-week-given-a-date

    # find and display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    common_hour = str(df['hour'].mode()[0])
    print('Most Frequent Start Hour: {}:00'.format(common_hour))

    # print("\nThis took %s seconds to compute." % (time.time() - start_time))
    # print('-'*50)

def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        (dataframe) df - containing city data filtered by month and day

    Returns:
        Start and end station statistics as console output.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # find and display the most commonly used start station
    busiest_start_station = str(df['Start Station'].mode()[0])
    print('The most commonly used Start Station:  {}'.format(busiest_start_station))

    # find and display the most commonly used end station
    busiest_end_station = str(df['End Station'].mode()[0])
    print('The most commonly used End Station:  {}'.format(busiest_end_station))

    # find and display the most frequent combination of start station and end stations
    print('The most common combination of Start and End Stations and number of trips:\n\n',
    df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).nlargest(n=1))

    # print("\nThis took %s seconds to compute." % (time.time() - start_time))
    # print('-'*50)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        (dataframe) df - containing city data filtered by month and day

    Returns:
        Trip duration statistics as console output.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # find and display total travel time in hours
    tot_trvl_time = df['Trip Duration'].sum()
    print('Total travel time this period: ', tot_trvl_time/3600,
    'hours')

    # find and display mean travel time in minutes
    mean_trvl_time = df['Trip Duration'].mean()
    print('The average travel time was: ', mean_trvl_time/60, 'minutes')

    # print("\nThis took %s seconds to compute." % (time.time() - start_time))
    # print('-'*50)


def user_stats(df):
    """Displays statistics on bikeshare users.

    Args:
        (dataframe) df - containing city data filtered by month and day

    Returns:
        Bikshare user statistics as console output.
    """

    print('\nCalculating User Stats...')
    start_time = time.time()

    # find and display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nThe breakout of User Type was:\n", user_types)

    # find and display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print("\nThe breakout of user gender was as follows:\n", gender_count)
    except KeyError:
        print('\nSorry, there is no gender data available for this query.')

    # find and display earliest, most recent, and most common year of birth
    try:
        earliest_birth = int(df['Birth Year'].min())
        print("\nThe earlist birth year for any user was:", earliest_birth)
        most_recent_birth = int(df['Birth Year'].max())
        print("The most recent birth year for any user was:", most_recent_birth)
        most_common_yob = int(df['Birth Year'].mode())
        print("The most common birth year was:", most_common_yob)
    except:
        print('\nSorry, there is no birth year data available for this query.')

    # print("\nThis took %s seconds to compute." % (time.time() - start_time))
    # print('-'*50)

def raw_data(df):
    """ The raw_data function asks users if they would like to see raw data from
    the filitered dataframe. If users select 'yes,' they are given five rows of
    raw data until they selct 'no,' or they reach the end of the file.

    Args:
        (dataframe) df - containing city data filtered by month and day

    Returns:
        Raw dataframe statistics as console output five rows at a time.
    """

    raw_data_pref = ''
    start_row = 0

    # solict user interest in seeing raw data
    while raw_data_pref not in ('Yes', 'yes', 'Y', 'y', 'No', 'N', 'no', 'n'):
        try:
            raw_data_pref = input("\nWould you like to see samples of the raw data?\n\t"
                "Y = Yes\n\tN = No\n>>  ")
            if raw_data_pref not in ('Yes', 'yes', 'Y', 'y', 'No', 'N', 'no', 'n'):
                print("Sorry, that's not a valid option. Please enter either yes or no.")
        except Exception as e:
            print(e)
    # display raw data five rows at a time
    while raw_data_pref in ('Yes', 'yes', 'Y', 'y') and start_row + 5 < len(df):
        print('\n Displaying rows {} to {}:'.format(start_row + 1, start_row + 5))
        print('\n', df.iloc[start_row:start_row + 5, 1:9])
        start_row += 5
        print('-'*50)
        raw_data_pref = input("\nWould you like to see the next five rows of raw_data?\n\t"
        "Y = Yes\n\tN = No\n>>  ")
    if start_row + 5 >= len(df):
        print('\nYou have reached the end of the raw data set.')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
