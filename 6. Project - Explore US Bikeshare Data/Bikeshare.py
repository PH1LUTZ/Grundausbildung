import pandas as pd

def load_city_data(city):
	filename = f'{city.lower().replace(" ", "_")}.csv'
	return pd.read_csv(filename)

def get_city_selection():
	cities = {'1': 'Chicago', '2': 'New York City', '3': 'Washington'}
	
	while True:
		print("\nSelect a city:")
		for key, value in cities.items():
			print(f"{key}. {value}")
		
		selection = input("Enter the number of the desired city: ")
		
		if selection in cities:
			return cities[selection]
		else:
			print("Invalid input. Please choose again.")

# User selects the city
city_selection = get_city_selection()

# Load data for the selected city
try:
	df = load_city_data(city_selection)
except FileNotFoundError:
	print(f"Data for {city_selection} could not be found.")
	exit()

# Convert the 'Start Time' column to a datetime format
df['Start Time'] = pd.to_datetime(df['Start Time'])

# Add a column for the month
df['Month'] = df['Start Time'].dt.month

# Add a column for the day of the week
df['Day of Week'] = df['Start Time'].dt.day_name()

# Mapping of month numbers to month names
month_mapping = {
	1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
	7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
}

# Initialize filters
month_filter = None
weekday_filter = None

def get_selection(prompt):
	return input(prompt).strip()

def get_input_with_validation(prompt, valid_options):
	while True:
		user_input = get_selection(prompt)
		if user_input in valid_options:
			return user_input
		else:
			print("Invalid input. Please choose again.")

def display_options():
	month_filter_display = month_mapping[month_filter].upper()[:3] if month_filter else 'ALL'
	weekday_filter_display = weekday_filter.upper()[:3] if weekday_filter else 'ALL'

	print(f"\nSelect an option for ({city_selection}):")
	print("1. Popular times of travel")
	print("2. Popular stations and trip")
	print("3. Trip duration")
	print("4. User info")
	print("5. Display individual trip data")
	print(f"6. Filter by month ({month_filter_display})")
	print(f"7. Filter by weekday ({weekday_filter_display})")
	print("q. Quit the program")

def display_popular_times():
	print("\n#1 Popular times of travel:")
	filtered_data = filter_data()
	print("Most common month:", month_mapping[filtered_data['Month'].mode().iloc[0]])
	print("Most common day of week:", filtered_data['Day of Week'].mode().iloc[0])
	print("Most common hour of day:", filtered_data['Start Time'].dt.hour.mode().iloc[0])

def display_popular_stations_trip():
	print("\n#2 Popular stations and trip:")
	filtered_data = filter_data()
	print("Most common start station:", filtered_data['Start Station'].mode().iloc[0])
	print("Most common end station:", filtered_data['End Station'].mode().iloc[0])

	# Combination of start and end station
	combined_stations = filtered_data.groupby(['Start Station', 'End Station']).size().idxmax()
	print("Most common trip from start to end:", combined_stations[0], "to", combined_stations[1])
 
def display_trip_duration():
	print("\n#3 Trip duration:")
	filtered_data = filter_data()
	total_seconds = filtered_data['Trip Duration'].sum()

	# Convert seconds to days, hours, minutes, and seconds
	days, remainder = divmod(total_seconds, 86400)
	hours, remainder = divmod(remainder, 3600)
	minutes, seconds = divmod(remainder, 60)

	print(f"Total travel time: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
	average_seconds = filtered_data['Trip Duration'].mean()

	# Convert average to days, hours, minutes, and seconds
	avg_days, avg_remainder = divmod(average_seconds, 86400)
	avg_hours, avg_remainder = divmod(avg_remainder, 3600)
	avg_minutes, avg_seconds = divmod(avg_remainder, 60)

	print(f"Average travel time: {int(avg_days)} days, {int(avg_hours)} hours, {int(avg_minutes)} minutes, {int(avg_seconds)} seconds")

def display_user_info():
	print("\n#4 User info:")
	filtered_data = filter_data()
	print("Counts of each user type:")
	print(filtered_data['User Type'].value_counts())
	
	if 'Gender' in filtered_data.columns:
		print("\nCounts of each gender:")
		print(filtered_data['Gender'].value_counts())

	if 'Birth Year' in filtered_data.columns:
		print("\nEarliest year of birth:", int(filtered_data['Birth Year'].min()))
		print("Most recent year of birth:", int(filtered_data['Birth Year'].max()))
		print("Most common year of birth:", int(filtered_data['Birth Year'].mode().iloc[0]))

def display_data(data_frame):
	while True:
		view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
		start_loc = 0

		if view_data == 'no':
			break
		elif view_data != 'yes':
			print("Invalid input. Please enter 'yes' or 'no'.")
			continue

		while True:
			# Display 5 rows of data
			filtered_data = filter_data()
			print(filtered_data.iloc[start_loc:start_loc + 5])

			# Update starting location for the next iteration
			start_loc += 5

			# Ask the user if they want to continue
			view_data = input("Do you wish to continue? Enter yes or no: ").lower()
			if view_data != 'yes':
				break

def filter_by_month():
	global month_filter
	print("\nSelect a month:")
	print("0. ALL")
	for i in range(1, 13):
		print(f"{i}. {month_mapping[i]}")

	selected_month = get_input_with_validation("Enter the number of the desired month: ", [str(i) for i in range(13)])

	if selected_month == '0':
		month_filter = None
	else:
		try:
			selected_month = int(selected_month)
			if 1 <= selected_month <= 12:
				month_filter = selected_month
			else:
				print("Invalid input. Please choose again.")
		except ValueError:
			print("Invalid input. Please choose again.")

def filter_by_weekday():
	global weekday_filter
	print("\nSelect a weekday:")
	print("0. ALL")
	weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	for i, day in enumerate(weekdays, start=1):
		print(f"{i}. {day}")

	selected_weekday_index = get_input_with_validation("Enter the number of the desired weekday: ", [str(i) for i in range(8)])
	if selected_weekday_index == '0':
		weekday_filter = None
	else:
		try:
			selected_weekday_index = int(selected_weekday_index)
			weekday_filter = weekdays[selected_weekday_index - 1]
		except (ValueError, IndexError):
			print("Invalid input. Please choose again.")

def filter_data():
	filtered_data = df
	if weekday_filter and weekday_filter != 'ALL':
		filtered_data = filtered_data[filtered_data['Day of Week'] == weekday_filter]
	if month_filter and month_filter != 'ALL':
		filtered_data = filtered_data[filtered_data['Month'] == month_filter]
	return filtered_data

# Main program loop
while True:
	display_options()
	selection = get_selection("Enter the number of the desired option: ")

	if selection == '1':
		display_popular_times()

	elif selection == '2':
		display_popular_stations_trip()

	elif selection == '3':
		display_trip_duration()

	elif selection == '4':
		display_user_info()

	elif selection == '5':
		display_data(df)

	elif selection == '6':
		filter_by_month()

	elif selection == '7':
		filter_by_weekday()

	elif selection.lower() == 'q':
		print("Exiting the program.")
		break

	else:
		print("Invalid selection. Please choose again.")