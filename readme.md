### Как запустить:
- py -m venv env
- env\Scripts\activate (или source env\bin\activate)
- pip install -r requirements.txt

### Тесты
pytest tests/test_main.py -v

### Функционал
- py main.py foo=bar
- py main.py --file example.csv --where "rating>4.7"
- py main.py --file example.csv --where "brand=apple"
- py main.py --file example.csv --aggregate "rating=avg"
- py main.py --file example.csv --where "brand=xiaomi" --aggregate "rating=avg"

### Как добавить новые методы
c = CSVReader()  
c.add_aggregation('name', func)  
c.read()  
  
### Как изменить текущие методы
c = CSVReader()  
c.set_aggregation('name', func)  
c.read()  

### FAQ
- Методы добавляются в класс CSVReader
- Поддерживатеся работа при отсутствии данных
- Созданы классы обработки ошибок