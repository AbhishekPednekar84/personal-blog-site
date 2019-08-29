Title: A reminder app with Python, Twilio and AWS Lambda
Date: 2019-08-22 12:00
Category: Python
Tags: Python, AWS
Slug: reminders
Authors: Abhishek Pednekar
Summary: Send reminders on WhatsApp with Python, Twilio and AWS Lambda
Cover: /static/images/black-gradient-article.jpg

Recently, my wife and I missed the due date alert on a pretty important payment. This, despite having reminders set on our phones. Although we were able to sort it out without a lot of hassle, we knew that we couldn't afford a repeat of this scenario. Since an auto-payment (which I am not a big fan of anyways) wasn't an option here, additional alerting was the way to go. So as a true engineer, I decided to set up a custom alerting mechanism to which I would "hopefully" pay more attention. Since WhatsApp is pretty heavily used in my household, sending the reminder as a WhatsApp message to multiple phones seemed like a good idea. 

In this post, we will create a very simple Python (v3.7) script that calls the Twilio sandbox API to send an event reminder via WhatsApp. The reminder details and the list of recipients will be stored in separate json files. To run the script daily, we will be creating a function in AWS Lambda. 

The entire code is available in [this Github repository](https://github.com/AbhishekPednekar84/reminder_app_twilio_aws_lambda)

### Twilio
Before we get to the code, we will need to create a [Twilio](https://www.twilio.com/try-twilio) account. The process is pretty straightforward. Once you are logged in, you will see an **Account Security ID (SID)** and an **Authentication Token** in your Twilio Console Dashboard. Those are key parameters that will be needed to send the WhatsApp message. We'll be using those later when working with AWS. 

To set up the sandbox, navigate to the All Products and Services console and click on WhatsApp. Twilio will then give you a sandbox number (that can be saved as a contact on your phone) and walk you through the setup which involves sending an **activation code** to the sandbox number to enable messaging between your phone number and the sandbox. The short tutorial will also cover one-way and two-way messaging. Once you have sent the activation code from your phone to the sandbox number, you are all set to send and receive messages. If you would like other's to be able to communicate with the sandbox, the same activation code will need to be sent from their phones to the sandbox number. All the phone numbers that send the activation code will be listed as sandbox participants in your Twilio account.

![twilio1]({static}/images/index3/twilio1.jpg)

![twilio1]({static}/images/index3/twilio2.jpg)

When you use the sandbox to send a random message to your number, a 24-hour messaging window is created between the sandbox and your number. To extend this window for whatever reason, you will need to send a message back to the sandbox within those 24 hours. Luckily, the sandbox provides three messaging templates that do not follow this 24-hour rule. Messages composed using these templates can be sent any number of times at varying frequencies. The template that we will be using is `Your {{1}} appointment is coming up on {{2}}`. More on this in the next section.

### Python
To work with Twilio using Python, we'll need to install the twilio library using `pip install twilio`. But before that, let's create a [virtual environment](https://www.youtube.com/watch?v=APOPm01BVrk). This is optional but always a good practice to keep your project dependencies isolated. Alternately, you can `pip install` from the *requirements.txt* file in the repository - `pip install -r requirements.txt`. The requirements file includes the *pytest* and *pre-commit* libraries as well. pytest is being used to run a really really basic test in test_reminders.py. pre-commit runs a hook on the Python code before committing the code. You can learn more about pre-commit hooks in [this post](https://www.codedisciples.in/pre-commit.html). 


Next, let's create the two json files that I mentioned earlier.

* **reminder_events.json**

This file contains details such as the title of our reminder, it's frequency (monthly / yearly) and the due date. For monthly reminders, the due date will contain only the **day** as the reminder will be triggered on the same day each month. For the yearly reminders, the due date is in the format *month-day*. I did not have any weekly or quarterly events. Hence the subsequent code does not take those frequencies into consideration.

```
{
    "events": [
        {
            "title": "Electricity Bill",
            "due": "17",
            "frequency": "M"
        },
        {
            "title": "Car Insurance Premium",
            "due": "10-1",
            "frequency": "Y"
        }
    ]
}
```

* **directory.json**

This file contains all our recipient names and phone numbers.

```
{
    "members": [
        {
            "name": "Recipient 1",
            "phone": "+919xxxxxxxxx"
        },
        {
            "name": "Recipient 2",
            "phone": "+919xxxxxxxxx"
        }
    ]
}
```

*check_appointments()* is our primary method which will look for events that are due. This will also be called by the AWS Lambda function. Lambda refers to this method as the *handler*. The *event* and *context* parameters are specific to Lambda. [Click here](https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html) for additional information.   

First, we will extract the day and month from today's date. Additionally, we will format the date as *month, day* (Ex: *August, 22*). This is just a personal preference. Please refer to the [docs](https://docs.python.org/3.7/library/datetime.html?highlight=datetime#strftime-and-strptime-behavior) in case you would like a different format.

```
import json
import os
from twilio.rest import Client
from datetime import datetime


def check_appointments(event=None, context=None):
    current_day = datetime.today().day
    current_month = datetime.today().month

    formatted_date = datetime.today().strftime("%B, %d")

    with open("reminder_events.json", "r") as f:
    reminders = json.load(f)
```

Finally, our script will read the reminder_events.json file (using the [json](https://www.youtube.com/watch?v=9N6a-VLBa2I&t=543s) library and a [context manager](https://www.youtube.com/watch?v=-aKFBoZpiqA)) and iterate over its contents. In the `for` loop, the code checks if the due date (day or month-day combination) matches the current day. If yes, we then make a call to the *send_whatsapp_message* method to send the WhatsApp message. 

```
    for reminder in reminders["events"]:
        if reminder["frequency"] == "M":
            if reminder["due"] == str(current_day):
                send_whatsapp_message(reminder["title"], formatted_date)
        elif reminder["frequency"] == "Y":
            r_month, r_day = reminder["due"].split("-")

            if r_month == str(current_month) and r_day == str(current_day):
                send_whatsapp_message(reminder["title"], formatted_date)
```

*send_whatsapp_message* takes the event name from the json file and the formatted date as parameters.

```
def send_whatsapp_message(event_name, event_date):
    # The SID and TOKEN values will be read from the AWS Lambda Console
    account_sid = os.environ["account_sid"]
    auth_token = os.environ["auth_token"]

    # Create the Twilio client object
    client = Client(account_sid, auth_token)

    event_name = f"10 AM ({event_name})"

    # Read the recipient data from the directory.json file
    with open("directory.json", "r") as f:
        recipients = json.load(f)

    for recipient in recipients["members"]:
        message = client.messages.create(
            body=f"Your appointment is coming up on {event_date} at {event_name}",
            from_="WhatsApp:+14155238886",
            to=f"WhatsApp:{recipient['phone']}",
```

Remember the Twilio Account SID and the Authentication Token? We'll be adding them as environment variables in AWS in the next section. Right now, we will read the environment variable values into Python variables using `os.environ`. Once we read the contents of *directory.json*, we iterate over them and compose a message for each recipient.  +14155238886 is the sandbox number. Prefixing the **whatsapp:** is required for both the sender and the recipient numbers. 

Finally, the body of the message uses the template I mentioned earlier. In this pre-provisioned sandbox template, we only have the freedom to modify the values of the *event_name* and *event_date*. Although both are being passed as arguments to the method, I am modifying event name as *10 AM ({event_name})* just to make the message grammatically correct. So if I am being reminded about an electricity bill payment on August 31st, the message would read as `Your appointment is coming up on August, 31 at 10 AM (Electricity Bill)`. 10 AM is just a random time that I chose since my script will be running at around 10 AM local time. The message can, however, be modified in any way that one chooses as long as we stay true to the template.

### AWS Lambda

Now that we have our Python script and our Twilio sandbox ready to go, let's schedule the script in AWS Lambda. Sign up for the [AWS Free Tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc). In the AWS Management Console, look for Lambda.  

![lambda1]({static}/images/index3/lambda1.jpg)

On the following page, you will see an option to create a Lambda function. The free tier for Lambda offers 1M free requests per month. So its a great platform to run simple scripts like this. 

Give your function a name and select the runtime as Python 3.7

![lambda1]({static}/images/index3/lambda2.jpg)

On the configuration page, set the code entry type as Upload zip file. Next, set the two environment variables for the Account SID and the Authentication Token. Change the Handler to `module_name.function_name`. In this case, all our code is in the *reminders.py* file and we require the Lambda function to call the *check_appointments()* method. So, the handler will be `reminders.check_appointments`. I also set the timeout to 10 seconds from the default 3 seconds under Basic Settings. The script however, takes less than three seconds to complete, making this step optional.

**Creating the zip file** - copy reminders.py and the two json files to the *site-packages* directory. Since I used a virtual environment, the path on my laptop is `<Project_folder>/venv/Lib/site-packages`. Now, select all the contents of your site-packages directory and zip them. Please <u>do not</u> zip the site-packages directory itself, just the contents. Zipping the directory will result in a *Module not found* error when running the Lambda function. Give an appropriate name to the zip file and add it to the configuration.

![lambda1]({static}/images/index3/lambda3.jpg)

Next, add a trigger to set up our **cron** job. 

![lambda1]({static}/images/index3/lambda4.jpg)

In the Trigger configuration, select *CloudWatch Events*. Create a new rule with an appropriate name, specify the Rule Type as Schedule Expression and provide a cron expression. If you are new to cron, here's a link to the [AWS cron documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html?source=post_page---------------------------#CronExpressions). The time zone specified in the cron expression on Lambda is UTC by default. So `cron(30 4 * * ? *)` will execute our script at 4:30 AM UTC every day which is 10 AM local time for me. Make sure that the trigger is enabled and add it to the configuration. 

![lambda1]({static}/images/index3/lambda5.jpg)

If added successfully, you will see a new CloudWatch Event added to your function configuration.

![lambda1]({static}/images/index3/lambda6.jpg)

That's it! Now, whenever the script runs and finds an event that is due on the current day, it will send a WhatsApp message to your number.

![lambda1]({static}/images/index3/WhatsApp-final.jpg)








