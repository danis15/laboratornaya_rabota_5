import csv
import datetime
            
class Record:
    def __init__(self, date, time, area):
        self.date = date
        self.time = time
        self.area = area

    def __str__(self):
        return self.date + ',' + self.time + ',' + str(self.area)
                
class Combiner:
    def __init__(self, full_name, age):
        self.full_name = full_name
        self.age = age

    def __str__(self):
        return self.full_name + ',' + str(self.age)

class Combine:
    def __init__(self, model, performance):
        self.model = model
        self.performance = performance
        
    def __str__(self):
        """
		Метод преобразования объекта к строковому типу.
		"""
        if self.type is None:
            return 'no_type,' + self.model + ',' + str(self.performance)
        else:
            return self.type + ',' + self.model + ',' + str(self.performance)

class GrainCombine(Combine):
    def __init__(self, model, performance):
        """
		Конструктор производного класса.
		:param model: модель комбайна
		:param performance: производительность комбайна
		"""
        Combine.__init__(self, model, performance)
        self.type = "Зерноуборочный"
        
class BeetCombine(Combine):
    def __init__(self, model, performance):
        """
		Конструктор производного класса.
		:param model: модель комбайна
		:param performance: производительность комбайна
		"""
        Combine.__init__(self, model, performance)
        self.type = "Свеклоуборочный"

class PotatoCombine(Combine):
    def __init__(self, model, performance):
        """
		Конструктор производного класса.
		:param model: модель комбайна
		:param performance: производительность комбайна
		"""
        Combine.__init__(self, model, performance)
        self.type = "Картофелеуборочный"
        
class ForageCombine(Combine):
    def __init__(self, model, performance):
        """
		Конструктор производного класса.
		:param model: модель комбайна
		:param performance: производительность комбайна
		"""
        Combine.__init__(self, model, performance)
        self.type = "Кормоуборочный"

class InformationList:
    def __init__(self, filename):
        """
		Конструктор производного класса.
		:param filename: путь к файлу csv
		"""
        self.read(filename)
        self.__index = None
        self.__limit = None
        
    def __iter__(self):
        """
		Метод инициализации процесса итерации.
		"""
        setattr(self, "__index", 0)
        setattr(self, "__limit", len(self.list))
        return self

    def __next__(self):
        """
		Метод получения следующего элемента при итерации.
		"""
        if self.__index < self.__limit:
            data = self.list[self.__index]
            setattr(self, "__index", self.__index + 1)
            return data
        else:
            raise StopIteration

    def gen(self):
        """
        Генератор объектов списка.
        """
        for data in self.list:
            yield data
        
    def __repr__(self):
        """
		Метод репрезентации объекта.
		"""
        return repr(self.list)
    
    def __str__(self):
        """
		Метод преобразования объекта к строковому типу.
		"""
        s = str()
        for info in self.list:
            for data in info:
                s += str(data) + " | "
            s += '\n'
        return s

    def __setattr__(self, name, value):
        """
		Метод указания атрибута объекта.
		:param name: имя атрибута
		:param value: значение атрибута
		"""
        self.__dict__[name] = value

    def __getitem__(self, index):
        """
        Метод извлечения объекта коллекции по индексу.
        :param index: индекс извлекаемого значения
        """
        return self.list[index]
    
    """
    Ключи для извлечения необходимого значения из элемента списка.
    """
    @staticmethod
    def DATE_KEY(info):
        return datetime.datetime.strptime(info[0].date + ' ' + info[0].time, '%d.%m.%Y %H:%M')
    @staticmethod
    def AREA_KEY(info):
        return info[0].area
    @staticmethod
    def FULL_NAME_KEY(info):
        return info[1].full_name

    def sort(self, key, reverse=False):
        """
        Метод сортировки списка.
        :param key: ключ сортировки
        :param reverse: флаг обратной сортировки
        """
        self.list.sort(key=key, reverse=reverse)

    def filter(self, key, value, method):
        """
        Метод фильтрации списка от элементов с заданными параметрами.
        :param key: ключ фильтрации
        :param value: значение для фильтрации
        :param method: способ фильтрации ("==", ">=", "<" и т.д.)
        """
        new_list = list()
        for info in self.list:
            if key(info) == value:
                if method == "==" or method == ">=" or method == "<=":
                    continue
            elif key(info) > value:
                if method == ">=" or method == ">":
                    continue
            elif method == "<=" or method == "<":
                continue
            new_list.append(info)
        setattr(self, "list", new_list)
                
    def write(self, filename):
        """
		Метод записи списка информации в файл csv.
		:param filename: путь к файлу csv
		"""        
        file = open(filename, 'w', newline='')
        csv_writer = csv.writer(file, delimiter=',', quotechar='"')
        csv_writer.writerow(self.titles)
        for info in self.list:
            csv_writer.writerow([str(info[0]) + ',' + str(info[1]) + ',' + str(info[2])])
        
    def read(self, filename):
        """
		Метод чтения файла в формате csv.
		:param filename: путь к файлу csv
		"""
        file = open(filename, 'r')
        rows = list(csv.reader(file, delimiter=',', quotechar='"'))
        self.titles = rows[0]
        self.list = list()
        for row in rows[1:]:
            combine = None
            if row[5] == "Зерноуборочный":
                combine = GrainCombine(row[6], float(row[7]))
            elif row[5] == "Свеклоуборочный":
                combine = BeetCombine(row[6], float(row[7]))
            elif row[5] == "Картофелеуборочный":
                combine = PotatoCombine(row[6], float(row[7]))
            else:
                combine = ForageCombine(row[6], float(row[7]))
            self.list.append([Record(row[0], row[1], float(row[2])), 
                              Combiner(row[3], int(row[4])), 
                              combine])

if __name__ == "__main__":
    info_list = InformationList("data.csv") # инициализация списка информации
    print([str(date) for date in info_list[0]]) # обращение к элементу коллекции по индексу
    print(info_list) # вывод списка
    # сортировка в обратном порядке по дате
    info_list.sort(InformationList.DATE_KEY, reverse=True)
    print(info_list) # вывод списка
    # фильтрация (удаление) элементов списка, обработанная площадь в которых составляет менее 500
    info_list.filter(key=InformationList.AREA_KEY, value=500, method="<")
    print(info_list) # вывод списка
    info_list.write("data2.csv") # запись в файл списка информации