Изменения в архитектуре Дерева решений:
Хотелось бы видеть вместо словаря yaml структуру,
причем чтобы функция определения хранилась в таком виде: Event:EventChecker
Т.к. нахожу такой вид более читабельным.
Итак:
```python
import yaml
s = """
NoDuckEvent: "There isn't any duck" in message.content
"""
yaml


```