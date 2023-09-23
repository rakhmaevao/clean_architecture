import os
import inspect
import sys

def analyze_project(project_path):
    sys.path.append(project_path)
    classes = {}
    modules = {}

    # Проходим по всем файлам в проекте с расширением .py
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                module_name = os.path.splitext(file)[0]
                module_path = os.path.join(root, file)
                modules[module_name] = module_path

                # Импортируем модуль для анализа его содержимого
                module = __import__(module_name)

                # Ищем классы в модуле
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        class_name = name
                        class_module = module_name

                        # Проверяем, используется ли класс в других модулях
                        class_usage = []
                        for module_name, module_path in modules.items():
                            if module_name != class_module:
                                # Загружаем другой модуль для анализа его содержимого
                                other_module = __import__(module_name)

                                # Ищем использование класса в другом модуле
                                for _, other_obj in inspect.getmembers(other_module):
                                    if inspect.isclass(other_obj):
                                        for attr_name, attr_value in vars(other_obj).items():
                                            if attr_value == obj:
                                                class_usage.append(module_name)
                                                break

                        classes[class_name] = (class_module, class_usage)

    return classes

# Пример использования скрипта
project_path = "/home/rahmaevao/Projects/clean_architecture/tests/mock_component"
result = analyze_project(project_path)
print(result)