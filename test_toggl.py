import pyperclip
from Toggl import Toggl

toggl = Toggl()

data = toggl.GET_YESTERDAY_DATA()
# data = toggl.GET_LAST_WEEK_DATA()
# data = toggl.GET_LAST_MONTH_DATA()

pyperclip.copy(data)

print("Data copied to clipboard!")