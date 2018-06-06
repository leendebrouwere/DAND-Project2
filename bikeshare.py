import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    while True:
        city=input('Would you like to see data for Chicago, New York city or Washington? ').title()
        if city not in ('Chicago','Washington','New York City','All'):
            print('Invalid input. Please try again.')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month=input('Which month do you want to see? January, February, March, April, May, June or all? ').title()
        if month not in ('January','February','March','April','May','June','All'):
            print('Invalid input. Please try again.')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input('Which day do you want to see? Monday, Tuesday, ... Sunday or all? ').title()
        if day not in ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All'):
            print('Invalid input. Please try again.')
        else:
            break

    print('-'*40)
    return city, month, day



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
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

   # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df



def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month, when not a specific month was chosen:
    if month == 'All':
        df['month'] = df['Start Time'].dt.month
        common_month = df['month'].mode()[0]
        month_names = ['January', 'February', 'March', 'April', 'May', 'June']
        common_month_name = month_names[common_month-1]
        print('Most common month:', common_month_name)

    # display the most common day of week, when not a specific day was chosen:
    if day == 'All':
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        common_day = df['day_of_week'].mode()[0]
        print('Most common day:', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common start hour:', common_hour,'h')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most common start station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most common end station:', common_end_station)

    # display most frequent combination of start station and end station trip
    df['Trip']= 'From \"' + df['Start Station'] + '\" to \"' + df['End Station'] + '\"'
    common_trip = df['Trip'].mode()[0]
    print('Most common trip:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time:', int(df['Trip Duration'].sum()),'sec')

    # display mean travel time
    print('Average travel time:', int(df['Trip Duration'].mean()),'sec')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    if city == 'Washington':
        print('\nNo user statistics available for this city.\n')
    else:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        print('Count of user types:\n', df['User Type'].value_counts())

        # Display counts of gender
        print('\nCount of gender:\n', df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print('\nThe youngest user is born in:', int(df['Birth Year'].max()))
        print('The oldest user is born in:', int(df['Birth Year'].min()))
        common_year = df['Birth Year'].mode()[0]
        print('The most common year of birth is:',int(common_year))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def rawdata_display(df):
        """Displays some raw data from the tabel at users request."""
        while True:
            raw = input('\nWould you like to look at some raw data? Enter yes or no.\n')
            if raw.lower() not in ('yes','no'):
                print('Invalid input. Please try again.')
            else:
                break
        if raw.lower() == 'yes':
            print (df.head())

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        rawdata_display(df)
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() not in ('yes','no'):
                print('Invalid input. Please try again.')
            else:
                break
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
