#!/usr/bin/env python
import os
import sys
import django
from django.db import transaction

# Настраиваем окружение Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from tanda_backend.products.models.category import Category, CategoryOptionRequirement
from tanda_backend.products.models.options import OptionType


@transaction.atomic
def create_category_options():
    """
    Создает настройки опций для существующих категорий
    """
    print("Создание настроек опций для категорий...")
    
    # Получаем все типы опций
    try:
        color_type = OptionType.objects.get(code="color")
        size_type = OptionType.objects.get(code="size")
        material_type = OptionType.objects.get(code="material")
        memory_type = OptionType.objects.get(code="memory")
        processor_type = OptionType.objects.get(code="processor")
        screen_type = OptionType.objects.get(code="screen")
        weight_type = OptionType.objects.get(code="weight")
        style_type = OptionType.objects.get(code="style")
        
        print("Типы опций успешно получены")
    except OptionType.DoesNotExist as e:
        print(f"Ошибка: {e}")
        print("Убедитесь, что все необходимые типы опций созданы")
        return
    
    # Очищаем существующие настройки опций
    CategoryOptionRequirement.objects.all().delete()
    print("Существующие настройки опций удалены")
    
    # Получаем категории по именам
    categories = {}
    
    # Основные категории
    main_categories = ["Электроника", "Одежда", "Мебель", "Спорттовары"]
    for name in main_categories:
        try:
            categories[name] = Category.objects.get(name=name)
            print(f"Найдена категория: {name}")
        except Category.DoesNotExist:
            print(f"Категория '{name}' не найдена")
    
    # Подкатегории с особыми требованиями
    subcategories = [
        "Смартфоны", "Ноутбуки", "Планшеты", "Обувь", "Кровати", "Фитнес"
    ]
    for name in subcategories:
        try:
            categories[name] = Category.objects.get(name=name)
            print(f"Найдена подкатегория: {name}")
        except Category.DoesNotExist:
            print(f"Подкатегория '{name}' не найдена")
    
    # Создаем настройки для основных категорий
    
    # Электроника
    if "Электроника" in categories:
        CategoryOptionRequirement.objects.create(
            category=categories["Электроника"],
            option_type=color_type,
            is_main=True,
            is_required=True,
            sort_order=1
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Электроника"],
            option_type=weight_type,
            is_main=False,
            is_required=False,
            sort_order=2
        )
        print("Созданы настройки для категории 'Электроника'")
    
    # Смартфоны
    if "Смартфоны" in categories:
        CategoryOptionRequirement.objects.create(
            category=categories["Смартфоны"],
            option_type=color_type,
            is_main=True,
            is_required=True,
            sort_order=1
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Смартфоны"],
            option_type=memory_type,
            is_main=False,
            is_required=True,
            sort_order=2
        )
        print("Созданы настройки для категории 'Смартфоны'")
    
    # Ноутбуки
    if "Ноутбуки" in categories:
        CategoryOptionRequirement.objects.create(
            category=categories["Ноутбуки"],
            option_type=processor_type,
            is_main=True,
            is_required=True,
            sort_order=1
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Ноутбуки"],
            option_type=memory_type,
            is_main=False,
            is_required=True,
            sort_order=2
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Ноутбуки"],
            option_type=screen_type,
            is_main=False,
            is_required=True,
            sort_order=3
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Ноутбуки"],
            option_type=color_type,
            is_main=False,
            is_required=True,
            sort_order=4
        )
        print("Созданы настройки для категории 'Ноутбуки'")
    
    # Планшеты
    if "Планшеты" in categories:
        CategoryOptionRequirement.objects.create(
            category=categories["Планшеты"],
            option_type=screen_type,
            is_main=True,
            is_required=True,
            sort_order=1
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Планшеты"],
            option_type=memory_type,
            is_main=False,
            is_required=True,
            sort_order=2
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Планшеты"],
            option_type=color_type,
            is_main=False,
            is_required=True,
            sort_order=3
        )
        print("Созданы настройки для категории 'Планшеты'")
    
    # Одежда
    if "Одежда" in categories:
        CategoryOptionRequirement.objects.create(
            category=categories["Одежда"],
            option_type=size_type,
            is_main=True,
            is_required=True,
            sort_order=1
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Одежда"],
            option_type=color_type,
            is_main=False,
            is_required=True,
            sort_order=2
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Одежда"],
            option_type=material_type,
            is_main=False,
            is_required=False,
            sort_order=3
        )
        print("Созданы настройки для категории 'Одежда'")
    
    # Обувь
    if "Обувь" in categories:
        CategoryOptionRequirement.objects.create(
            category=categories["Обувь"],
            option_type=color_type,
            is_main=True,
            is_required=True,
            sort_order=1
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Обувь"],
            option_type=size_type,
            is_main=False,
            is_required=True,
            sort_order=2
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Обувь"],
            option_type=material_type,
            is_main=False,
            is_required=True,
            sort_order=3
        )
        print("Созданы настройки для категории 'Обувь'")
    
    # Мебель
    if "Мебель" in categories:
        CategoryOptionRequirement.objects.create(
            category=categories["Мебель"],
            option_type=material_type,
            is_main=True,
            is_required=True,
            sort_order=1
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Мебель"],
            option_type=color_type,
            is_main=False,
            is_required=True,
            sort_order=2
        )
        print("Созданы настройки для категории 'Мебель'")
    
    # Кровати
    if "Кровати" in categories:
        CategoryOptionRequirement.objects.create(
            category=categories["Кровати"],
            option_type=material_type,
            is_main=True,
            is_required=True,
            sort_order=1
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Кровати"],
            option_type=color_type,
            is_main=False,
            is_required=True,
            sort_order=2
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Кровати"],
            option_type=size_type,
            is_main=False,
            is_required=True,
            sort_order=3
        )
        print("Созданы настройки для категории 'Кровати'")
    
    # Спорттовары
    if "Спорттовары" in categories:
        CategoryOptionRequirement.objects.create(
            category=categories["Спорттовары"],
            option_type=color_type,
            is_main=True,
            is_required=True,
            sort_order=1
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Спорттовары"],
            option_type=material_type,
            is_main=False,
            is_required=False,
            sort_order=2
        )
        print("Созданы настройки для категории 'Спорттовары'")
    
    # Фитнес
    if "Фитнес" in categories:
        CategoryOptionRequirement.objects.create(
            category=categories["Фитнес"],
            option_type=weight_type,
            is_main=True,
            is_required=True,
            sort_order=1
        )
        CategoryOptionRequirement.objects.create(
            category=categories["Фитнес"],
            option_type=color_type,
            is_main=False,
            is_required=True,
            sort_order=2
        )
        print("Созданы настройки для категории 'Фитнес'")
    
    print("Настройки опций для категорий успешно созданы!")


if __name__ == "__main__":
    create_category_options()
