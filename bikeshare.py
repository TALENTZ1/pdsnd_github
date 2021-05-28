import time
import calendar 
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
    
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ["chicago", "new york city", "washington"]
    months = ["january", "february", "march", "april", "may", "june", "all"]
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]
    while True:
        city = input("Which city would you like to see data for? Select chicago, new york city or washington\n").lower()
        print(city)
        if city in cities:
            break
        else:
            print("Invalid input. Please select from chicago, new york or washington.")
    
    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to see data for? Select january, february, march, april, may, june or all\n").lower()
        print(month)
        if month in months:
            break
        else:
            print("Invalid input. Please select january, february, march, april, may, june or all.")
    
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day would you like to see data for? Select monday, tuesday, wednesday, thursday, friday, saturday, sunday or all\n").lower()
        print(day)
        if day in days_of_week:
            break
        else:
            print("Invalid input. Please select monday, tuesday, wednesday, thursday, friday, saturday, sunday or all.")
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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # Substitute NaN in gender column
    if city !='washington':
        df['Gender'].fillna('Unknown', inplace=True)
        
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
        
    # Extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['days_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # Filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['days_of_week'] == day.title()]
    return df
    
def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # Display the most common month
    popular_month_number = df['month'].mode()[0]
    popular_month_name = calendar.month_name[popular_month_number]    
    if month == 'all':
        print('Most common month:', popular_month_name.title())
    else:
        print('Most common month (as selected by the user) :',  month.title())
    
    # Display the most common day of week
    popular_weekday = df['days_of_week'].mode()[0]
    if day == 'all':
        print('Most common day of week:', popular_weekday)
    else:
        print('Most common day of week (as selected by the user) :', popular_weekday)
        
    # Display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most common hour of day:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # Display counts of distinct start stations
    start_stations = df['Start Station'].nunique()
    print('Number of start stations:', start_stations)   
    
    # Display counts of distinct end stations
    end_stations = df['End Station'].nunique()
    print('Number of end stations:', end_stations)     
       
    # Display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most commonly used start station:', popular_start)
    
    # Display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most commonly used end station:', popular_end)
    
    # Display most frequent combination of start station and end station trip
    df['station_combination']= df['Start Station'] + ':' + df['End Station']
    popular_station_combination = df['station_combination'].mode()[0]
    print('Most commonly used combination of stations:', popular_station_combination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # Display shortest travel time
    min_travel_time = df['Trip Duration'].min() / 60 / 60
    print('shortest travel time:', min_travel_time, 'hours')
    
    # Display longest travel time
    max_travel_time = df['Trip Duration'].max() / 60 / 60
    print('longest travel time:', max_travel_time, 'hours')    

    # Display total travel time
    sum_travel_time = df['Trip Duration'].sum() / 60 / 60
    print('total travel time:', sum_travel_time, 'hours')
    
    # Display mean travel time
    avg_travel_time = df['Trip Duration'].mean() / 60
    print('average travel time:', avg_travel_time, 'minutes')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print('Distribution of user types:', user_types)
    
    # Display counts of gender
    if 'Gender' in df.columns:
       gender_count = df['Gender'].value_counts().to_frame()
       print('Distribution of gender:', gender_count)
    else:
       print("No gender data to share.")
    
    # Display earliest, most recent, and most common year of birth and unknown birth year volumes
    if 'Birth Year' in df.columns:
        most_recent_birthyear = df['Birth Year'].max()
        print('Most recent birth year:', int(most_recent_birthyear))
        earliest_birthyear = df['Birth Year'].min()
        print('Earliest birth year:', int(earliest_birthyear))
        most_common_birthyear = df['Birth Year'].mode()[0]
        print('Most common birth year:', int(most_common_birthyear))     
        null_birth_date = df['Birth Year'].isnull().sum() 
        print('Users with unknown birth year:', int(null_birth_date))        
    else:
        print("No birth year data to share.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def main():
    """Displays raw filtered data based on user input"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df,month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        i = 0
        
        # User input for displaying rows
        raw = input("Would you like to see the first 5 rows of raw data? Type 'yes' or 'no'.\n").lower()
        pd.set_option('display.max_columns', 200)
        while True:
          if raw == 'no':
            break
          print(df[i:i+5])
          raw = input("Would you like to see the next 5 rows of raw data?\n").lower()
          i +=5
          
        # User input for restart          
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            
if __name__ == "__main__":
	main()