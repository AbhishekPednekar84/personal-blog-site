Title: Working with date and time in Python
Date: 2020-06-10 21:00
Category: Python
Tags: Python
Slug: datetime
Authors: Abhishek Pednekar
Summary: A look at Python's awesome `datetime` library
Cover: /static/images/gradient-texture-cubes.jpg

In this post, you will learn how to effectively use Python's built-in `datetime` library. Working with dates and time is a fundamental concept with any programming language. Python's `datetime` library makes this simple by exposing a wide range of methods and attributes.

To keep the examples succinct, the `import datetime` statement will be excluded in all but the first code snippet. This post covers a more widely used subset of the attributes and methods provided by the `datetime` library. For the complete list, refer to the [official documentation](https://docs.python.org/3/library/datetime.html).

## Aware vs. Naive

Python's date and time objects can be classified as **aware** or **naive** depending on whether they include time zone information or not.

An **aware** object contains details like the time zone and daylight saving time information whereas a **naive** object does not. In one of the subsequent sections, you will learn how to convert a naive object to an aware object.

## `date` objects

A `date` object in Python represents a date in the (year, month, day) format.

```
>>> import datetime

>>> d = datetime.date(2020, 6, 10)

>>> d
datetime.date(2020, 6, 10)
```

<i class="fas fa-clipboard"></i> Note that the `month` part of the `date` object should not be prefixed with `0`. If the `month` in the example is specified as `06` instead of `6`, you will receive an `invalid token` error.

To access the year, the month or the day from a `date` object, you can use the `year`, `month`, `day` attributes respectively.

```
>>> d.year
2020

>>> d.month
6

>>> d.day
10
>>>
```

Another common use case of any datetime library is to access the current local date. You can do this with the `today()` method.

```
>>> datetime.date.today()
datetime.date(2020, 6, 10)
```

To get the day of the week, you can use either the `weekday()` or the `isoweekday()` methods.

- `weekday()` - Monday <i class="fas fa-arrow-right"></i> 0; Sunday <i class="fas fa-arrow-right"></i> 6
- `isoweekday()` - Monday <i class="fas fa-arrow-right"></i> 1; Sunday <i class="fas fa-arrow-right"></i> 7

```
>>> dt = datetime.date.today()
>>> dt.weekday()
2
>>> dt.isoweekday()
3
```

## `time` objects

To work with time, the `datetime` library provides a `time` object which represents time in the (hours, minutes, seconds, microseconds) format.

```
>>> t = datetime.time(10, 30, 27, 100000)

>>> t
datetime.time(10, 30, 27, 100000)
```

To access specific time parameters, you can use the `hour`, `minute`, `second` and `microsecond` attributes.

```
>>> t.hour
10

>>> t.minute
30

>>> t.second
27

>>> t.microsecond
100000
```

## `timedelta` objects

A `timedelta` object represents the difference between two dates or times. It takes the following arguments - `days`, `seconds`, `microseconds`, `milliseconds`, `minutes`, `hours`, `weeks`.

### `timedelta` arithematic with `date` objects.

<i class="fas fa-angle-double-right"></i> Adding or subtracting two `date` objects will result in a `timedelta` <i class="fas fa-arrow-right"></i> `date +/- date2 = timedelta`.

```
# Subtracting two dates

>>> date1 = datetime.date(2020, 6, 10)
>>> date2 = datetime.date(2020, 6, 11)

>>> diff = date2 - date1
>>> diff
datetime.timedelta(days=1)

```

To get the total seconds in a `timedelta`, you can use the `total_seconds()` method.

```
>>> diff.total_seconds()
86400.0
```

<i class="fas fa-angle-double-right"></i> Adding or subtracting a `timedelta` from a `date` object will result in another date <i class="fas fa-arrow-right"></i> `date1 +/- timedelta = date2`

```
# Today's date + 5

>>> tday = datetime.date.today()
>>> tdelta = datetime.timedelta(days=5)

>>> tday + tdelta
datetime.date(2020, 6, 15)
```

## `datetime` objects

A `datetime` object is essentially a combination of the `date` and `time` objects. It takes all the arguments of the `date` and `time` objects combined. In addition to this, you can also pull the entire date and the time parts separately using the `date()` and `time()` methods.

```
>>> dt = datetime.datetime(2020, 6, 10, 9, 30, 0, 000000)
>>> dt
datetime.datetime(2020, 6, 10, 9, 30)

>>> dt.date()
datetime.date(2020, 6, 10)

>>> dt.time()
datetime.time(9, 30)

>>> dt.day
10

>>> dt.month
6

>>> dt.hour
9

>>> dt.microsecond
0
```

The `datetime` object can also be used with a `timedelta` object.

```
>>> tdelta = datetime.timedelta(days=10)
>>> dt + tdelta
datetime.datetime(2020, 6, 20, 9, 30)

>>> tdelta = datetime.timedelta(hours=12)
>>> dt + tdelta
datetime.datetime(2020, 6, 10, 21, 30)
```

## Alternative constructors for the `datetime` object

### `datetime.today()`

The `datetime.today()` method returns the local date and time **without** any time zone information.

```
>>> dt_today = datetime.datetime.today()
>>> dt_today
datetime.datetime(2020, 6, 10, 13, 3, 40, 691966)
```

### `datetime.now()`

The `datetime.now()` method returns the local date and time. It, however, accepts an optional time zone (`tz`) argument. `tz` has a default value of `None`. Time zones will be the focus of the next section.

```
>>> dt_today = datetime.datetime.today()
>>> dt_today
datetime.datetime(2020, 6, 10, 13, 3, 40, 691966)
```

### `datetime.utcnow()`

The `datetime.now()` method returns UTC (Coordinated Universal Time) without any time zone information.

```
>>> dt_utc_now = datetime.datetime.utcnow()
>>> dt_utc_now
datetime.datetime(2020, 6, 10, 7, 40, 37, 488672)
```

## Time zones

Time zones are a critical aspect of working with dates and times. Fortunately, the `pytz` module simplifies this. Note that `pytz` is the recommended module in Python's official documentation for working with time zones. `pytz` is not a part of the Python standard library. To install `pytz`, you will need to run `pip install pytz`.

The [documentation](https://pythonhosted.org/pytz/) for `pytz` recommends that you work with UTC and convert to a local time only when generating a time output that will be read by humans.

To create a time zone aware `datetime` object, you can simply pass the `tzinfo=pytz.utc` argument to it.

```
>>> import pytz

>>> dt_tz = datetime.datetime(2020, 6, 10, 9, 30, 0, 000000, tzinfo=pytz.UTC)
>>> dt_tz
datetime.datetime(2020, 6, 10, 9, 30, tzinfo=<UTC>)
```

In the previous section, you saw that the `datetime.now()` method accepts an optional time zone. You can pass the `tz=pytz.UTC` argument to the method to generate the current UTC.

```
>>> dt_now_utc = datetime.datetime.now(tz=pytz.utc)
>>> dt_now_utc
datetime.datetime(2020, 6, 10, 8, 10, 26, 309377, tzinfo=<UTC>)
```

Although the `datetime.utcnow()` method generates the UTC, it is not time zone aware. To make it time zone aware, you can chain `.replace(tzinfo=pytz.UTC)` to it.

```
>>> dt_utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
>>> dt_utc_now
datetime.datetime(2020, 6, 10, 8, 13, 21, 597852, tzinfo=<UTC>)
```

## Time zone conversions

Thus far, all the aware `datetime` objects have been in UTC. However, UTC can be converted to other time zones which is what you will be doing in most cases. To view all the time zones provided by `pytz` or to determine your current time zone, you can loop over the `all_time zones` attribute.

```
>>> for _ in pytz.all_time zones:
	    print(_)

Africa/Abidjan
Africa/Accra
Africa/Addis_Ababa
Africa/Algiers
...
...
US/Samoa
UTC
Universal
W-SU
WET
Zulu
```

The conversion methods will differ depending on whether you are working with a naive or an aware `datetime` object.

### Convert aware `datetime` objects

To convert an aware `datetime` object to any time zone, you will use the `astimezone()` method and pass the required time zone information to it. Note that `astimezone()` **cannot** be used with naive objects. In the next section, you will see how naive objects can be converted to a specific time zone.

Below example converts UTC to first, the Indian Standard Time (IST) followed by the US Central time (CST/CDT). For the latter, note that the current daylight saving time is returned.

```
# Create the aware datetime object

>>> dt_utc = datetime.datetime.now(tz=pytz.UTC)
>>> dt_utc
datetime.datetime(2020, 6, 10, 10, 0, 32, 42287, tzinfo=<UTC>)

# Convert UTC to IST

>>> dt_ist = dt_utc.astime zone(pytz.timezone("Asia/Calcutta"))
>>> dt_ist
datetime.datetime(2020, 6, 10, 15, 30, 32, 42287, tzinfo=<DstTzInfo 'Asia/Calcutta' IST+5:30:00 STD>)

# Convert UTC to CST/CDT

>>> dt_cdt = dt_utc.astime zone(pytz.timezone("US/Central"))
>>> dt_cdt
datetime.datetime(2020, 6, 10, 5, 0, 32, 42287, tzinfo=<DstTzInfo 'US/Central' CDT-1 day, 19:00:00 DST>)
```

### Convert naive `datetime` objects

To convert a naive object to a specific time zone is a two-step process -

1. Convert the naive object to an aware `datetime` object using the `localize()` method<br />
2. Convert the aware object to the preferred time zone using `astimezone()`

```
# Create the naive object

>>> dt_now = datetime.datetime.now()
>>> dt_now
datetime.datetime(2020, 6, 10, 16, 3, 4, 110521)

# Convert the naive object to aware for the local time zone (IST)

>>> tz_ist = pytz.timezone("Asia/Calcutta")
>>> dt_now = tz_ist.localize(dt_now)
>>> dt_now
datetime.datetime(2020, 6, 10, 16, 3, 4, 110521, tzinfo=<DstTzInfo 'Asia/Calcutta' IST+5:30:00 STD>)

# Convert IST to CDT

>>> dt_cdt = dt_now.astime zone(pytz.timezone("US/Central"))
>>> dt_cdt
datetime.datetime(2020, 6, 10, 5, 33, 4, 110521, tzinfo=<DstTzInfo 'US/Central' CDT-1 day, 19:00:00 DST>)
```

The above example first creates a naive object called `dt_now` which returns the local time. Next, `dt_now` is converted to an aware object for the same time zone (IST in this case) using the `localize()` method. Note that the result of this conversion is being saved in `dt_now` itself. Finally, the `datetime` object is being converted from IST to CDT using the `astimezone()` method.

## `datetime` formatting

### ISO format

The ISO (International Organization for Standardization) date format is a globally accepted standard to represent a date. This was introduced to standardize the date format and to eliminate any ambiguity. For instance, North Americans write the month before the day whereas, in Europe and Asia, the month is usually written after the day. The date separators also vary between a hyphen (-) and a forward slash (/).

Both naive and aware `datetime` objects can be converted to the ISO format using the `isoformat()` method.

```
# Naive to ISO

>>> dt_now = datetime.datetime.now()
>>> dt_now.isoformat()
'2020-06-10T16:25:54.248241'

# Aware to ISO

>>> dt_now = datetime.datetime.now(tz=pytz.timezone("Asia/Calcutta"))
>>> dt_now.isoformat()
'2020-06-10T16:29:07.232477+05:30'

```

### `strftime`

The `strftime()` method converts the `datetime` object to a `string`. Furthermore, it accepts format codes as parameters to represent the `datetime` in the desired format. The complete [list of format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) are available in the official documentation.

The format codes can be applied to both naive and aware objects.

```
# Formatting naive objects

>>> dt_now = datetime.datetime.now()
>>> dt_now.strftime("%B, %Y")
'June, 2020'

# Formatting aware objects

>>> dt_now = datetime.datetime.now(tz=pytz.timezone("Asia/Calcutta"))
>>> dt_now.strftime("%d-%B-%Y - %I:%M:%S %p")
'10-June-2020 - 04:35:54 PM'
```

### `strptime`

The `strftime()` method converts a `string` to a `datetime` object. This method also accepts format codes. The codes should match the string being converted.

```
>>> dt_str = "03/30/2020"
>>> dt = datetime.datetime.strptime(dt_str, "%m/%d/%Y")
>>> dt
datetime.datetime(2020, 3, 30, 0, 0)

>>> dt_str = "June 10, 2020"
>>> dt = datetime.datetime.strptime(dt_str, "%B %d, %Y")
>>> dt
datetime.datetime(2020, 6, 10, 0, 0)

>>> dt_str = "10-June-2020 - 04:35:54 PM"
>>> dt = datetime.datetime.strptime(dt_str, "%d-%B-%Y - %I:%M:%S %p")
>>> dt
datetime.datetime(2020, 6, 10, 16, 35, 54)

```

## Conclusion

Python's `datetime` library makes it easy to work with dates and times. When used in conjunction with the third-party `pytz` module, it enables straightforward conversions between time zones.

You should now be familiar with naive and aware objects, working with deltas and converting between time zones.
