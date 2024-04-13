# -*- coding: utf-8 -*-

from wox import Wox
import pyperclip

from Toggl import Toggl

class ToggleDataGetter(Wox):

    # query is default function to receive realtime keystrokes from wox launcher
    def query(self, query):
        results = []
        # results.append({
        #     "Title": "Hello World",
        #     "SubTitle": "Query: {}".format(query),
        #     "IcoPath":"Images/app.png",
        #     "ContextData": "ctxData",
        #     "JsonRPCAction": {
        #         'method': 'take_action',
        #         'parameters': ["{}".format("SomeData")],
        #         'dontHideAfterAction': False
        #     }
        # })

        
        # append yestarday, last week, last month

        results.append({
            "Title": "Yesterday",
            "SubTitle": "Query: {}".format(query),
            "IcoPath":"Images/app.png",
            "ContextData": "ctxData",
            "JsonRPCAction": {
                'method': 'get_yesterday_data',
                'parameters': ["{}".format("Yesterday")],
                'dontHideAfterAction': False
            }
        })

        results.append({
            "Title": "Last Week",
            "SubTitle": "Query: {}".format(query),
            "IcoPath":"Images/app.png",
            "ContextData": "ctxData",
            "JsonRPCAction": {
                'method': 'get_last_week_data',
                'parameters': ["{}".format("Last Week")],
                'dontHideAfterAction': False
            }
        })

        results.append({
            "Title": "Last Month",
            "SubTitle": "Query: {}".format(query),
            "IcoPath":"Images/app.png",
            "ContextData": "ctxData",
            "JsonRPCAction": {
                'method': 'get_last_month_data',
                'parameters': ["{}".format("Last Month")],
                'dontHideAfterAction': False
            }
        })

        return results

    # context_menu is default function called for ContextData where `data = ctxData`
    def context_menu(self, data):
        results = []
        # results.append({
        #     "Title": "Context menu entry",
        #     "SubTitle": "Data: {}".format(data),
        #     "IcoPath":"Images/app.png"
        # })
        
        return results

    def take_action(self, SomeArgument):
        # Choose what to trigger on pressing enter on the result.
        # use SomeArgument to do something with data sent by parameters.

        return None
    
    
    def get_yesterday_data(self, SomeArgument):
        toggl = Toggl()
        # resp = self.get_toggle_data("YESTERDAY")
        pyperclip.copy(toggl.GET_YESTERDAY_DATA())
        # pyperclip.copy("YESTERDAY DATA")
        return "Yesterday Data"
    
    def get_last_week_data(self, SomeArgument):
        # resp = self.get_toggle_data("LAST_WEEK")
        # pyperclip.copy(resp)
        toggl = Toggl()
        pyperclip.copy(toggl.GET_LAST_WEEK_DATA())
        return "Last Week Data"
    
    def get_last_month_data(self, SomeArgument):
        # resp = self.get_toggle_data("LAST_MONTH")
        # pyperclip.copy(resp)
        toggl = Toggl()
        pyperclip.copy(toggl.GET_LAST_MONTH_DATA())
        return "Last Month Data"

if __name__ == "__main__":
    ToggleDataGetter()
