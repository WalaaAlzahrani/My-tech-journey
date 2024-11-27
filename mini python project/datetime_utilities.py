import datetime

def days_in_month(year, month):
    """
    Inputs:
      year  - an integer between datetime.MINYEAR and datetime.MAXYEAR
              representing the year
      month - an integer between 1 and 12 representing the month

    Returns:
      The number of days in the input month.
    """
    # Handle December specially, since the next month is January of the next year
    if month == 12:
        next_month = datetime.date(year + 1, 1, 1)
    else:
        next_month = datetime.date(year, month + 1, 1)
    
    current_month = datetime.date(year, month, 1)
    delta = next_month - current_month
    return delta.days



def is_valid_date(year, month, day):
    """
    Inputs:
      year  - an integer representing the year
      month - an integer representing the month
      day   - an integer representing the day

    Returns:
      True if year-month-day is a valid date and
      False otherwise
    """
    
    # Check if the year is within the valid range
    if not (datetime.MINYEAR <= year <= datetime.MAXYEAR):
        return False

    # Check if the month is valid
    if not (1 <= month <= 12):
        return False

    # Check if the day is valid
    # Use days_in_month to get the maximum valid day for the month
    if not (1 <= day <= days_in_month(year, month)):
        return False

    # If all checks pass, the date is valid
    return True



def days_between(year1, month1, day1, year2, month2, day2):
    """
    Inputs:
      year1  - an integer representing the year of the first date
      month1 - an integer representing the month of the first date
      day1   - an integer representing the day of the first date
      year2  - an integer representing the year of the second date
      month2 - an integer representing the month of the second date
      day2   - an integer representing the day of the second date

    Returns:
      The number of days from the first date to the second date.
      Returns 0 if either date is invalid or the second date is
      before the first date.
    """
    # Check if both dates are valid
    if not (is_valid_date(year1, month1, day1) and is_valid_date(year2, month2, day2)):
        return 0

    # Create date objects
    date1 = datetime.date(year1, month1, day1)
    date2 = datetime.date(year2, month2, day2)

    # Check if the second date is earlier than the first date
    if date2 < date1:
        return 0

    # Calculate the difference in days
    delta = date2 - date1
    return delta.days

def age_in_days(year, month, day):
    """
    Inputs:
      year  - an integer representing the birthday year
      month - an integer representing the birthday month
      day   - an integer representing the birthday day

    Returns:
      The age of a person with the input birthday as of today.
      Returns 0 if the input date is invalid or if the input
      date is in the future.
    """
    
    # Check if the birthday date is valid
    if not is_valid_date(year, month, day):
        return 0

    # Get today's date
    today = datetime.date.today()

    # Create a date object for the birthday
    birthday = datetime.date(year, month, day)

    # Check if the birthday is in the future
    if birthday > today:
        return 0

    # Calculate the age in days using the days_between function
    return days_between(year, month, day, today.year, today.month, today.day)

