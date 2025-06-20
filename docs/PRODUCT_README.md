# Руководство по товарам

Этот проект предоставляет GraphQL-интерфейс для управления каталогом товаров. Ниже приведены примеры создания товара и обновления товара и его вариантов.

## Создание товара

Используйте мутацию `createProduct`. Она принимает основные поля товара и список его вариантов.

Пример запроса:

```graphql
mutation CreateProduct($variants: [ProductVariantInput!]!) {
  createProduct(
    title: "Кроссовки"
    description: "Беговые кроссовки"
    categoryId: 1
    merchantId: 1
    brand: "Adidas"
    productVariants: $variants
  ) {
    product {
      id
      title
    }
  }
}
```

Значение переменной `variants`:

```json
[
  {
    "article": "ABC-001",
    "costPrice": 1000.0,
    "sellingPrice": 1500.0,
    "optionValueIds": [1, 2],
    "imageId": 3
  }
]
```

## Обновление товара

Для изменения существующего товара используйте `updateProduct`.

```graphql
mutation {
  updateProduct(
    productId: 10
    title: "Обновлённый товар"
    description: "Новое описание"
    brand: "Another"
  ) {
    product {
      id
      title
      description
      brand
    }
  }
}
```

## Обновление варианта товара

Если нужно изменить отдельный вариант, доступна мутация `updateProductVariant`.

```graphql
mutation {
  updateProductVariant(
    variantId: 5
    article: "ABC-001-NEW"
    costPrice: 1200.0
    sellingPrice: 1700.0
    optionValueIds: [1, 3]
    imageId: 4
  ) {
    productVariant {
      id
      article
      costPrice
      sellingPrice
    }
  }
}
```
