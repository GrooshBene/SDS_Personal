# -*- coding: utf-8 -*-
import json
import warnings
import re

warnings.filterwarnings("ignore")

def setTaskOutput(current_task, output_object, query = True, da_name = "inform"):
    if Temp_Task == current_task:
        if query == True:
            global output
            global Previous_Da
            global Previous_Target
            output = output_object
            Previous_Da = da_name
            Previous_Target = "system"
        elif query == False:
            return 1
    elif Temp_Task != current_task:
        return 1

def setNextTask(current_task, next_task, query=True):
    global Temp_Task
    if Temp_Task == current_task and query == True:
        Temp_Task = next_task
    elif Temp_Task == current_task and query != True:
        return 1

def previousUtter(target, da_name):
    if Previous_Da == da_name and Previous_Target == target:
        return True
    elif Previous_Da != da_name or Previous_Target != target:
        return False

def createSlot(slot_class, slot_name):
    global slot_objects
    slot_class = slot_class.title()
    slot_name = slot_class + "." + slot_name
    slot_objects[slot_name] = ""
    print "Slot Created : " + slot_name

def setSlotValue(slot_name, slot_content):
    global slot_objects
# NLP & NLG
    slot_objects[slot_name] = slot_content
    print "Slot Value Set"

def hasValue(slot_name):
    global slot_objects
    slot_content_string = json.dumps(slot_objects)
    slot_content_dict = json.loads(slot_content_string)
    keys = slot_content_dict.keys()

    if slot_name in keys:
        if slot_content_dict[slot_name] is not None:
            return True
        elif slot_content_dict[slot_name] is None:
            return False


def getValue(slot_name):
    global slot_objects
    return slot_objects[slot_name]

#TODO
def utterHistory(da_name, turn):
    return True
#END

def systemUtter(user_utter = False, filter = [], da_name = []):
    global output
    p = re.compile("<\w*.\w*>")
    m = p.findall(output)
    for i in m:
        i = i.replace("<", "").replace(">", "")
        slot_value = getValue(i)
        i = "<" + i + ">"
        output = output.replace(str(i), str(slot_value))
    if user_utter == True:
        print "Transaction Utter At Task Greet : " + output
        user_utter = raw_input()
        for i in filter:
            if i in user_utter and da_name is not []:
                global Previous_Da
                Previous_Da = da_name[filter.index(i)]
                break
            elif i not in user_utter and da_name is not []:
                print "Unknown"
                if filter.index(i) != len(filter)-1:
                    continue
                elif filter.index(i) == len(filter)-1:
                    systemUtter(True, filter, da_name)
    elif user_utter == False:
        print "Transaction Utter At Task " + Temp_Task + " : " + output
    if Temp_Task == "END":
        print "Session Closed"

#Function for Customize(Using Restful API, Access DB, etc.)
def perform():
    #Enter Your Code Here

    return True

#Function End

def debug(options = ""):
    print "Task : " + Temp_Task
    print "Previous DA : " + Previous_Da
    print "Previous Target : " + Previous_Target
    print "Output : " + output


Task = "Greet"
Previous_Da = ""
Previous_Target = ""
Temp_Task = "Greet"
output = ""

slot_objects = {}
createSlot("user", "money")
createSlot("user","name")
createSlot("user2", "money")
createSlot("user2", "name")
setSlotValue("User.money", 10000)
setSlotValue("User.name", "박지수")
setSlotValue("User2.money", 20000)
setSlotValue("User2.name", "김학성")

setTaskOutput("Greet", "안녕하세요, 무엇을 도와드릴까요?")
systemUtter(True, ['잔여요금안내'], ["user_inform"])
setTaskOutput("Greet", "잔여요금을 알고 싶으시군요. 성함을 말씀해 주세요!", previousUtter("system", "user_inform"))
systemUtter(True, ['박지수', '김학성'], ["inform_name", "inform_name2"])
setNextTask("Greet", "UserInfo", previousUtter("system", "inform_name"))
setNextTask("Greet", "UserInfo2", previousUtter("system", "inform_name2"))
setTaskOutput("UserInfo", "<User.name> 회원님의 잔여 요금은 <User.money>원 입니다.", True, "user_info_money")
setTaskOutput("UserInfo2", "<User2.name> 회원님의 잔여 요금은 <User2.money>원 입니다.", True, "user_info_money")
setNextTask("UserInfo", "END", previousUtter("system", "user_info_money"))
systemUtter()
