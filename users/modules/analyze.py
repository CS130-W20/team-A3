from datetime import datetime, timedelta
# now = datetime.now()
# now.year, now.month, now.day, now.hour, now.minute, now.second
# N = 2
# date_N_days_ago = datetime.now() - timedelta(days=N)
from random import random

fake_radar_data = [
    {
        'className': 'Long-Term', # optional can be used for styling
        'axes': [
            {'axis': "participation", 'value': 12}, 
            {'axis': "breadth of knowledge", 'value': 6}, 
            {'axis': "contribution", 'value': 5},  
            {'axis': "social interaction", 'value': 9},  
            {'axis': "mastery of skills", 'value': 2}
    ]},{
        'className': 'Recent',
        'axes': [
            {'axis': "participation", 'value': 6}, 
            {'axis': "breadth of knowledge", 'value': 7}, 
            {'axis': "contribution", 'value': 10},  
            {'axis': "social interaction", 'value': 12},  
            {'axis': "mastery of skills", 'value': 9}
    ]
  }
]

user_scores = ["participation", "breadth of knowledge", "contribution", "social interaction", "mastery of skills"]


def get_analyze_radar_data(user_id):
    # TODO: this function is temporarily fake, please implement it
    print("from users.modules.analyze.get_analyze_radar_data: please implement me")
    return fake_radar_data

def get_analyze_line_data(user_id, most_recent=10):
    # TODO: this function is temporarily fake, please implement it
    print("from users.modules.analyze.get_analyze_line_data: please implement me")
    # this is the fake data
    fake_line_chart_data = list()
    current_datetime = datetime.now()
    for i in range(most_recent):
        days_delta = most_recent - i # not including today
        tmp_date = current_datetime - timedelta(days=days_delta)
        tmp_date_str = "{:04d}{:02d}{:02d}".format(tmp_date.year, tmp_date.month, tmp_date.day)
        tmp_day_data = dict()
        tmp_day_data["date"] = tmp_date_str
        for s in user_scores:
            tmp_day_data[s] = 100 * random()
        fake_line_chart_data.append(tmp_day_data)
    return fake_line_chart_data
