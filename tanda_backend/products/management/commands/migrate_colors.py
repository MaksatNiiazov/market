import csv
import os

from django.core.management.base import BaseCommand

from tanda_backend.products.models import OptionValue, OptionType, CategoryOptionRequirement, Category
from tanda_backend.products.services.category_option_events import send_option_value_created_event, \
    send_category_option_requirement_created_event, send_category_created_event, send_option_type_created_event


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(current_dir, "colors.csv")
        print("\n1. Создание категорий...")
        categories = create_categories()

        print("\n2. Создание типов опций...")
        option_types = create_option_types()

        print("\n3. Создание значений опций...")
        option_values = create_option_values(option_types)

        print("\n4. Создание связей категорий с опциями...")
        create_option_requirements(categories, option_types)

        option_type = OptionType.objects.get(code="color")
        try:
            with open(csv_file_path, "r", encoding="utf-8") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    columns = list(row.values())
                    value, is_created = OptionValue.objects.get_or_create(
                        option_type=option_type,
                        value=columns[0],
                        defaults={"meta_data": {"hex": columns[1]}}
                    )
                    if is_created:
                        send_option_value_created_event(value)

                self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Файл {csv_file_path} не найден"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при загрузке: {e}"))

def create_categories():
    """Создание иерархии категорий"""

    # Создание основных категорий
    electronics, created = Category.objects.get_or_create(name="Электроника", parent=None)
    if created:
        send_category_created_event(electronics)

    household, created = Category.objects.get_or_create(name="Бытовая техника", parent=None)
    if created:
        send_category_created_event(household)

    clothing, created = Category.objects.get_or_create(name="Одежда", parent=None)
    if created:
        send_category_created_event(clothing)

    # Подкатегории Электроники
    computers_phones, created = Category.objects.get_or_create(
        name="Ноутбуки и компьютеры",
        parent=electronics
    )
    if created:
        send_category_created_event(computers_phones)

    smartphones, created = Category.objects.get_or_create(
        name="Смартфоны и телефоны",
        parent=electronics
    )
    if created:
        send_category_created_event(smartphones)

    tv_video, created = Category.objects.get_or_create(
        name="Телевизоры и видеотехника",
        parent=electronics
    )
    if created:
        send_category_created_event(tv_video)

    # Под-подкатегории Ноутбуков и компьютеров
    laptops, created = Category.objects.get_or_create(name="Ноутбуки", parent=computers_phones)
    if created:
        send_category_created_event(laptops)

    ultrabooks, created = Category.objects.get_or_create(name="Ультрабуки", parent=computers_phones)
    if created:
        send_category_created_event(ultrabooks)

    smartphones_sub, created = Category.objects.get_or_create(name="Смартфоны", parent=smartphones)
    if created:
        send_category_created_event(smartphones_sub)

    televisions, created = Category.objects.get_or_create(name="Телевизоры", parent=tv_video)
    if created:
        send_category_created_event(televisions)

    # Подкатегории Бытовой техники
    kitchen_tech, created = Category.objects.get_or_create(
        name="Техника для кухни",
        parent=household
    )
    if created:
        send_category_created_event(kitchen_tech)

    beauty_health, created = Category.objects.get_or_create(
        name="Техника для красоты и здоровья",
        parent=household
    )
    if created:
        send_category_created_event(beauty_health)

    large_household, created = Category.objects.get_or_create(
        name="Крупная бытовая техника",
        parent=household
    )
    if created:
        send_category_created_event(large_household)

    home_tech, created = Category.objects.get_or_create(
        name="Техника для дома",
        parent=household
    )
    if created:
        send_category_created_event(home_tech)

    climate_tech, created = Category.objects.get_or_create(
        name="Климатическая техника",
        parent=household
    )
    if created:
        send_category_created_event(climate_tech)

    # Под-подкатегории кухонной техники
    electric_kettles, created = Category.objects.get_or_create(
        name="Электрические чайники и термопоты",
        parent=kitchen_tech
    )
    if created:
        send_category_created_event(electric_kettles)

    blenders, created = Category.objects.get_or_create(
        name="Блендеры, измельчители и миксеры",
        parent=kitchen_tech
    )
    if created:
        send_category_created_event(blenders)

    juicers, created = Category.objects.get_or_create(name="Соковыжималки", parent=kitchen_tech)
    if created:
        send_category_created_event(juicers)

    microwaves, created = Category.objects.get_or_create(name="Микроволновки", parent=kitchen_tech)
    if created:
        send_category_created_event(microwaves)

    meat_grinders, created = Category.objects.get_or_create(
        name="Мясорубки и насадки",
        parent=kitchen_tech
    )
    if created:
        send_category_created_event(meat_grinders)

    coffee_machines, created = Category.objects.get_or_create(
        name="Кофеварки и кофемашины",
        parent=kitchen_tech
    )
    if created:
        send_category_created_event(coffee_machines)

    hair_dryers, created = Category.objects.get_or_create(
        name="Фены и аксессуары",
        parent=beauty_health
    )
    if created:
        send_category_created_event(hair_dryers)

    # Крупная бытовая техника
    refrigerators, created = Category.objects.get_or_create(
        name="Холодильники",
        parent=large_household
    )
    if created:
        send_category_created_event(refrigerators)

    freezers, created = Category.objects.get_or_create(
        name="Морозильные камеры",
        parent=large_household
    )
    if created:
        send_category_created_event(freezers)

    washing_machines, created = Category.objects.get_or_create(
        name="Стиральные машины",
        parent=large_household
    )
    if created:
        send_category_created_event(washing_machines)

    wine_cabinets, created = Category.objects.get_or_create(
        name="Винные и сигарные шкафы",
        parent=large_household
    )
    if created:
        send_category_created_event(wine_cabinets)

    vacuum_cleaners, created = Category.objects.get_or_create(
        name="Пылесос",
        parent=home_tech
    )
    if created:
        send_category_created_event(vacuum_cleaners)

    irons, created = Category.objects.get_or_create(
        name="Утюг и отпариватели",
        parent=home_tech
    )
    if created:
        send_category_created_event(irons)

    air_conditioners, created = Category.objects.get_or_create(
        name="Кондиционеры и сплит-системы",
        parent=climate_tech
    )
    if created:
        send_category_created_event(air_conditioners)

    # Подкатегории Одежды
    mens_clothing, created = Category.objects.get_or_create(name="Мужская", parent=clothing)
    if created:
        send_category_created_event(mens_clothing)

    womens_clothing, created = Category.objects.get_or_create(name="Женская", parent=clothing)
    if created:
        send_category_created_event(womens_clothing)

    # Мужская одежда
    mens_shirts, created = Category.objects.get_or_create(
        name="Футболки и майки",
        parent=mens_clothing
    )
    if created:
        send_category_created_event(mens_shirts)

    mens_jeans, created = Category.objects.get_or_create(name="Джинсы", parent=mens_clothing)
    if created:
        send_category_created_event(mens_jeans)

    mens_pants, created = Category.objects.get_or_create(name="Брюки", parent=mens_clothing)
    if created:
        send_category_created_event(mens_pants)

    mens_polos, created = Category.objects.get_or_create(
        name="Футболки-поло",
        parent=mens_clothing
    )
    if created:
        send_category_created_event(mens_polos)

    mens_shirts_formal, created = Category.objects.get_or_create(
        name="Рубашки",
        parent=mens_clothing
    )
    if created:
        send_category_created_event(mens_shirts_formal)

    mens_shorts, created = Category.objects.get_or_create(name="Шорты", parent=mens_clothing)
    if created:
        send_category_created_event(mens_shorts)

    mens_underwear, created = Category.objects.get_or_create(name="Белье", parent=mens_clothing)
    if created:
        send_category_created_event(mens_underwear)

    # Женская одежда
    womens_skirts, created = Category.objects.get_or_create(name="Юбки", parent=womens_clothing)
    if created:
        send_category_created_event(womens_skirts)

    womens_blouses, created = Category.objects.get_or_create(
        name="Блузки и рубашки",
        parent=womens_clothing
    )
    if created:
        send_category_created_event(womens_blouses)

    womens_longsleeves, created = Category.objects.get_or_create(
        name="Лонгсливы",
        parent=womens_clothing
    )
    if created:
        send_category_created_event(womens_longsleeves)

    womens_tops, created = Category.objects.get_or_create(
        name="Футболки и топы",
        parent=womens_clothing
    )
    if created:
        send_category_created_event(womens_tops)

    womens_underwear, created = Category.objects.get_or_create(
        name="Белье",
        parent=womens_clothing
    )
    if created:
        send_category_created_event(womens_underwear)

    womens_dresses, created = Category.objects.get_or_create(
        name="Платья и сарафаны",
        parent=womens_clothing
    )
    if created:
        send_category_created_event(womens_dresses)

    womens_jeans, created = Category.objects.get_or_create(name="Джинсы", parent=womens_clothing)
    if created:
        send_category_created_event(womens_jeans)

    womens_shorts, created = Category.objects.get_or_create(name="Шорты", parent=womens_clothing)
    if created:
        send_category_created_event(womens_shorts)

    womens_pants, created = Category.objects.get_or_create(name="Брюки", parent=womens_clothing)
    if created:
        send_category_created_event(womens_pants)

    womens_tunics, created = Category.objects.get_or_create(name="Туники", parent=womens_clothing)
    if created:
        send_category_created_event(womens_tunics)

    womens_socks, created = Category.objects.get_or_create(
        name="Носки, колготки и чулки",
        parent=womens_clothing
    )
    if created:
        send_category_created_event(womens_socks)

    womens_jackets, created = Category.objects.get_or_create(
        name="Пиджаки, жилеты и жакеты",
        parent=womens_clothing
    )
    if created:
        send_category_created_event(womens_jackets)

    print("Категории созданы успешно!")
    return {
        'laptops': laptops,
        'ultrabooks': ultrabooks,
        'smartphones_sub': smartphones_sub,
        'televisions': televisions,
        'electric_kettles': electric_kettles,
        'blenders': blenders,
        'juicers': juicers,
        'microwaves': microwaves,
        'meat_grinders': meat_grinders,
        'coffee_machines': coffee_machines,
        'hair_dryers': hair_dryers,
        'refrigerators': refrigerators,
        'freezers': freezers,
        'washing_machines': washing_machines,
        'wine_cabinets': wine_cabinets,
        'vacuum_cleaners': vacuum_cleaners,
        'irons': irons,
        'air_conditioners': air_conditioners,
        'mens_shirts': mens_shirts,
        'mens_jeans': mens_jeans,
        'mens_pants': mens_pants,
        'mens_polos': mens_polos,
        'mens_shirts_formal': mens_shirts_formal,
        'mens_shorts': mens_shorts,
        'mens_underwear': mens_underwear,
        'womens_skirts': womens_skirts,
        'womens_blouses': womens_blouses,
        'womens_longsleeves': womens_longsleeves,
        'womens_tops': womens_tops,
        'womens_underwear': womens_underwear,
        'womens_dresses': womens_dresses,
        'womens_jeans': womens_jeans,
        'womens_shorts': womens_shorts,
        'womens_pants': womens_pants,
        'womens_tunics': womens_tunics,
        'womens_socks': womens_socks,
        'womens_jackets': womens_jackets,
    }


def create_option_types():
    """Создание типов опций"""

    option_types = [
        ("Цвет", "color"),
        ("Процессор", "processor"),
        ("Объем оперативной памяти (Гб)", "ram_gb"),
        ("Объем накопителя SSD", "ssd_storage"),
        ("Встроенная память", "internal_memory"),
        ("Оперативная память", "ram"),
        ("Диагональ экрана, дюймы", "screen_diagonal"),
        ("Объем, мл", "volume_ml"),
        ("Мощность устройства (Вт)", "device_power"),
        ("Общий объем холодильной камеры, л", "fridge_volume"),
        ("Общий объем камеры, л", "camera_volume"),
        ("Загрузка белья, кг", "laundry_load"),
        ("Количество бутылок, шт", "bottle_count"),
        ("Мощность всасывания, Вт", "suction_power"),
        ("Мощность устройства, Вт", "device_power_wt"),
        ("Площадь помещения, кв.м", "room_area"),
        ("Размер", "size"),
    ]

    created_types = {}
    for name, code in option_types:
        option_type, created = OptionType.objects.get_or_create(
            code=code,
            defaults={'name': name}
        )
        created_types[code] = option_type
        if created:
            send_option_type_created_event(option_type)
            print(f"Создан тип опции: {name}")

    return created_types


def create_option_values(option_types):
    """Создание значений опций (исключая цвета)"""

    # Значения опций на основе данных из файла (исключая цвета)
    option_values_data = {
        'processor': [
            'Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'Intel Core i9',
            'Intel Core Ultra 5', 'Intel Core Ultra 7', 'Intel Core Ultra 9',
            'AMD Ryzen 3', 'AMD Ryzen 5', 'AMD Ryzen 7', 'AMD Ryzen 9',
            'M1', 'M2', 'M3', 'M3 Pro', 'M3 Max'
        ],
        'ram_gb': ['8', '16', '32', '64'],
        'ssd_storage': ['256', '512', '1Т', '2048'],
        'internal_memory': ['64', '128', '256', '512', '1Т'],
        'ram': ['4', '6', '8', '12', '16'],
        'screen_diagonal': ['32', '42', '50', '55', '65', '75', '85'],
        'volume_ml': ['1200', '1700', '2000', '600', '1000', '1500', '1800'],
        'device_power': [
            '600', '800', '1000', '1200', '1800',  # для блендеров и др.
            '700', '900',  # дополнительные значения
            '1500', '2000'  # для более мощных устройств
        ],
        'fridge_volume': ['180', '200', '250', '280', '300', '350', '400'],
        'camera_volume': ['100', '150', '180', '200', '250', '280', '300'],
        'laundry_load': ['6', '7', '8', '10', '12'],
        'bottle_count': ['6', '7', '8', '10', '12', '20', '30'],
        'suction_power': ['800', '900', '1000', '1200', '1500', '1800', '2000'],
        'device_power_wt': ['800', '1000', '1200', '1500', '1800', '2000', '2200'],
        'room_area': ['15', '20', '24', '25', '26', '35', '40', '50', '54', '70'],
        'size': ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL']
    }

    created_values = {}
    for option_code, values in option_values_data.items():
        if option_code in option_types:
            option_type = option_types[option_code]
            created_values[option_code] = []

            for value in values:
                option_value, created = OptionValue.objects.get_or_create(
                    option_type=option_type,
                    value=value
                )
                created_values[option_code].append(option_value)
                if created:
                    send_option_value_created_event(option_value)
                    print(f"Создано значение опции: {option_type.name} - {value}")

    return created_values


def create_option_requirements(categories, option_types):
    """Создание связей категорий с опциями"""

    # Маппинг категорий к их главным опциям
    category_options = {
        # Электроника
        categories['laptops']: [
            (option_types['color'], True),  # Цвет - главная опция
            (option_types['processor'], False),
            (option_types['ram_gb'], False),
            (option_types['ssd_storage'], False),
        ],
        categories['ultrabooks']: [
            (option_types['color'], True),
            (option_types['processor'], False),
            (option_types['ram_gb'], False),
            (option_types['ssd_storage'], False),
        ],
        categories['smartphones_sub']: [
            (option_types['color'], True),
            (option_types['internal_memory'], False),
            (option_types['ram'], False),
        ],
        categories['televisions']: [
            (option_types['color'], True),
            (option_types['screen_diagonal'], False),
        ],

        # Кухонная техника
        categories['electric_kettles']: [
            (option_types['color'], True),
            (option_types['volume_ml'], False),
        ],
        categories['blenders']: [
            (option_types['color'], True),
            (option_types['device_power'], False),
        ],
        categories['juicers']: [
            (option_types['color'], True),
            (option_types['device_power'], False),
        ],
        categories['microwaves']: [
            (option_types['color'], True),
            (option_types['device_power'], False),
        ],
        categories['meat_grinders']: [
            (option_types['color'], True),
            (option_types['device_power'], False),
        ],
        categories['coffee_machines']: [
            (option_types['color'], True),
            (option_types['volume_ml'], False),
        ],
        categories['hair_dryers']: [
            (option_types['color'], True),
            (option_types['device_power'], False),
        ],

        # Крупная бытовая техника
        categories['refrigerators']: [
            (option_types['color'], True),
            (option_types['fridge_volume'], False),
        ],
        categories['freezers']: [
            (option_types['color'], True),
            (option_types['camera_volume'], False),
        ],
        categories['washing_machines']: [
            (option_types['color'], True),
            (option_types['laundry_load'], False),
        ],
        categories['wine_cabinets']: [
            (option_types['color'], True),
            (option_types['bottle_count'], False),
        ],
        categories['vacuum_cleaners']: [
            (option_types['color'], True),
            (option_types['suction_power'], False),
        ],
        categories['irons']: [
            (option_types['color'], True),
            (option_types['device_power_wt'], False),
        ],
        categories['air_conditioners']: [
            (option_types['color'], True),
            (option_types['room_area'], False),
        ],

        # Одежда - все категории одежды имеют цвет и размер
    }

    # Добавляем все категории одежды
    clothing_categories = [
        'mens_shirts', 'mens_jeans', 'mens_pants', 'mens_polos',
        'mens_shirts_formal', 'mens_shorts', 'mens_underwear',
        'womens_skirts', 'womens_blouses', 'womens_longsleeves',
        'womens_tops', 'womens_underwear', 'womens_dresses',
        'womens_jeans', 'womens_shorts', 'womens_pants',
        'womens_tunics', 'womens_socks', 'womens_jackets'
    ]

    for cat_name in clothing_categories:
        if cat_name in categories:
            category_options[categories[cat_name]] = [
                (option_types['color'], True),  # Цвет - главная опция
                (option_types['size'], False),  # Размер - дополнительная опция
            ]

    # Создание CategoryOptionRequirement записей
    for category, options in category_options.items():
        for i, (option_type, is_main) in enumerate(options):
            requirement, is_created = CategoryOptionRequirement.objects.get_or_create(
                category=category,
                option_type=option_type,
                defaults={
                    'is_main': is_main,
                    'is_required': True,
                    'sort_order': i
                }
            )
            if is_created:
                send_category_option_requirement_created_event(requirement)
            print(f"Создана связь: {category.name} - {option_type.name} (main: {is_main})")
