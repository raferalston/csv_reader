- # CSV Reader

Утилита на Python для чтения, фильтрации и обработки данных из CSV-файлов с пользовательским интерфейсом в консоли.

## Как запустить:
- py -m venv env
- env\Scripts\activate (или source env\bin\activate)
- pip install -r requirements.txt

## Тесты
pytest tests/test_main.py -v

## Функционал
- py main.py foo=bar
- py main.py --file example.csv --where "rating>4.7"
- py main.py --file example.csv --where "brand=apple"
- py main.py --file example.csv --aggregate "rating=avg"
- py main.py --file example.csv --where "brand=xiaomi" --aggregate "rating=avg"

## Как добавить новые методы
c = CSVReader()  
c.add_aggregation('name', func)  
c.read()  
  
## Как изменить текущие методы
c = CSVReader()  
c.set_aggregation('name', func)  
c.read()  

## FAQ
- Методы добавляются в класс CSVReader
- Поддерживатеся работа при отсутствии данных
- Созданы классы обработки ошибок

## Назначение

Позволяет быстро просматривать и фильтровать содержимое CSV-файлов, делая акцент на удобстве командной работы с табличными данными. Подходит для начальной проверки больших CSV-файлов или анализа их структуры перед дальнейшей обработкой.

## Основной функционал

- Загрузка данных из CSV-файла
- Вывод первых/последних строк таблицы
- Фильтрация строк по значениям столбца
- Поддержка команд через консольный интерфейс

```bash
git clone https://github.com/raferalston/csv_reader.git
cd csv_reader
