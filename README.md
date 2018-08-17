# DA Python Function Refactor Version

## Overview
Modules to control scenario flows in DA.

## Module Functions


 ### Function setTaskOutput(current_task, output_object, #current_da)
> 해당하는 Task의 output을 설정합니다.

> 이 함수의 Output Object에는 Transaction과 Response의 발화정보가 포함될 수 있습니다.

다음은 함수의 3가지 인자에 대한 개별적인 설명입니다.
```
current_task (Required) : 발화정보를 설정할 대상 Task의 이름입니다.

output_object (Required) : 발화 내용이 담긴 Object입니다. 이 Object에 대한 설명은 하위에 기술되어 있습니다.

current_da (Optional) : Response를 설정하기 위한 DA Type을 입력하는 곳입니다.
                        입력하지 않을 경우 자동으로 해당 Task의 Transaction만 설정되게 됩니다.
```

Task에 대한 __Transaction__ 과 __Response__ 발화 구문은 **output_object** 인자에 **JSON**을 선언한 변수를 이용해 입력시킬 수 있습니다.

* 다음은 **output_object** 인자에 들어가는 Object의 **예시** 형태입니다.
```
output_object_greet = {
    'default' : '안녕하세요',
    'request_user_info' : "유저 정보 안내입니다."
}
```

* 다음은 Object **output_object_greet**에 대한 설명입니다.

```
default : SDS 모니터상의 Transaction과 같은 역할을 합니다.
          Response가 따로 지정되지 않았을 경우, default 키값에 해당하는 내용이 태스크 진입 시 가장 먼저 발화하게 됩니다.

request_user_info(Example) : request_user_info DA에 해당하는 response의 발화 내용입니다.
```

Output을 설정할 Task의 대한 발화정보 Object가 준비되었다면,
해당하는 정보들을 함수 인자에 대입 시킴으로써 Task 발화정보 세팅이 완료됩니다.

* 다음은 **setTaskOutput()** 을 사용한 **Transaction** 설정 예시 코드입니다.
```
setTaskOutput("Greet", output_object_greet)
```

* 다음은 **setTaskOutput()** 을 사용한 **request_user_info DA** 에 관한 **Response** 설정 예시 코드입니다.
```
setTaskOutput("Greet", output_object_greet, "request_user_info")
```

---
### Function setNextTask(current_task, current_da, next_task, #query, #query_content)
> 해당하는 Task에서의 조건 충족 시 이동할 Task를 설정합니다.

다음은 함수의 5가지 인자에 대한 개별적인 설명입니다.
```
current_task (Required) : Task 이동정보를 설정할 대상 Task의 이름입니다.
current_da (Required) : Task 이동시 충족해야 할 DA의 이름입니다.
next_task (Required) : Task 이동시 이동 목표 Task의 이름입니다.
query (Optional) : Task 이동시 충족해야 할 조건식을 입력받는 인자입니다.
query_content (Optional) : Task 이동시 충족해야 할 조건식에 대한 값들이 포함된 Object를 입력받는 인자입니다.
```

Task에 대한 **Intent Query Filter Content**는 **query_content** 인자에 **JSON**을 선언한 변수를 이용해 입력시킬 수 있습니다.

* 다음은 **query_content** 인자에 들어가는 Object의 **예시** 형태입니다.

```
query_content = {
    'overdue_value' : '60000',
    'overdue_term' : 3
}
```

* 다음은 Object **query_content**에 대한 설명입니다.

```
overdue_value(Example) : Task 이동 조건식에 포함된 overdue_value에 대한 값입니다.

overdue_term(Example) : Task 이동 조건식에 포함된 overdue_term에 대한 값입니다.
```

**query_content** 내부에 조건식에 대입할 값들이 명시되었다면, 조건식을 이용하여 Task의 흐름을 관리할 수 있습니다.

* 다음은 **setNextTask** 내에서 Task의 흐름을 관리하는 조건문의 예시입니다.

```
overdue_value >= 5000 and overdue_term is not None
```

* 조건문은 Python v2.x 조건문 문법을 기반으로 작동하며, 사용자가 원하는 String 형태의 내용으로 수정이 가능합니다. 다음은 또 다른 조건문의 예시입니다.

```
query_content = {
	'user_number' : 3,
    'user_type' : "children"
}

user_number >=3 and user_type is "children"
```

유저의 수가 **3명 이상**이고, 유저가 모두 **어린이**일때의 조건을 설정하는 조건문입니다.

다음과 같이, **query_content와 query를 적절히 수정**하여 원하는 조건문을 설정할 수 있습니다.
**SDS 모니터** 상에서는 Task와 Response의 ***Condition*** 역할을 수행하는 기능과 동일합니다.

조건문은 ***setNextTask()***의 **Optional Argument** 이기에, 조건문을 설정하지 않고도 Task의 이동관계를 설정할 수 있습니다.

* 다음은 ***setNextTask()***를 사용한 Task Flow 설정 예시 코드입니다.
```
setNextTask("Greet", "request_user_info", "GreetAffirm")
```

* 다음은 ***setNextTask()***를 사용한 Task Flow 설정과 Task Move 조건 설정 예시 코드입니다.

```
query_content = {
	'overdue_value' : '60000',
    'overdue_term' : 3
}

setNextTask("Greet", "request_user_info", "GreetAffirm", "overdue_value >= 5000 and overdue_term is not none", query_content)
```

##Example

Greet -> GreetAffirm -> END1로 이루어진 간단한 Task 이동에 대한 소스코드입니다.

### SourceCode
```
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
print output
setTaskOutput("Greet", output_object_greet, "request_user_info")
print output
setNextTask("Greet", "request_user_info", "GreetAffirm", "overdue_value >= 5000 and overdue_term is not None", query_content)
print Temp_Tesk
setTaskOutput("GreetAffirm", output_object_greetAffirm)
print output
setNextTask("GreetAffirm", "request_user_info", "END1")
print Temp_Tesk
```

### Output
```
Transaction Utter At Task Greet : 안녕하세요
Response Utter of request_user_info DA at Task Greet : 유저 정보 안내입니다.
Task Is Now GreetAffirm
 Condition Satisfied!
Transaction Utter At Task GreetAffirm : GreetAffirm Transaction입니다.
Task Is Now END1
```