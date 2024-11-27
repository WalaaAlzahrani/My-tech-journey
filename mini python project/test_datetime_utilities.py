import datetime_utilities as du  

# Test for days_in_month function
print("Testing days_in_month(2024, 2):", du.days_in_month(2024, 2))  # Leap year
print("Testing days_in_month(2023, 2):", du.days_in_month(2023, 2))  # Non-leap year

# Test for is_valid_date function
print("Testing is_valid_date(2024, 2, 29):", du.is_valid_date(2024, 2, 29))  # Valid date (leap year)
print("Testing is_valid_date(2023, 2, 29):", du.is_valid_date(2023, 2, 29))  # Invalid date (not leap year)

# Test for days_between function
print("Testing days_between(2024, 1, 1, 2024, 1, 10):", du.days_between(2024, 1, 1, 2024, 1, 10))  # 9 days

# Test for age_in_days function
print("Testing age_in_days(1990, 5, 15):", du.age_in_days(1990, 5, 15))  # Calculate age in days for a given birthdate
