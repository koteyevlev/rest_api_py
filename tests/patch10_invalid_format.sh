curl -d '{"town": "Моsdfсква", "street": "Льва Толстого", "building": "16к7стр5", "apartment": 7, "name": "firstПервый чел", "birth_date": "01.11.98", "gender": "male", "relatives": [1, 2]}' -H "Content-Type: application/json"  -X PATCH 'http://0.0.0.0:8080/imports/17/citizens/1'
