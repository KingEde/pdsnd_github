import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['January','Feburary','March','April','May','June','All']

DAY_DATA = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data from January to June 2017!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city =''
    month=''
    day=''
    while city not in CITY_DATA:
        city = input('\nWhich city would you like to take a look at? (Chicago, New York City or Washington)\n').lower()

    # get user input for month (all, january, february, ... , june)
    while month.title() not in MONTH_DATA:
        month = input('\nWhich month would you like to take a look at? (type "all" to not filter on month)\n').lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day.title() not in DAY_DATA:
        day = input('\nWhich day would you like to take a look at? (type "all" to not filter on day)\n').lower()

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        month = month.title()
        month = MONTH_DATA.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    #print(df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Start Time'].dt.month.mode()[0]
    print('The most popular month is:', MONTH_DATA[popular_month-1],'\n')

    # display the most common day of week
    popular_dow = df['Start Time'].dt.weekday_name.mode()[0]
    print('The most popular day of the week is:', popular_dow,'\n')

    # display the most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most popular hour to start a rental is: ", popular_hour,'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('The most popular station to start a trip is: ', popular_start_station,'\n')

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('The most popular station to end a trip is: ', popular_end_station,'\n')

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' Station to '+ df['End Station'] + ' Station'
    popular_route= df['trip'].value_counts().idxmax()
    print('The most popular trip is from', popular_route,'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 60
    print('The total travel time for the select city and timeframe is: {} hours\n'.format(round(total_travel_time/60/60,2)))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average travel time is {} minutes and {} seconds.\n'.format(int(mean_travel_time //60) , int(mean_travel_time %60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print(user_types,'\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
        print(gender_types,'\n')
    else:
        print('Gender based anaylsis are not available for the selected city.\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        youngest_birth = int(df['Birth Year'].max())
        oldest_birth = int(df['Birth Year'].min())
        common_birth = int(df['Birth Year'].mode()[0])
        print('The youngest person was born {}, the oldest person was born {}, the most common birthyear is {}.'.format(youngest_birth,oldest_birth,common_birth))
    else:
        print('Age based anaylsis are not available for the selected city.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    rawdata_request = input('\nWould you like to see the raw data? Enter yes or no.\n')
    start = 0
    end = 5

    while rawdata_request.lower() == 'yes':
        print('-'*40)
        if end > len(df.index):
            end = -1
        rawdata=df.iloc[start:end]
        print(rawdata,'\n')
        if end == -1:
            print('\nReached end of raw data. Continuing with normal program\n')
            print('-'*40)
            break
        print('-'*40)
        rawdata_request = input('\nWould you like to see 5 more lines? Enter yes or no.\n')
        start += 5
        end += 5
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)


        display_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
