curl -d '{"citizens": [{"citizen_id": 2, "town": "Москва", "street": "Льва Толстого", "building": "16к7стр5", "apartment": -1, "name": "Иванов Сергей Иванович", "birth_date": "01.04.1997", "gender": "male", "relatives": [1, 2] }, {"citizen_id": 1, "town": "Москва", "street": "Льва Толстого", "building": "16к7стр5", "apartment": 7, "name": "Иванов Сергей Иванович", "birth_date": "01.04.1997", "gender": "male", "relatives": [2]}]}' -H "Content-Type: application/json"  -X POST 'http://0.0.0.0:8080/imports'
