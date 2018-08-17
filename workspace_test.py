# -*- coding: utf-8 -*-
from tkinter import *
import json
import warnings

warnings.filterwarnings("ignore")

def previousUtter(da_name):
    return true

def hasValue(slot_name):
    return true

def getValue(slot):
    return true

def utterHistory(da_name, turn):
    return true
    

def setTaskOutput(current_task, output_object, current_da=""):
    if Temp_Tesk == current_task:
        if current_da == "":
            output_string = json.dumps(output_object)
            output_dict = json.loads(output_string)
            global output
            output = output_dict['default']
        elif current_da is not "":
            output_string = json.dumps(output_object)
            output_dict = json.loads(output_string)
            global output
            output = output_dict[current_da]

def setNextTask(current_task, current_da, next_task, query="", query_content={}):
    if Temp_Tesk == current_task and query == "":
        if Temp_dialog_act == current_da:
            global Temp_Tesk
            Temp_Tesk = next_task
        else:
            global Temp_Tesk
            Temp_Tesk = 'unknown'
    elif Temp_Tesk == current_task and query is not "":
        query_content_string = json.dumps(query_content)
        query_content_dict = json.loads(query_content_string)
        keys = query_content_dict.keys()
        for i in keys:
            query = query.replace(i, "query_content['" + i + "']")
        query = "if " + query + ''':
            global Temp_Tesk
            Temp_Tesk = next_task
        '''
        exec query

# ----------- Example Codes -----------

Tesk = "Greet"
dialog_act = "request_user_info"
Temp_dialog_act = "request_user_info"
Temp_Tesk = "Greet"
output = ""
output_object_greet = {
    'default' : '안녕하세요',
    'request_user_info' : "유저 정보 안내입니다."
}
output_object_greetAffirm = {
    'default' : "GreetAffirm Transaction입니다."
}
query_content = {
    'overdue_value' : '60000',
    'overdue_term' : 3
}


setTaskOutput("Greet", output_object_greet)
print "Transaction Utter At Task Greet : " + output
setTaskOutput("Greet", output_object_greet, "request_user_info")
print "Response Utter of request_user_info DA at Task Greet : " + output
setNextTask("Greet", "request_user_info", "GreetAffirm", "overdue_value >= 5000 and overdue_term is not None", query_content)
print "Task Is Now " + Temp_Tesk + "\n Condition Satisfied!"
setTaskOutput("GreetAffirm", output_object_greetAffirm)
print "Transaction Utter At Task GreetAffirm : " + output
setNextTask("GreetAffirm", "request_user_info", "END1")
print "Task Is Now " + Temp_Tesk
