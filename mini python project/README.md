# Date Utilities Python Project

This Python project contains a set of utilities for working with dates. It includes functions to:

- Calculate the number of days in a given month
- Check if a date is valid
- Calculate the number of days between two dates
- Calculate a person's age in days based on their birthdate

## 📜Functions

1. **days_in_month(year, month)**:
   - Returns the number of days in a specified month of a specified year.

2. **is_valid_date(year, month, day)**:
   - Returns `True` if the date is valid, otherwise `False`.

3. **days_between(year1, month1, day1, year2, month2, day2)**:
   - Returns the number of days between two dates, ensuring the second date is not before the first one.

4. **age_in_days(year, month, day)**:
   - Returns the age of a person in days based on their birthdate as of today.

## 🚀Usage

```python
import datetime_utilities as du

# Get number of days in a month
print(du.days_in_month(2024, 2))

# Check if a date is valid
print(du.is_valid_date(2024, 2, 29))

# Calculate the number of days between two dates
print(du.days_between(2024, 1, 1, 2024, 12, 31))

# Calculate age in days
print(du.age_in_days(1990, 5, 15))
