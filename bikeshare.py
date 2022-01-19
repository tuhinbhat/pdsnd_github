import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('\nWhich city would you like data for?\n').lower()
    while city not in CITY_DATA.keys():
        print('There is no data for this city', city)
        print('Valid cities are:', CITY_DATA.keys())
        print('Exiting now due to invalid city.')
        exit()

    #asking user what filter type they would like.
    input_type = ['month', 'day', 'both', 'none']
    while True:
        t = input('\nWould you like to filter by month, day, both, or none?\n').lower()
        if t not in input_type:
            print('Invalid input type, Valid types are:', input_type)
            restart = input('\nWould you like to restart with a valid value? Enter yes (y) or no (n).\n')
            if ( restart.lower() == 'no' or restart.lower() == 'n' ):
                print('Exiting now based on user input.')
                exit()
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    month = 'NA'
    if t == 'month' or t == 'both':
        month = (input('\nWhich month would you like data for?\n')).lower()
        while month not in mnth:
            print('Invalid month, Valid months are:', mnth)
            print('Exiting now.')
            exit()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = 'NA'
    if t =='day' or t == 'both':
        day = (input('\nWhich day would you like data for?\n')).lower()
        while day not in dow:
            print('Invalid day of the week, Valid days are:', dow)
            print('Exiting now.')
            exit()

    print('-'*40)
    print(city, month, day, t)
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

    #this file needs to be determined by a for loop to match one of the three cities

    c = list(CITY_DATA.keys())
    f = list(CITY_DATA.values())
    i = c.index(city)
    file = f[i]
    print(file)

    df = pd.read_csv(file)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['day'] = df['Start Time'].dt.day
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday

    #choosing data filtering method based on user input
    #filter by month if not NA, filter by day if not NA, filter by city and month if both are not NA
    if (month == 'NA' and day == 'NA'):
        a = 1
    else:
        if month != 'NA':
            dum = -1
            rmindex = []
            for i in range(0, len(df['month'])-1):  #months and dow
                m = df['month'][i]
                if not ( m == mnth.index(month)+1):
                    dum += 1
                    rmindex.insert(dum, i)

        if day != 'NA':
            dum = -1
            rmindex = []
            for i in range(0, len(df['month'])-1):  #months and dow
                d = df['weekday'][i]
                if not ( d == dow.index(day) ):
                    dum += 1
                    rmindex.insert(dum, i)

        #dropping the non-matched indexes
        df.drop(rmindex, inplace = True)

    return df

def time_stats(df, month, day):

    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'NA':
        common_month = df['month'].mode()[0]
        print("\nThe most common month is: ", common_month)

    # display the most common day of week
    if day == 'NA':
        common_day = df['day'].mode()[0]
        print("\nThe most common day is: ", common_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("\nThe most common start hour is: ", popular_hour)

    print("\nThe time_stats test took {:.2e} seconds." .format(time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    #Execute only if column data is available
    if check_column(hdr,"Start Station"):
        common_start_station = df['Start Station'].mode()[0]
        print("\nThe most common start station is: ", common_start_station)

    # display most commonly used end station
    if check_column(hdr,"End Station"):
        common_end_station = df['End Station'].mode()[0]
        print("\nThe most common end station is: ", common_end_station)

    # display most frequent combination of start station and end station trip
    df['common_comb_station'] = df['Start Station'] + ' ' + df['End Station']
    common_combination_station = df['common_comb_station'].mode()[0]
    print("\nThe most common combination station is: ", common_combination_station)

    print("\nThe station_stats test took {:.2e} seconds." .format(time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    if check_column(hdr,"Trip Duration"):
        total_travel_time = sum(df['Trip Duration'])
        print("\nThe total travel time is {} seconds.".format(total_travel_time))
        # display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        print("\nThe mean travel time is {} seconds.".format(mean_travel_time))

    print("\nThe trip duration stats {:.2e} seconds." .format(time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if check_column(hdr,"User Type"):
        user_types_count = df['User Type'].count()
        user_types_unique_count = df['User Type'].value_counts()
        print("\nThe user types count is:", user_types_count)
        print("\nThe unique user types count is:\n", user_types_unique_count)

    # Display counts of gender
    if check_column(hdr,"Gender"):
        gender_count = df['Gender'].count()
        gender_unique_count = df['Gender'].value_counts()
        print("\nThe gender count is:", gender_count)
        print("\nThe unique gender count is:\n", gender_unique_count)

    # Display earliest, most recent, and most common year of birth
    if check_column(hdr,"Birth Year"):
        earliest_yob = int(min(df['Birth Year']))
        most_recent_yob = int(max(df['Birth Year']))
        common_yob = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth is: ", earliest_yob)
        print("\nThe most recent year of birth is: ", most_recent_yob)
        print("\nThe most common year of birth is: ", common_yob)

    print("\nThe user stats took {:.2e} seconds." .format(time.time() - start_time))
    print('-'*40)

def check_column(hdr, column):
    #Checking for availability of column data
    status = True
    if not column in hdr:
        status = False
        print('Data for {} is not available - Skipping data operation.'.format(column))
    return(status)

def display_data(df):
    #Display limited dataset based on user choice.
    start_loc = 0
    while (start_loc <= len(df)):
        view_data = input('\nWould you like to view 5 more rows of individual trip data? Enter yes (y) or no (n).\n')
        if ( view_data.lower() == 'yes' or view_data.lower() == 'y' ):
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
        else:
            break

def main():
    global mnth, dow, hdr
    mnth = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    dow = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
    #   hdr = list(df.head(1) #Capturing header and making it global.
        hdr = np.array(list(df.head(1))) #Capturing header and making it global.
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes (y) or no (n).\n')
        if ( restart.lower() == 'no' or restart.lower() == 'n' ):
            break

if __name__ == "__main__":
	main()
