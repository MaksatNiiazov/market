# Finik Payments Gateway API

## **Interface Description**

This document describes the interface to interact with **Finik Payments Gateway API** to verify recipients and make service payments.  
  
In order to successfully work with the **Payments Gateway API**:  

1. One needs to obtain the `ApiKey` from Finik representatives.
2. Generate SSL private and public keys.

## Prerequisites

### Generate Keys

Before proceeding to service integration, generate **private key** and **public key** certificates. Use the following command to generate the keys.  

openssl genrsa -out finik_private.pem 2048  
  
openssl rsa -in finik_private.pem -pubout > finik_public.pem

- **Private key:**

- Sign each request to **Finik Acquiring API** using this private key.
- **Important:** Keep it **secret**. If someone gains access to this private key, they may send requests on your behalf.

- **Public key:**

- Send this public key to Finik representatives via a secure channel in order for the service to verify your requests.

## **Authorization**

In **Finik Payments Gateway API** each request is validated using the `signature` provided in the request HTTP header. In order to make a payment it is necessary to generate `signature` using the private key.  
  
For Node.js and Python there are available packages that provide convenient classes to generate signatures. We will soon provide similar libraries for other programming languages. In the meantime, for other languages use the signature algorithm explained at the end of this document.  

### Node.js

In Node.js you can use [@mancho.devs/authorizer](https://www.npmjs.com/package/@mancho.devs/authorizer) NPM package.  

### Python

In Python you can use [mancho-devs/python-authorizer](https://github.com/mancho-devs/python-authorizer) package.  

### Other languages

**1)** Collect data required for generate signature (pseudocode).  

1) data  = Lowercase(HTTP method) + "\n"  
2) data += URIAbsolutePath + "\n"  
3) data += ( header["Host"] and headers that start with x-api-*) + "\n"  
4) data += queryStringParams + "\n"  
5) data += `json``(``request``.``body``)`

**Notes:**  

1. Convert the HTTP header to a lower case. Ex: `post`, `get`.
2. Append the `path` part of the URL that starts with a leading `/` (forward slash) and ends before any query parameter (excluding the `?`).
3. Append all headers in the following way:

4. Take header[“Host”]
5. Take all headers that start with `x-api-*`.
6. Sort by header names alphabetically.
7. Then concatenate in with following way:

parts  = "host" + ":" + String(header["Host"]) + "&"  
  
parts += Lowercase(<HeaderName1>) + ":" + String(<value>) + "&"  
parts += Lowercase(<HeaderName2>) + ":" + String(<value>) + "&"  
...  
parts += Lowercase(<HeaderNameN>) + ":" + String(<value>) 

1. Next, query string parameters must be collected in the following way:

2. Sort by query parameter names alphabetically
3. Then concatenate in the following way:

parts  = URiEncode(<QueryParameter1>) + "=" + URiEncode(<value>) + "&"  
parts += URiEncode(<QueryParameter2>) + "=" + URiEncode(<value>) + "&"  
...  
parts += URiEncode(<QueryParameterN>) + "=" + URiEncode(<value>)

If the query parameter value is empty, use an empty string as a value. For example, in `http://s3.amazonaws.com/examplebucket?acl` the `acl` query parameter has no value. Then, the concatenation should be as follows:  

```
parts += URiEncode("acl") + "=" + ""
```

1. Finally, you should **sort JSON object payload** as well **by object keys**, then stringify it with keys sorted.

**2)** Once data is collected for signature, use the generated private key above and proceed to signature.  
  
For example, in Java:  

public String sign(String payload, String privatePath) {  
  try{  
    Signature signature = Signature.getInstance("SHA256withRSA");  
      
    String privateKeyFile = new String(Files.readAllBytes(Paths.get(privatePath)));  
      
    RSAKey rsaKey = (RSAKey) JWK.parseFromPEMEncodedObjects(privateKeyFile);  
      
    PrivateKey privateKey = rsaKey.toPrivateKey();  
      
    signature.initSign(privateKey);  
      
    signature.update(payload.getBytes(StandardCharsets.UTF_8));  
      
    byte[] signatureValue = signature.sign();  
      
    return Base64.encodeBase64String(signatureValue);  
  }catch (Exception e){  
    throw new AppException(e.getMessage());  
  }  
}

## Check recipient

The signature is required for the request.  
  
**API Status**: stable  
**Request type:** `POST`  
**Request URL/URL запроса:**  

- Beta - [https://beta.api.paymentsgateway.averspay.kg/v2/recipient](https://beta.api.paymentsgateway.averspay.kg/v2/recipient)
- Production - [https://api.paymentsgateway.averspay.kg/v2/recipient](https://api.paymentsgateway.averspay.kg/v2/recipient)

**Headers/Заголовки:** `signature: **<signature>**`  
`x-api-key: **<apiKey**`**`>`**  
`x-api-timestamp: **<timestamp**`**`>`**  

### **HTTP header parameters/Параметры HTTP заголовка**

|   |   |   |   |
|---|---|---|---|
|Название|Тип|Required/Optional|Описание|
|signature|String|Required|Authorization signature|
|x-api-key|String|Required|API client key; provided by Finik. Must also be provided in the signature generation step.|
|x-api-timestamp|String|Required|Current timestamp in milliseconds. The same timestamp must also be provided in the signature generation step.|

### **Request body parameters/Параметры тела запроса**

|   |   |   |   |
|---|---|---|---|
|Название|Тип|Required/Optional|Описание|
|`fields` {  <br>name: value,  <br>...  <br>}|Object|Required|An object representing the required fields for the recipient.  <br>  <br>The value of each field is entered into the object as a `key:value` pair. For example: `phone: +996XXXYYYYYYYZZZZ`.  <br>  <br>It is important to remember that each service may have its own list of fields, which can differ from the fields of another service. The list of services and their required fields can be obtained by making a request to the `GET /services` API.  <br>  <br>Объект, представляющий обязательные реквизиты получателя.  <br>  <br>Значение каждого поля вводится в объект, как `ключ:значение` аттрибуты. Например: `phone: +996XXXYYYZZZ`.  <br>  <br>К сведению, каждая услуга может иметь свои поля, которые могут отличаться от полей других услуг. Список услуг и их обязательные поля можно получить, сделав запрос на `GET /services` API.|
|`service`|String|Required|Service ID in the Finik domain.  <br>ID услуги в домене Finik.|

### **Response Parameters/Параметры ответа**

|   |   |   |   |
|---|---|---|---|
|Название|Тип|Required/Optional|Описание|
|`statusCode`|String|Required|Response Status/Статус ответа.|
|`name`|String|Optional|Recipient's full name. Present if the service provider returns such data.  <br>  <br>In the case of Finik name includes the recipient's initials. For example: А. У.  <br>  <br>ФИО получателя. Присутствует, если поставщик услуг предоставляет такие данные.  <br>  <br>В случае Finik `name` включает инициалы получателя. Например: `А. У.`|
|`phone`|String|Optional|Recipient's requisite. Present for Finik service.  <br>Реквизит получателя. Присутствует для услуги Finik.|

Sample request/Пример запроса:  

```
{
```

  
Sample response to a successful request/Пример ответа на успешный запрос:  

```
{
```

Sample response in case of a nonexistent recipient/Пример ответа в случае несуществующего реквизита:  

```
{
```

Sample response in case of a blocked recipient/Пример ответа в случае заблокированного реквизита:  

```
{
```

## **Making payment/**Создание платежа

The signature is required for the request.  
  
**API Status**: stable  
**Request type:** `POST`  
**Request URL/URL запроса:**  

- Beta - [https://beta.api.paymentsgateway.averspay.kg/v2/payment](https://beta.api.paymentsgateway.averspay.kg/v2/payment)
- Production - [https://api.paymentsgateway.averspay.kg/v2/payment](https://api.paymentsgateway.averspay.kg/v2/payment)

**Headers/Заголовки:** `signature: **<signature>**`  
`x-api-key: **<apiKey**`**`>`**  
`x-api-timestamp: **<timestamp**`**`>`**  
Note: **timestamp** will be valid only **10 seconds** after creation.  

### **HTTP header parameters/Параметры HTTP заголовка**

|   |   |   |   |
|---|---|---|---|
|Название|Тип|Required/Optional|Описание|
|signature|String|Required|Authorization signature|
|x-api-key|String|Required|API client key; provided by Finik. Must also be provided in the signature generation step.|
|x-api-timestamp|String|Required|Current timestamp in milliseconds. The same timestamp must also be provided in the signature generation step.|

### **Request body parameters/Параметры тела запроса**

|   |   |   |   |
|---|---|---|---|
|Название|Тип|Required/Optional|Описание|
|`accountId`|String|Required|ID of the account from which the payment is debited. The user with `userId` must have permissions to debit from this account.  <br>  <br>ID счета, откуда списывается платеж. Пользователь с ID `userId` должен иметь права для списывания с этого счета.|
|`fields` {  <br>name: value,  <br>...  <br>}|Object|Required|An object representing the required fields for the recipient.  <br>  <br>The value of each field is entered into the object as a `key:value` pair. For example: `phone: +996XXXYYYYYYYZZZZ`.  <br>  <br>It is important to remember that each service may have its own list of fields, which can differ from the fields of another service. The list of services and their required fields can be obtained by making a request to the `GET /services` API.  <br>  <br>Объект, представляющий обязательные реквизиты получателя.  <br>  <br>Значение каждого поля вводится в объект, как `ключ:значение` аттрибуты. Например: `phone: +996XXXYYYZZZ`.  <br>  <br>К сведению, каждая услуга может иметь свои поля, которые могут отличаться от полей других услуг. Список услуг и их обязательные поля можно получить, сделав запрос на `GET /services` API.|
|`service` {  <br>id: String  <br>}|Object|Required|An object representing the required fields of the service. `id` indicates the ID of the service in the Finik domain.  <br>  <br>Объект, представляющий обязательные поля услуги. `id` указывает на ID услуги в домене Finik.|
|`transactionId`|String|Required|A unique transaction ID used to prevent duplicate requests from this client.  <br>  <br>Уникальный ID транзакции, используемое для предотвращения дубликатов при повторных запросах с данного клиента.|
|`userId`|String|Required|The ID of the user the request is being made on behalf of.  <br>  <br>ID пользователя, от имени которого делается запрос.|

Sample request/Пример запроса:  

```
{
```

### **Response Parameters/Параметры ответа**

|   |   |   |   |
|---|---|---|---|
|Название|Тип|Required/Optional|Описание|
|`accountId`|String|Required|ID of the account from which the payment is debited. The user with `userId` must have permissions to debit from this account.  <br>  <br>ID счета, откуда списывается платеж. Пользователь с ID `userId` должен иметь права для списывания с этого счета.|
|`fields` {  <br>name: value,  <br>...  <br>}|Object|Required|An object representing the required fields for the recipient.  <br>  <br>The value of each field is entered into the object as a `key:value` pair. For example: `phone: +996XXXYYYYYYYZZZZ`.  <br>  <br>It is important to remember that each service may have its own list of fields, which can differ from the fields of another service. The list of services and their required fields can be obtained by making a request to the `GET /services` API.  <br>  <br>Объект, представляющий обязательные реквизиты получателя.  <br>  <br>Значение каждого поля вводится в объект, как `ключ:значение` аттрибуты. Например: `phone: +996XXXYYYZZZ`.  <br>  <br>К сведению, каждая услуга может иметь свои поля, которые могут отличаться от полей других услуг. Список услуг и их обязательные поля можно получить, сделав запрос на `GET /services` API.|
|`id`|String|Required|The unique ID of the transaction in the Finik domain.  <br>  <br>Уникальный ID транзакции в домене Finik.|
|`requestDate`|Number|Required|The date of the received request in UNIX timestamp format.  <br>  <br>Дата поступившего запроса в формате UNIX timestamp.|
|`service` {  <br>id: String  <br>}|Object|Required|An object representing the required fields of the service. `id` indicates the ID of the service in the Finik domain.  <br>  <br>Объект, представляющий обязательные поля услуги. `id` указывает на ID услуги в домене Finik.|
|`status`|String|Required|Payment (transaction) status. Status options: `CANCELED`, `FAILED`, `PENDING`, `PROCESSING`, `SUCCEEDED`.  <br>  <br>Статус платежа (транзакции). Варианты статусов: `CANCELED`, `FAILED`, `PENDING`, `PROCESSING`, `SUCCEEDED`.|
|`statusCode`|Number|Required|Response Status. A successful response contains `statusCode: 200` for synchronous services or `statusCode: 201` for asynchronous services.  <br>  <br>Currently only Averspay is a synchronous service.  <br>  <br>Статус ответа. Успешный ответ содержит `statusCode: 200` для синхронных услуг или `statusCode: 201` для асинхронных услуг.  <br>  <br>На данный момент только Finik является синхронной услугой.|
|`transactionDate`|Number|Optional|Transaction date in UNIX timestamp format. The presence of this field indicates the final state of the payment.  <br>  <br>Дата проведения транзакции в формате UNIX timestamp. Наличие этого поля указывает на конечное состояние платежа.|
|`transactionId`|String|Required|A unique transaction ID used to prevent duplicate requests from this client.  <br>  <br>Уникальный ID транзакции, используемое для предотвращения дубликатов при повторных запросах с данного клиента.|
|`userId`|String|Required|The ID of the user the request is being made on behalf of.  <br>  <br>ID пользователя, от имени которого делается запрос.|

Sample response to a successful payment request to Finik service/Пример ответа на успешный запрос платежа для услуги Finik:  

```
{
```

Sample response to an erroneous request/Пример ответа на ошибочный запрос:  

```
{
```

## Check payment status/Проверка платежа

For better user experience and performance it is recommended to implement [Payments Status Callback](https://quip.com/zblmAPa7lhQX#temp:C:MYO9ace7f698868419aaf532ac7c) endpoint.  
  
**API Status**: stable  
**Request type:** `GET`  
**Request URL/URL запроса:**  

- Beta - [https://beta.api.paymentsgateway.averspay.kg/v2/payments/{paymentId}](https://beta.api.paymentsgateway.averspay.kg/v2/payments/{paymentId})
- Production - [https://api.paymentsgateway.averspay.kg/v2/payments/{paymentId}](https://beta.api.paymentsgateway.averspay.kg/v2/payment)

**Headers/Заголовки:** `signature: **<signature>**`  
`x-api-key: **<apiKey**`**`>`**  
`x-api-timestamp: **<timestamp**`**`>`**  
Note: **timestamp** will be valid only **10 seconds** after creation.  

### **HTTP header parameters/Параметры HTTP заголовка**

|   |   |   |   |
|---|---|---|---|
|Название|Тип|Required/Optional|Описание|
|signature|String|Required|Authorization signature|
|x-api-key|String|Required|API client key; provided by Finik. Must also be provided in the signature generation step.|
|x-api-timestamp|String|Required|Current timestamp in milliseconds. The same timestamp must also be provided in the signature generation step.|

### **Request parameters/Параметры запроса**

|   |   |   |   |
|---|---|---|---|
|Название|Тип|Required/Optional|Описание|
|`{paymentId}`|String|Required|The payment ID received in response to the payment request.  <br>  <br>ID платежа, полученный в ответ на запрос платежа.|

Sample response to a successful payment status check request/Пример ответа на успешный запрос проверки платежа:  

```
{
```

Sample response to an erroneous request/Пример ответа на ошибочный запрос:  

```
{
```

**Note** that in the _beta_ environment all requests are idle, in other words **no** real payment will be made to the service provider. Hence, in the _beta_ environment the system will randomly return different statuses like successful or erroneous. Therefore, if you see an erroneous status, do not be frightened. Thus, while testing in the beta environment the system is intentionally set up so that you can implement error handling on your side.  
  
**Нужно отметить**, что в _бета_ среде все запросы - холостые, то есть реальных платежей в сторону поставщика услуг (ПУ) **не** будут. В связи с этим система рандомно будет возвращать разные статусы, например, успешный или наоборот ошибочный. Поэтому, увидя ошибочный статус, не пугайтесь. Таким образом, на стадии тестирования в бета среде система намеренно настроена так, чтобы Вы могли реализовать обработку ошибок на своей стороне.  

### **How often one must check the payment status/**Как часто проверять статус платежа

In practice we observed that the payment status changes on the service provider's side within 30 seconds in 99% of cases, therefore you can set a 30-second timeout, then check the payment status.  
  
По опыту мы видим, что статус платежа изменяется на стороне поставщика услуг в течение 30 секунд в 99% случаев, поэтому можете поставить себе отсрочку в 30 секунд, затем проверьте статус платежа.  

## Status codes/Коды статусов

|statusCode|errorMessage|retriable|
|---|---|---|
|200|Payment has been successfully completed.|No|
|201|Payment has been successfully accepted for asynchronous processing.|
|400|A payload must be provided.|
|An unrecognizable payload is provided.|
|Transaction ID is required.|
|A valid service is required.|
|An invalid or missing service ID is provided.|
|Invalid service ID is provided.|
|Fields must be an object and include all required fields.|
|An invalid amount is provided. Amount must be greater than 0.|
|Account ID is required.|
|User ID is required.|
|Invalid user ID is provided.|
|User is disabled.|
|Source and destination accounts must be different.|
|An invalid payment ID is provided.|
|401|An invalid or missing `Authorization` header is provided.|
|An invalid client ID is provided.|
|402|Insufficient funds.|
|403|User is not authorized to access this resource with an explicit deny.|
|User has no permissions to access this account.|
|Client has no permissions to access this payment.|
|404|The requested resource has not been found. Eg. `User does not exist.` or `An invalid operation ID is provided.`|
|409|Transaction with the same ID already exists.|
|500|Internal Server Error|Yes|
|An unexpected error has occurred.|
|502|Service "XXX" is temporarily unavailable.|
|Service provider is unavailable.|
|503|The server cannot handle the request because it is overloaded or down for maintenance.|

## Services/Услуги

### List of services/Список услуг

The signature is required for the request.  
  
**API Status**: stable  
**Request type:** `POST`  
**Request URL/URL запроса:**  

- Beta - [https://beta.api.paymentsgateway.averspay.kg/v2/services](https://beta.api.paymentsgateway.averspay.kg/v2/services)
- Production - [https://api.paymentsgateway.averspay.kg/v2/services](https://api.paymentsgateway.averspay.kg/v2/services)

**Headers/Заголовки:** `signature: **<signature>**`  
`x-api-key: **<apiKey**`**`>`**  
`x-api-timestamp: **<timestamp**`**`>`**  
Note: **timestamp** will be valid only **10 seconds** after creation.  

### **HTTP header parameters/Параметры HTTP заголовка**

|   |   |   |   |
|---|---|---|---|
|Название|Тип|Required/Optional|Описание|
|signature|String|Required|Authorization signature|
|x-api-key|String|Required|API client key; provided by Finik. Must also be provided in the signature generation step.|
|x-api-timestamp|String|Required|Current timestamp in milliseconds. The same timestamp must also be provided in the signature generation step.|

### **Request body parameters/Параметры тела запроса**

|   |   |   |   |
|---|---|---|---|
|Название|Тип|Required/Optional|Описание|
|`from`|Number|Optional|Defaults from the first service. Starts from scratch.  <br>  <br>По умолчанию, с первой услуги. Начинается с нуля.|
|`size`|Number|Optional|Number of services. Default is `20` records. Maximum - `50` records.  <br>  <br>Количество услуг. По умолчанию - `20` записей. Максимум - `50` записей.|
|`filter {   status: String[],   parentId: String   }`|Object|Optional|Service Filter. Possible fields:  <br>  <br>- `status`: array of strings. Valid values: `ENABLED`, `DISABLED`, `INACTIVE`. Default: `[ENABLED, DISABLED]`.  <br>- `parentId`: a string representing the ID of the parent category. If not specified, all services will be returned. If specified, only services in this category will be returned.  <br>  <br>Фильтр услуг. Возможные поля:  <br>  <br>- `status`: массив строк. Возможные значения: `ENABLED`, `DISABLED`, `INACTIVE`. По умолчанию: `[ENABLED, DISABLED]`.  <br>- `parentId`: строка, означающий ID родительской категории. Если не указано, то вернутся все услуги. Если указать, то вернутся услуги только в этой категории.|
|`locale`|String|Optional|Language of service names. Possible values: `EN`, `KY`, `RU`. Default: `EN`.  <br>  <br>Язык названий услуг. Возможные значения: `EN`, `KY`, `RU`. По умолчанию: `EN.`|
|`query`|String|Optional|A field to search for services by name. The search will be performed in all supported languages.  <br>  <br>Поле для поиска услуг по названию. Поиск будет происходить на всех поддерживаемых языках.|

Sample request/Пример запроса:  

{  
    from: 0,  
    query: '',  
    locale: 'EN',  
    size: 20,  
    filter: {  
        parentId: 'kyrgyzstan',  
    },  
}

An example of a response to a successful request/Пример ответа на успешный запрос:  

```
{
```

It is necessary to pay attention to the `requiredFields` field. It lists all the fields that are required to create the payment to that specific service. For example, in order to make a payment to the `O!` service above, one must provide 3 fields in the `fields` attribute:  
  
Необходимо уделить внимание на поле `requiredFields`. В нем перечислены все поля, которые необходимы для создания платежа в сторону определенной услуги. Например, для услуги `О!` выше, необходимо предоставить 3 поля в `fields` для платежа:  

```
{
```

## Payments Status Callback

Finik Payments Status Webhook Documentation is available at [https://manchodevs.quip.com/fyLzAt6TDMtH](https://manchodevs.quip.com/fyLzAt6TDMtH).