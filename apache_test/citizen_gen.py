## Этот файл создает json для 10000 горожан у которых парные связи

import copy

output = []
nmr = 9999
default_dict = {"citizen_id": 2, "town": "somewhere", "street": "42", "building": "12", "apartment": 5, "name": "Ivan", "birth_date": "01.05.1978", "gender": "male", "relatives": [1] }
while nmr > 1:
    default_dict["citizen_id"] = nmr
    if nmr % 2 == 0:
        default_dict["relatives"] = [nmr + 1]
    if nmr % 2 == 1:
        default_dict["relatives"] = [nmr - 1]
    nmr -= 1
    output.append(copy.deepcopy(default_dict))
print(str({"citizens": output}))
