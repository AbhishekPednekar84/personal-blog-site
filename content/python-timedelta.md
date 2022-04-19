Title: Hours, days and weeks with Python
Date: 2022-04-19 21:00
Category: Python
Tags: Python
Slug: python-timedelta
Authors: Abhishek Pednekar
Summary: Hours, days and weeks with Python
Cover: /static/images/gradient-texture-cubes.jpg

Python does not have a built-in function to directly compute the number of hours, days or weeks between two given datetime values. This article will show how we can use the `timedelta` class of python's `datetime` module to do exactly that.

A rather obvious way to compute the number of days (for example) between two dates is to use `total_seconds()`.
<br />

```
import datetime as dt

yesterday = dt.datetime(2022, 4, 18, 22, 0, 0, 0)
today = dt.datetime(2022, 4, 19, 22, 0, 0, 0)

difference = today - yesterday # Returns datetime.timedelta(days=1)

days = difference.total_seconds() / 24 / 60 / 60

print(int(days)) # Returns 1

```

Python does have a non-obvious way to do this by dividing the difference between the datetime values with the `timedelta`.
<br />

```
import datetime as dt

today = dt.datetime(2022, 4, 19, 22, 0, 0, 0)
week_from_today = dt.datetime(2022, 4, 26, 22, 0, 0, 0)

diff = week_from_today - today
```

### Total hours

```
total_hours = int(diff/dt.timedelta(hours=1)) # Returns 168 (24 * 7)
```

### Total days

```
total_days = int(diff/dt.timedelta(days=1)) # Returns 7
```

### Total weeks

```
total_weeks = int(diff/dt.timedelta(weeks=1)) # Returns 1
```

For an in-depth look at python's `datetime` module, check out [Working with date and time in Python](https://codedisciples.in/datetime.html).
