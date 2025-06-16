#!/usr/bin/env python
import os
import sys
import django
from django.db import transaction

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from tanda_backend.products.models.category import Category
from tanda_backend.products.models.options import OptionType, OptionValue
from tanda_backend.products.models.product import Product, ProductVariant, VariantOption


@transaction.atomic
def create_sample_data():
    # Создаем категории и подкатегории
    print("Создание категорий...")
    electronics = Category.objects.create(name="Электроника")
    smartphones = Category.objects.create(name="Смартфоны", parent=electronics)
    laptops = Category.objects.create(name="Ноутбуки", parent=electronics)
    tablets = Category.objects.create(name="Планшеты", parent=electronics)
    headphones = Category.objects.create(name="Наушники", parent=electronics)
    accessories = Category.objects.create(name="Аксессуары", parent=electronics)

    clothing = Category.objects.create(name="Одежда")
    dresses = Category.objects.create(name="Платья", parent=clothing)
    shirts = Category.objects.create(name="Рубашки", parent=clothing)
    tshirts = Category.objects.create(name="Футболки", parent=clothing)
    jeans = Category.objects.create(name="Джинсы", parent=clothing)
    jackets = Category.objects.create(name="Куртки", parent=clothing)
    shoes = Category.objects.create(name="Обувь", parent=clothing)

    furniture = Category.objects.create(name="Мебель")
    tables = Category.objects.create(name="Столы", parent=furniture)
    chairs = Category.objects.create(name="Стулья", parent=furniture)
    sofas = Category.objects.create(name="Диваны", parent=furniture)
    beds = Category.objects.create(name="Кровати", parent=furniture)

    sports = Category.objects.create(name="Спорттовары")
    fitness = Category.objects.create(name="Фитнес", parent=sports)
    outdoor = Category.objects.create(name="Туризм", parent=sports)

    # Создаем типы опций
    print("Создание типов опций...")
    color_type = OptionType.objects.create(name="Цвет", code="color")
    memory_type = OptionType.objects.create(name="Объем памяти", code="memory")
    size_type = OptionType.objects.create(name="Размер", code="size")
    material_type = OptionType.objects.create(name="Материал", code="material")
    screen_type = OptionType.objects.create(name="Размер экрана", code="screen")
    processor_type = OptionType.objects.create(name="Процессор", code="processor")
    style_type = OptionType.objects.create(name="Стиль", code="style")
    weight_type = OptionType.objects.create(name="Вес", code="weight")

    # Создаем значения опций
    print("Создание значений опций...")
    # Цвета
    white_color = OptionValue.objects.create(option_type=color_type, value="Белый", meta_data={"hex": "#FFFFFF"})
    black_color = OptionValue.objects.create(option_type=color_type, value="Черный", meta_data={"hex": "#000000"})
    red_color = OptionValue.objects.create(option_type=color_type, value="Красный", meta_data={"hex": "#FF0000"})
    blue_color = OptionValue.objects.create(option_type=color_type, value="Синий", meta_data={"hex": "#0000FF"})
    green_color = OptionValue.objects.create(option_type=color_type, value="Зеленый", meta_data={"hex": "#00FF00"})
    yellow_color = OptionValue.objects.create(option_type=color_type, value="Желтый", meta_data={"hex": "#FFFF00"})
    purple_color = OptionValue.objects.create(option_type=color_type, value="Фиолетовый", meta_data={"hex": "#800080"})
    gray_color = OptionValue.objects.create(option_type=color_type, value="Серый", meta_data={"hex": "#808080"})

    # Объемы памяти
    memory_64 = OptionValue.objects.create(option_type=memory_type, value="64 ГБ")
    memory_128 = OptionValue.objects.create(option_type=memory_type, value="128 ГБ")
    memory_256 = OptionValue.objects.create(option_type=memory_type, value="256 ГБ")
    memory_512 = OptionValue.objects.create(option_type=memory_type, value="512 ГБ")
    memory_1tb = OptionValue.objects.create(option_type=memory_type, value="1 ТБ")

    # Размеры
    size_xs = OptionValue.objects.create(option_type=size_type, value="XS")
    size_s = OptionValue.objects.create(option_type=size_type, value="S")
    size_m = OptionValue.objects.create(option_type=size_type, value="M")
    size_l = OptionValue.objects.create(option_type=size_type, value="L")
    size_xl = OptionValue.objects.create(option_type=size_type, value="XL")
    size_xxl = OptionValue.objects.create(option_type=size_type, value="XXL")

    # Размеры обуви
    size_38 = OptionValue.objects.create(option_type=size_type, value="38")
    size_39 = OptionValue.objects.create(option_type=size_type, value="39")
    size_40 = OptionValue.objects.create(option_type=size_type, value="40")
    size_41 = OptionValue.objects.create(option_type=size_type, value="41")
    size_42 = OptionValue.objects.create(option_type=size_type, value="42")
    size_43 = OptionValue.objects.create(option_type=size_type, value="43")

    # Материалы
    wood_material = OptionValue.objects.create(option_type=material_type, value="Дерево")
    glass_material = OptionValue.objects.create(option_type=material_type, value="Стекло")
    metal_material = OptionValue.objects.create(option_type=material_type, value="Металл")
    leather_material = OptionValue.objects.create(option_type=material_type, value="Кожа")
    cotton_material = OptionValue.objects.create(option_type=material_type, value="Хлопок")
    wool_material = OptionValue.objects.create(option_type=material_type, value="Шерсть")
    plastic_material = OptionValue.objects.create(option_type=material_type, value="Пластик")
    fabric_material = OptionValue.objects.create(option_type=material_type, value="Ткань")

    # Размеры экрана
    screen_13 = OptionValue.objects.create(option_type=screen_type, value="13 дюймов")
    screen_14 = OptionValue.objects.create(option_type=screen_type, value="14 дюймов")
    screen_15 = OptionValue.objects.create(option_type=screen_type, value="15.6 дюймов")
    screen_17 = OptionValue.objects.create(option_type=screen_type, value="17 дюймов")

    # Процессоры
    intel_i5 = OptionValue.objects.create(option_type=processor_type, value="Intel Core i5")
    intel_i7 = OptionValue.objects.create(option_type=processor_type, value="Intel Core i7")
    intel_i9 = OptionValue.objects.create(option_type=processor_type, value="Intel Core i9")
    amd_ryzen5 = OptionValue.objects.create(option_type=processor_type, value="AMD Ryzen 5")
    amd_ryzen7 = OptionValue.objects.create(option_type=processor_type, value="AMD Ryzen 7")

    # Стили
    casual_style = OptionValue.objects.create(option_type=style_type, value="Повседневный")
    formal_style = OptionValue.objects.create(option_type=style_type, value="Деловой")
    sport_style = OptionValue.objects.create(option_type=style_type, value="Спортивный")

    # Вес
    weight_light = OptionValue.objects.create(option_type=weight_type, value="Легкий")
    weight_medium = OptionValue.objects.create(option_type=weight_type, value="Средний")
    weight_heavy = OptionValue.objects.create(option_type=weight_type, value="Тяжелый")

    # Создаем продукты и их варианты
    print("Создание продуктов и вариантов...")

    # 1. iPhone с разными объемами памяти и цветами
    iphone = Product.objects.create(
        title="iPhone 15 Pro",
        description="Новейший смартфон от Apple с передовыми технологиями",
        images=["iphone-15-6c.jpg"],
        slug="iphone-15-pro",
        category=smartphones,
        group_by_option_id=memory_type,
        stock_id="IPHONE15PRO",
        # provider_id="APPLE",
        selling_price=6000,
    )

    # Варианты iPhone
    # Создаем все комбинации: 3 цвета x 3 объема памяти = 9 вариантов
    variants_data = [
        {"color": white_color, "memory": memory_64, "stock_id": "IPHONE15PRO-WHITE-64", "qty": 10},
        {"color": white_color, "memory": memory_256, "stock_id": "IPHONE15PRO-WHITE-256", "qty": 15},
        {"color": white_color, "memory": memory_512, "stock_id": "IPHONE15PRO-WHITE-512", "qty": 5},
        {"color": black_color, "memory": memory_64, "stock_id": "IPHONE15PRO-BLACK-64", "qty": 8},
        {"color": black_color, "memory": memory_256, "stock_id": "IPHONE15PRO-BLACK-256", "qty": 12},
        {"color": black_color, "memory": memory_512, "stock_id": "IPHONE15PRO-BLACK-512", "qty": 6},
        {"color": red_color, "memory": memory_64, "stock_id": "IPHONE15PRO-RED-64", "qty": 7},
        {"color": red_color, "memory": memory_256, "stock_id": "IPHONE15PRO-RED-256", "qty": 9},
        {"color": red_color, "memory": memory_512, "stock_id": "IPHONE15PRO-RED-512", "qty": 4},
    ]

    for variant_data in variants_data:
        variant = ProductVariant.objects.create(
            product=iphone,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["memory"]
        )

    # 2. Платье с разными размерами и цветами
    dress = Product.objects.create(
        title="Элегантное платье",
        description="Стильное платье для особых случаев",
        images=["DSC07520.jpg"],
        slug="elegant-dress",
        category=dresses,
        group_by_option_id=color_type,  # Группировка по цвету
        stock_id="ELEGANTDRESS",
        # provider_id="FASHIONBRAND",
        selling_price=3999,
    )

    # Варианты платья
    # Создаем все комбинации: 3 цвета x 3 размера = 9 вариантов
    dress_variants_data = [
        {"color": white_color, "size": size_xs, "stock_id": "ELEGANTDRESS-WHITE-XS", "qty": 5},
        {"color": white_color, "size": size_m, "stock_id": "ELEGANTDRESS-WHITE-M", "qty": 8},
        {"color": white_color, "size": size_l, "stock_id": "ELEGANTDRESS-WHITE-L", "qty": 6},
        {"color": black_color, "size": size_xs, "stock_id": "ELEGANTDRESS-BLACK-XS", "qty": 4},
        {"color": black_color, "size": size_m, "stock_id": "ELEGANTDRESS-BLACK-M", "qty": 10},
        {"color": black_color, "size": size_l, "stock_id": "ELEGANTDRESS-BLACK-L", "qty": 7},
        {"color": blue_color, "size": size_xs, "stock_id": "ELEGANTDRESS-BLUE-XS", "qty": 3},
        {"color": blue_color, "size": size_m, "stock_id": "ELEGANTDRESS-BLUE-M", "qty": 9},
        {"color": blue_color, "size": size_l, "stock_id": "ELEGANTDRESS-BLUE-L", "qty": 5},
    ]

    for variant_data in dress_variants_data:
        variant = ProductVariant.objects.create(
            product=dress,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["size"]
        )

    # 3. Стол (дополнительный товар)
    table = Product.objects.create(
        title="Обеденный стол",
        description="Прочный и стильный обеденный стол для вашего дома",
        images=["images%20(1).jpeg"],
        slug="dining-table",
        category=tables,
        group_by_option_id=material_type,
        stock_id="DININGTABLE",
        # provider_id="FURNITUREBRAND",
        selling_price=6100,
    )

    # Варианты стола
    # Создаем комбинации: 2 материала x 2 цвета = 4 варианта
    table_variants_data = [
        {"material": wood_material, "color": black_color, "stock_id": "DININGTABLE-WOOD-BLACK", "qty": 3},
        {"material": wood_material, "color": white_color, "stock_id": "DININGTABLE-WOOD-WHITE", "qty": 2},
        {"material": glass_material, "color": black_color, "stock_id": "DININGTABLE-GLASS-BLACK", "qty": 4},
        {"material": glass_material, "color": white_color, "stock_id": "DININGTABLE-GLASS-WHITE", "qty": 5},
    ]

    for variant_data in table_variants_data:
        variant = ProductVariant.objects.create(
            product=table,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["material"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

    # 4. Ноутбук MacBook Pro
    macbook = Product.objects.create(
        title="MacBook Pro 16",
        description="Мощный ноутбук для профессионалов с процессором M2 Pro",
        images=["macbook_pro.jpeg"],
        slug="macbook-pro-16",
        category=laptops,
        group_by_option_id=processor_type,
        stock_id="MACBOOKPRO16",
        # provider_id="APPLE",
        selling_price=199000,
    )

    # Варианты MacBook Pro
    macbook_variants_data = [
        {"processor": intel_i7, "memory": memory_512, "color": gray_color, "stock_id": "MACBOOKPRO16-I7-512-GRAY", "qty": 5},
        {"processor": intel_i7, "memory": memory_1tb, "color": gray_color, "stock_id": "MACBOOKPRO16-I7-1TB-GRAY", "qty": 3},
        {"processor": intel_i9, "memory": memory_512, "color": gray_color, "stock_id": "MACBOOKPRO16-I9-512-GRAY", "qty": 4},
        {"processor": intel_i9, "memory": memory_1tb, "color": gray_color, "stock_id": "MACBOOKPRO16-I9-1TB-GRAY", "qty": 2},
        {"processor": intel_i7, "memory": memory_512, "color": black_color, "stock_id": "MACBOOKPRO16-I7-512-BLACK", "qty": 6},
        {"processor": intel_i9, "memory": memory_1tb, "color": black_color, "stock_id": "MACBOOKPRO16-I9-1TB-BLACK", "qty": 3},
    ]

    for variant_data in macbook_variants_data:
        variant = ProductVariant.objects.create(
            product=macbook,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["processor"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["memory"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

    # 5. Футболка
    tshirt = Product.objects.create(
        title="Базовая футболка",
        description="Комфортная хлопковая футболка на каждый день",
        images=["base_shirt.webp"],
        slug="basic-tshirt",
        category=tshirts,
        group_by_option_id=color_type,  # Группировка по цвету
        stock_id="BASICTSHIRT",
        # provider_id="CASUALBRAND",
        selling_price=1200,
    )

    # Варианты футболки
    tshirt_variants_data = [
        {"color": white_color, "size": size_s, "material": cotton_material, "stock_id": "BASICTSHIRT-WHITE-S", "qty": 15},
        {"color": white_color, "size": size_m, "material": cotton_material, "stock_id": "BASICTSHIRT-WHITE-M", "qty": 20},
        {"color": white_color, "size": size_l, "material": cotton_material, "stock_id": "BASICTSHIRT-WHITE-L", "qty": 18},
        {"color": black_color, "size": size_s, "material": cotton_material, "stock_id": "BASICTSHIRT-BLACK-S", "qty": 12},
        {"color": black_color, "size": size_m, "material": cotton_material, "stock_id": "BASICTSHIRT-BLACK-M", "qty": 25},
        {"color": black_color, "size": size_l, "material": cotton_material, "stock_id": "BASICTSHIRT-BLACK-L", "qty": 15},
        {"color": red_color, "size": size_s, "material": cotton_material, "stock_id": "BASICTSHIRT-RED-S", "qty": 8},
        {"color": red_color, "size": size_m, "material": cotton_material, "stock_id": "BASICTSHIRT-RED-M", "qty": 10},
        {"color": red_color, "size": size_l, "material": cotton_material, "stock_id": "BASICTSHIRT-RED-L", "qty": 7},
        {"color": blue_color, "size": size_s, "material": cotton_material, "stock_id": "BASICTSHIRT-BLUE-S", "qty": 9},
        {"color": blue_color, "size": size_m, "material": cotton_material, "stock_id": "BASICTSHIRT-BLUE-M", "qty": 12},
        {"color": blue_color, "size": size_l, "material": cotton_material, "stock_id": "BASICTSHIRT-BLUE-L", "qty": 8},
    ]

    for variant_data in tshirt_variants_data:
        variant = ProductVariant.objects.create(
            product=tshirt,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["size"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["material"]
        )

    # 6. Джинсы
    jeans_product = Product.objects.create(
        title="Классические джинсы",
        description="Удобные джинсы прямого кроя из качественного денима",
        images=["djins.webp"],
        slug="classic-jeans",
        category=jeans,
        group_by_option_id=color_type,  # Группировка по цвету
        stock_id="CLASSICJEANS",
        # provider_id="DENIMBRAND",
        selling_price=3400,
    )

    # Варианты джинсов
    jeans_variants_data = [
        {"color": blue_color, "size": size_s, "style": casual_style, "stock_id": "CLASSICJEANS-BLUE-S", "qty": 10},
        {"color": blue_color, "size": size_m, "style": casual_style, "stock_id": "CLASSICJEANS-BLUE-M", "qty": 15},
        {"color": blue_color, "size": size_l, "style": casual_style, "stock_id": "CLASSICJEANS-BLUE-L", "qty": 12},
        {"color": black_color, "size": size_s, "style": casual_style, "stock_id": "CLASSICJEANS-BLACK-S", "qty": 8},
        {"color": black_color, "size": size_m, "style": casual_style, "stock_id": "CLASSICJEANS-BLACK-M", "qty": 14},
        {"color": black_color, "size": size_l, "style": casual_style, "stock_id": "CLASSICJEANS-BLACK-L", "qty": 10},
        {"color": gray_color, "size": size_s, "style": casual_style, "stock_id": "CLASSICJEANS-GRAY-S", "qty": 7},
        {"color": gray_color, "size": size_m, "style": casual_style, "stock_id": "CLASSICJEANS-GRAY-M", "qty": 12},
        {"color": gray_color, "size": size_l, "style": casual_style, "stock_id": "CLASSICJEANS-GRAY-L", "qty": 9},
    ]

    for variant_data in jeans_variants_data:
        variant = ProductVariant.objects.create(
            product=jeans_product,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["size"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["style"]
        )

    # 7. Куртка
    jacket = Product.objects.create(
        title="Зимняя куртка",
        description="Теплая куртка для холодной погоды",
        images=["shirt_2.webp"],
        slug="winter-jacket",
        category=jackets,
        group_by_option_id=color_type,  # Группировка по цвету
        stock_id="WINTERJACKET",
        # provider_id="OUTERWEAR",
        selling_price=5000,
    )

    # Варианты куртки
    jacket_variants_data = [
        {"color": black_color, "size": size_m, "material": leather_material, "stock_id": "WINTERJACKET-BLACK-M", "qty": 7},
        {"color": black_color, "size": size_l, "material": leather_material, "stock_id": "WINTERJACKET-BLACK-L", "qty": 9},
        {"color": black_color, "size": size_xl, "material": leather_material, "stock_id": "WINTERJACKET-BLACK-XL", "qty": 6},
        {"color": blue_color, "size": size_m, "material": leather_material, "stock_id": "WINTERJACKET-BLUE-M", "qty": 5},
        {"color": blue_color, "size": size_l, "material": leather_material, "stock_id": "WINTERJACKET-BLUE-L", "qty": 8},
        {"color": blue_color, "size": size_xl, "material": leather_material, "stock_id": "WINTERJACKET-BLUE-XL", "qty": 4},
        {"color": red_color, "size": size_m, "material": leather_material, "stock_id": "WINTERJACKET-RED-M", "qty": 3},
        {"color": red_color, "size": size_l, "material": leather_material, "stock_id": "WINTERJACKET-RED-L", "qty": 6},
        {"color": red_color, "size": size_xl, "material": leather_material, "stock_id": "WINTERJACKET-RED-XL", "qty": 2},
    ]

    for variant_data in jacket_variants_data:
        variant = ProductVariant.objects.create(
            product=jacket,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["size"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["material"]
        )

    # 8. Кроссовки
    sneakers = Product.objects.create(
        title="Спортивные кроссовки",
        description="Легкие и удобные кроссовки для бега и тренировок",
        images=["obuv.avif"],
        slug="sport-sneakers",
        category=shoes,
        group_by_option_id=color_type,  # Группировка по цвету
        stock_id="SPORTSNEAKERS",
        # provider_id="SPORTBRAND",
        selling_price=3499,
    )

    # Варианты кроссовок
    sneakers_variants_data = [
        {"color": white_color, "size": size_40, "style": sport_style, "stock_id": "SPORTSNEAKERS-WHITE-40", "qty": 8},
        {"color": white_color, "size": size_41, "style": sport_style, "stock_id": "SPORTSNEAKERS-WHITE-41", "qty": 10},
        {"color": white_color, "size": size_42, "style": sport_style, "stock_id": "SPORTSNEAKERS-WHITE-42", "qty": 12},
        {"color": black_color, "size": size_40, "style": sport_style, "stock_id": "SPORTSNEAKERS-BLACK-40", "qty": 7},
        {"color": black_color, "size": size_41, "style": sport_style, "stock_id": "SPORTSNEAKERS-BLACK-41", "qty": 9},
        {"color": black_color, "size": size_42, "style": sport_style, "stock_id": "SPORTSNEAKERS-BLACK-42", "qty": 11},
        {"color": red_color, "size": size_40, "style": sport_style, "stock_id": "SPORTSNEAKERS-RED-40", "qty": 5},
        {"color": red_color, "size": size_41, "style": sport_style, "stock_id": "SPORTSNEAKERS-RED-41", "qty": 7},
        {"color": red_color, "size": size_42, "style": sport_style, "stock_id": "SPORTSNEAKERS-RED-42", "qty": 9},
    ]

    for variant_data in sneakers_variants_data:
        variant = ProductVariant.objects.create(
            product=sneakers,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["size"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["style"]
        )

    # 9. Планшет iPad Pro
    ipad = Product.objects.create(
        title="iPad Pro",
        description="Мощный планшет для работы и развлечений",
        images=["ipad.webp"],
        slug="ipad-pro",
        category=tablets,
        group_by_option_id=memory_type,
        stock_id="IPADPRO",
        # provider_id="APPLE",
        selling_price=5200,
    )

    # Варианты iPad Pro
    ipad_variants_data = [
        {"memory": memory_128, "color": gray_color, "stock_id": "IPADPRO-128-GRAY", "qty": 10},
        {"memory": memory_256, "color": gray_color, "stock_id": "IPADPRO-256-GRAY", "qty": 8},
        {"memory": memory_512, "color": gray_color, "stock_id": "IPADPRO-512-GRAY", "qty": 6},
        {"memory": memory_128, "color": black_color, "stock_id": "IPADPRO-128-BLACK", "qty": 9},
        {"memory": memory_256, "color": black_color, "stock_id": "IPADPRO-256-BLACK", "qty": 7},
        {"memory": memory_512, "color": black_color, "stock_id": "IPADPRO-512-BLACK", "qty": 5},
    ]

    for variant_data in ipad_variants_data:
        variant = ProductVariant.objects.create(
            product=ipad,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["memory"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

    # 10. Наушники
    headphones_product = Product.objects.create(
        title="Беспроводные наушники",
        description="Качественные наушники с шумоподавлением",
        images=["realme.jpeg"],
        slug="wireless-headphones",
        category=headphones,
        group_by_option_id=color_type,
        stock_id="WIRELESSHEADPHONES",
        # provider_id="AUDIOBRAND",
        selling_price=2100,
    )

    # Варианты наушников
    headphones_variants_data = [
        {"color": black_color, "material": plastic_material, "stock_id": "WIRELESSHEADPHONES-BLACK", "qty": 15},
        {"color": white_color, "material": plastic_material, "stock_id": "WIRELESSHEADPHONES-WHITE", "qty": 12},
        {"color": red_color, "material": plastic_material, "stock_id": "WIRELESSHEADPHONES-RED", "qty": 8},
        {"color": blue_color, "material": plastic_material, "stock_id": "WIRELESSHEADPHONES-BLUE", "qty": 10},
    ]

    for variant_data in headphones_variants_data:
        variant = ProductVariant.objects.create(
            product=headphones_product,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["material"]
        )

    # 11. Рубашка
    shirt = Product.objects.create(
        title="Деловая рубашка",
        description="Элегантная рубашка для офиса и деловых встреч",
        images=["delovaya-rubashka-t-m-lewin.jpg"],
        slug="formal-shirt",
        category=shirts,
        group_by_option_id=color_type,  # Группировка по цвету
        stock_id="FORMALSHIRT",
        # provider_id="FORMALBRAND",
        selling_price=2500,
    )

    # Варианты рубашки
    shirt_variants_data = [
        {"color": white_color, "size": size_s, "style": formal_style, "stock_id": "FORMALSHIRT-WHITE-S", "qty": 12},
        {"color": white_color, "size": size_m, "style": formal_style, "stock_id": "FORMALSHIRT-WHITE-M", "qty": 15},
        {"color": white_color, "size": size_l, "style": formal_style, "stock_id": "FORMALSHIRT-WHITE-L", "qty": 10},
        {"color": blue_color, "size": size_s, "style": formal_style, "stock_id": "FORMALSHIRT-BLUE-S", "qty": 8},
        {"color": blue_color, "size": size_m, "style": formal_style, "stock_id": "FORMALSHIRT-BLUE-M", "qty": 14},
        {"color": blue_color, "size": size_l, "style": formal_style, "stock_id": "FORMALSHIRT-BLUE-L", "qty": 9},
        {"color": black_color, "size": size_s, "style": formal_style, "stock_id": "FORMALSHIRT-BLACK-S", "qty": 7},
        {"color": black_color, "size": size_m, "style": formal_style, "stock_id": "FORMALSHIRT-BLACK-M", "qty": 11},
        {"color": black_color, "size": size_l, "style": formal_style, "stock_id": "FORMALSHIRT-BLACK-L", "qty": 6},
    ]

    for variant_data in shirt_variants_data:
        variant = ProductVariant.objects.create(
            product=shirt,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["size"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["style"]
        )

    # 12. Стул
    chair = Product.objects.create(
        title="Офисный стул",
        description="Эргономичный стул для дома и офиса",
        images=["stul2.webp"],
        slug="office-chair",
        category=chairs,
        group_by_option_id=color_type,
        stock_id="OFFICECHAIR",
        # provider_id="FURNITUREBRAND",
        selling_price=3000,
    )

    # Варианты стула
    chair_variants_data = [
        {"color": black_color, "material": leather_material, "stock_id": "OFFICECHAIR-BLACK-LEATHER", "qty": 8},
        {"color": black_color, "material": fabric_material, "stock_id": "OFFICECHAIR-BLACK-FABRIC", "qty": 10},
        {"color": gray_color, "material": leather_material, "stock_id": "OFFICECHAIR-GRAY-LEATHER", "qty": 6},
        {"color": gray_color, "material": fabric_material, "stock_id": "OFFICECHAIR-GRAY-FABRIC", "qty": 9},
        {"color": white_color, "material": leather_material, "stock_id": "OFFICECHAIR-WHITE-LEATHER", "qty": 5},
        {"color": white_color, "material": fabric_material, "stock_id": "OFFICECHAIR-WHITE-FABRIC", "qty": 7},
    ]

    for variant_data in chair_variants_data:
        variant = ProductVariant.objects.create(
            product=chair,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["material"]
        )

    # 13. Диван
    sofa = Product.objects.create(
        title="Угловой диван",
        description="Комфортный угловой диван для гостиной",
        images=["divan.jpg"],
        slug="corner-sofa",
        category=sofas,
        group_by_option_id=color_type,
        stock_id="CORNERSOFA",
        # provider_id="FURNITUREBRAND",
        selling_price=5000,
    )

    # Варианты дивана
    sofa_variants_data = [
        {"color": gray_color, "material": fabric_material, "stock_id": "CORNERSOFA-GRAY-FABRIC", "qty": 4},
        {"color": blue_color, "material": fabric_material, "stock_id": "CORNERSOFA-BLUE-FABRIC", "qty": 3},
        {"color": black_color, "material": leather_material, "stock_id": "CORNERSOFA-BLACK-LEATHER", "qty": 2},
        {"color": white_color, "material": fabric_material, "stock_id": "CORNERSOFA-WHITE-FABRIC", "qty": 5},
    ]

    for variant_data in sofa_variants_data:
        variant = ProductVariant.objects.create(
            product=sofa,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["material"]
        )

    # 14. Кровать
    bed = Product.objects.create(
        title="divan15.webp",
        description="Комфортная кровать с мягким изголовьем",
        images=["bed_front.jpg", "bed_side.jpg"],
        slug="double-bed",
        category=beds,
        group_by_option_id=material_type,
        stock_id="DOUBLEBED",
        # provider_id="FURNITUREBRAND",
        selling_price=8000,
    )

    # Варианты кровати
    bed_variants_data = [
        {"material": wood_material, "color": black_color, "stock_id": "DOUBLEBED-WOOD-BLACK", "qty": 3},
        {"material": wood_material, "color": white_color, "stock_id": "DOUBLEBED-WOOD-WHITE", "qty": 4},
        {"material": metal_material, "color": black_color, "stock_id": "DOUBLEBED-METAL-BLACK", "qty": 2},
        {"material": metal_material, "color": white_color, "stock_id": "DOUBLEBED-METAL-WHITE", "qty": 3},
    ]

    for variant_data in bed_variants_data:
        variant = ProductVariant.objects.create(
            product=bed,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["material"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

    # 15. Фитнес-трекер
    fitness_tracker = Product.objects.create(
        title="Фитнес-трекер",
        description="Умный фитнес-трекер для мониторинга активности и здоровья",
        images=["tracker.webp"],
        slug="fitness-tracker",
        category=fitness,
        group_by_option_id=color_type,
        stock_id="FITNESSTRACKER",
        # provider_id="SPORTBRAND",
        selling_price=3000,
    )

    # Варианты фитнес-трекера
    tracker_variants_data = [
        {"color": black_color, "stock_id": "FITNESSTRACKER-BLACK", "qty": 15},
        {"color": red_color, "stock_id": "FITNESSTRACKER-RED", "qty": 12},
        {"color": blue_color, "stock_id": "FITNESSTRACKER-BLUE", "qty": 10},
        {"color": green_color, "stock_id": "FITNESSTRACKER-GREEN", "qty": 8},
    ]

    for variant_data in tracker_variants_data:
        variant = ProductVariant.objects.create(
            product=fitness_tracker,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

    # 16. Палатка
    tent = Product.objects.create(
        title="Туристическая палатка",
        description="Легкая и прочная палатка для походов и кемпинга",
        images=["palatka.webp"],
        slug="camping-tent",
        category=outdoor,
        group_by_option_id=size_type,
        stock_id="CAMPINGTENT",
        # provider_id="OUTDOORBRAND",
        selling_price=5000,
    )

    # Варианты палатки
    tent_variants_data = [
        {"size": size_s, "color": green_color, "stock_id": "CAMPINGTENT-S-GREEN", "qty": 6},  # Двухместная
        {"size": size_m, "color": green_color, "stock_id": "CAMPINGTENT-M-GREEN", "qty": 8},  # Трехместная
        {"size": size_l, "color": green_color, "stock_id": "CAMPINGTENT-L-GREEN", "qty": 4},  # Четырехместная
        {"size": size_s, "color": blue_color, "stock_id": "CAMPINGTENT-S-BLUE", "qty": 5},
        {"size": size_m, "color": blue_color, "stock_id": "CAMPINGTENT-M-BLUE", "qty": 7},
        {"size": size_l, "color": blue_color, "stock_id": "CAMPINGTENT-L-BLUE", "qty": 3},
    ]

    for variant_data in tent_variants_data:
        variant = ProductVariant.objects.create(
            product=tent,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["size"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

    # 17. Рюкзак
    backpack = Product.objects.create(
        title="Туристический рюкзак",
        description="Вместительный и прочный рюкзак для путешествий",
        images=["sumka.webp"],
        slug="hiking-backpack",
        category=outdoor,
        group_by_option_id=color_type,  # Группировка по цвету
        stock_id="HIKINGBACKPACK",
        # provider_id="OUTDOORBRAND",
        selling_price=4000,
    )

    # Варианты рюкзака
    backpack_variants_data = [
        {"color": black_color, "size": size_m, "stock_id": "HIKINGBACKPACK-BLACK-M", "qty": 10},  # 40л
        {"color": black_color, "size": size_l, "stock_id": "HIKINGBACKPACK-BLACK-L", "qty": 8},   # 60л
        {"color": blue_color, "size": size_m, "stock_id": "HIKINGBACKPACK-BLUE-M", "qty": 9},
        {"color": blue_color, "size": size_l, "stock_id": "HIKINGBACKPACK-BLUE-L", "qty": 7},
        {"color": red_color, "size": size_m, "stock_id": "HIKINGBACKPACK-RED-M", "qty": 6},
        {"color": red_color, "size": size_l, "stock_id": "HIKINGBACKPACK-RED-L", "qty": 5},
    ]

    for variant_data in backpack_variants_data:
        variant = ProductVariant.objects.create(
            product=backpack,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["size"]
        )

    # 18. Спортивный костюм
    sportsuit = Product.objects.create(
        title="Спортивный костюм",
        description="Удобный костюм для тренировок и бега",
        images=["IMG_2830_11zon.webp"],
        slug="sport-suit",
        category=fitness,
        group_by_option_id=color_type,  # Группировка по цвету
        stock_id="SPORTSUIT",
        # provider_id="SPORTBRAND",
        selling_price=3000,
    )

    # Варианты спортивного костюма
    sportsuit_variants_data = [
        {"color": black_color, "size": size_s, "stock_id": "SPORTSUIT-BLACK-S", "qty": 8},
        {"color": black_color, "size": size_m, "stock_id": "SPORTSUIT-BLACK-M", "qty": 12},
        {"color": black_color, "size": size_l, "stock_id": "SPORTSUIT-BLACK-L", "qty": 10},
        {"color": blue_color, "size": size_s, "stock_id": "SPORTSUIT-BLUE-S", "qty": 7},
        {"color": blue_color, "size": size_m, "stock_id": "SPORTSUIT-BLUE-M", "qty": 11},
        {"color": blue_color, "size": size_l, "stock_id": "SPORTSUIT-BLUE-L", "qty": 9},
        {"color": red_color, "size": size_s, "stock_id": "SPORTSUIT-RED-S", "qty": 6},
        {"color": red_color, "size": size_m, "stock_id": "SPORTSUIT-RED-M", "qty": 10},
        {"color": red_color, "size": size_l, "stock_id": "SPORTSUIT-RED-L", "qty": 8},
    ]

    for variant_data in sportsuit_variants_data:
        variant = ProductVariant.objects.create(
            product=sportsuit,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["size"]
        )

    # 19. Ноутбук Dell XPS
    dell_laptop = Product.objects.create(
        title="Dell XPS 15",
        description="Мощный ноутбук с высококачественным дисплеем",
        images=["dell-xps-15-2022-770x433.webp"],
        slug="dell-xps-15",
        category=laptops,
        group_by_option_id=processor_type,
        stock_id="DELLXPS15",
        # provider_id="DELL",
        selling_price=100000,
    )

    # Варианты Dell XPS
    dell_variants_data = [
        {"processor": intel_i7, "memory": memory_512, "screen": screen_15, "stock_id": "DELLXPS15-I7-512", "qty": 7},
        {"processor": intel_i7, "memory": memory_1tb, "screen": screen_15, "stock_id": "DELLXPS15-I7-1TB", "qty": 5},
        {"processor": intel_i9, "memory": memory_512, "screen": screen_15, "stock_id": "DELLXPS15-I9-512", "qty": 4},
        {"processor": intel_i9, "memory": memory_1tb, "screen": screen_15, "stock_id": "DELLXPS15-I9-1TB", "qty": 3},
    ]

    for variant_data in dell_variants_data:
        variant = ProductVariant.objects.create(
            product=dell_laptop,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["processor"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["memory"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["screen"]
        )

    # 20. Рубашка повседневная
    casual_shirt = Product.objects.create(
        title="Повседневная рубашка",
        description="Стильная рубашка для повседневной носки",
        images=["rubashka.webp"],
        slug="casual-shirt",
        category=shirts,
        group_by_option_id=color_type,  # Группировка по цвету
        stock_id="CASUALSHIRT",
        # provider_id="CASUALBRAND",
        selling_price=5000,
    )

    # Варианты повседневной рубашки
    casual_shirt_variants_data = [
        {"color": blue_color, "size": size_s, "style": casual_style, "stock_id": "CASUALSHIRT-BLUE-S", "qty": 10},
        {"color": blue_color, "size": size_m, "style": casual_style, "stock_id": "CASUALSHIRT-BLUE-M", "qty": 15},
        {"color": blue_color, "size": size_l, "style": casual_style, "stock_id": "CASUALSHIRT-BLUE-L", "qty": 12},
        {"color": green_color, "size": size_s, "style": casual_style, "stock_id": "CASUALSHIRT-GREEN-S", "qty": 8},
        {"color": green_color, "size": size_m, "style": casual_style, "stock_id": "CASUALSHIRT-GREEN-M", "qty": 14},
        {"color": green_color, "size": size_l, "style": casual_style, "stock_id": "CASUALSHIRT-GREEN-L", "qty": 10},
        {"color": red_color, "size": size_s, "style": casual_style, "stock_id": "CASUALSHIRT-RED-S", "qty": 7},
        {"color": red_color, "size": size_m, "style": casual_style, "stock_id": "CASUALSHIRT-RED-M", "qty": 13},
        {"color": red_color, "size": size_l, "style": casual_style, "stock_id": "CASUALSHIRT-RED-L", "qty": 9},
    ]

    for variant_data in casual_shirt_variants_data:
        variant = ProductVariant.objects.create(
            product=casual_shirt,
            stock_id=variant_data["stock_id"],
            available_quantity=variant_data["qty"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["color"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["size"]
        )

        VariantOption.objects.create(
            product_variant=variant,
            option_value=variant_data["style"]
        )

    print("Создание тестовых данных завершено!")


if __name__ == "__main__":
    create_sample_data()
