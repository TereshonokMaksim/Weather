import modules.widget
import modules.reg_window
'''
і
    Небольшая справка по проетку:

    Команда lambda: 1 + 1 в кнопках явлвяется заполнителем, предотвращает ошибку.
    Все текстовые поля имеют ширину 0 так как они ее изменяют автоматически вместе
    с текстом.
    Виджет не может никогда быть закрытым, это является сердцем программы по сути.

    
    Исправленные ошибки:

    Папка для датабазы и сама датабаза теперь умеет сама создаваться если была удалена.
    Убрано немного мусора
    Исключены ошибки связанные с временем в приложении (они не ложили программу, но давали неверную информацию пользователю)
    Часовые пояса теперь нормально учитываются
    Поиск иконок был немного перестроен чтобы не вызывать ошибок и были добавлены функции авто подгрузки в некоторые места в коде
    Загрузка функций в основное приложение теперь не сделано через передачу кучки функций в виде словарей в параметрах, а нормальным авто закрытием и открытием датабазы в нужные моменты
    Более мелкие исправления

    Список выполненых задач (тип - MD+):
    n - 0011 0101 %
    f - 0110 0000 %
    . - 1001 0000 %
    g - 0001 0101 %

'''