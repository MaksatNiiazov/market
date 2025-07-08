# Finik QR Documentation

This is a documentation to generate ELQR standardized by the National Bank of Kyrgyz Republic. These QR images are compatible and recognized by all financial mobile applications in Kyrgyzstan.  

## CreateItem (Create QR)

In order to generate a QR one must send a `CreateItem` request to Finik GraphQL server using the following specifications. Note that this is not a REST API but a [GraphQL](https://graphql.org/learn/) API.  
  
**Request type:** `POST`  
**Request URL:**  

- Beta: [https://beta.api.paymentsgateway.averspay.kg/graphql](https://beta.graphql.averspay.kg/graphql)
- Production: [https://api.paymentsgateway.averspay.kg/graphql](https://graphql.averspay.kg/graphql)

### **HTTP header parameters**

|   |   |   |   |
|---|---|---|---|
|Name|Type|Required/Optional||
|`x-api-key`|String|Required|API client key; provided by Finik.|

### **Request body parameters**

|   |   |   |   |
|---|---|---|---|
|Name|Type|Required/Optional|Description|
|query|String|Required|A static string in the specified format as shown below:  <br>  <br>`1. mutation CreateItem($input: CreateItemInput!) {   2. createItem(input: $input) {   3. callbackUrl   4. fixedAmount   5. id   6. name_en   7. qrCode {   8. url   9. image   10. }   11. status   12. }   13. }`  <br>  <br>This query indicates:  <br>  <br>1. The operation to call `CreateItem`..  <br>2. The parametes to pass `$input` with `CreateItemInput` interface. The parameter values must be defined in the separate `variables`.  <br>3. On lines `3-11` one can specify a list of field to return from the server.  <br>4. Object fields must be nested as shown on lines `7-10`.  <br>5. It is optional to request fields between lines 3-11. One can specify no fields, and the server will retrun no values.|
|operationName|String|Required|The value must be `CreateItem`.|
|variables {  <br>input: {  <br>account: {  <br>id: string  <br>},  <br>callbackUrl: string,  <br>maxAvailableQuantity: Integer,  <br>name_en: string,  <br>status: enum,  <br>fixedAmount: number,  <br>requiredFields: object,  <br>requestId: string  <br>}  <br>}|Object|Required|Variables that must be specified.  <br>  <br>- `account: {id: string}` - a required field. It is the Finik account where the funds will be deposited acquired from merchant's clients. Reach out to Finik representatives to receive your corporate `accountId` with `x-api-key`.  <br>  <br>- `callbackUrl` - an optional field used as a webhook; when specified, Finik will send a `POST` request to your server with the payment details in its body in JSON format, including its final status that can be either `SUCCEEDED` or `FAILED` as well as `requiredFields` in the form of `fields` object attribute.  <br>  <br>- `maxAvailableQuantity` - the value must be `1`.  <br>  <br>- `name_en` - a required field used as a QR name that will be displayed to merchant's clients on their devices upon payment.  <br>  <br>- `status` - a required field that indicates wheather or not the QR must be enabled. Valid values are `ENABLED` or `DISABLED`. When disabled, a merchant's client will not be able to deposit funds.  <br>  <br>- `fixedAmount` - an optional field. When specified, a QR is generated with this specific amount. The merchant's client will not be able to specify any custom amount.  <br>  <br>- `requiredFields` - an optional field. When specified, Finik will proxy the provided `key:value` in the `fields` field when sending the payment details to `callbackUrl` if configured.  <br>  <br>- `requestId` - a required field to control the uniqueness of a request. For each request it must be unique so that Finik makes sure there are no dublicate QR items being created.|

That’s why `query` and `operationName` fields are always static.  
  
Sample request:  

```
{
```

### **Response Parameters**

|   |   |   |
|---|---|---|
|Name|Type|**Description**|
|data|Object|Object data|

Sample response to a successful request:  

```
{
```

Sample response in error cases:  

{   
   "`errors`": [  
        {  
            "errorType": "ValidationException",  
            "messase": "`accountId` does not belong to requested user"  
        }  
   ]  
}

## Status codes

|statusCode|errorMessage|
|---|---|
|200|on success and error cases|

## GetItem (Get QR)

In order to get QR one must send a `GetItem` request to Finik GraphQL server using the following specifications. Note that this is not a REST API but a [GraphQL](https://graphql.org/learn/) API.  
  
**Request type:** `POST`  
**Request URL:**  

- Beta: [https://beta.graphql.averspay.kg/graphql](https://beta.graphql.averspay.kg/graphql)
- Production: [https://graphql.averspay.kg/graphql](https://graphql.averspay.kg/graphql)

### **HTTP header parameters**

|   |   |   |   |
|---|---|---|---|
|Name|Type|Required/Optional||
|`x-api-key`|String|Required|API client key; provided by Finik.|

### **Request body parameters**

|   |   |   |   |
|---|---|---|---|
|Name|Type|Required/Optional|Description|
|query|String|Required|A static string in the specified format as shown below:  <br>  <br>`1. query GetItem($input: ServiceInput!) {   2. getItem(input: $input) {   3. callbackUrl   4. fixedAmount   5. id   6. name_en   7. qrCode {   8. url   9. image   10. }   11. status   12. }   13. }`  <br>  <br>This query indicates:  <br>  <br>1. The operation to call `GetItem`.  <br>2. The parametes to pass `$input` with `ServiceInput` interface. The parameter values must be defined in the separate `variables`.  <br>3. On lines `3-11` one can specify a list of field to return from the server.  <br>4. Object fields must be nested as shown on lines `7-10`.  <br>5. It is optional to request fields between lines 3-11. One can specify no fields, and the server will retrun no values.|
|operationName|String|Required|The value must be `GetItem`.|
|variables {  <br>input: {  <br>id: string  <br>}  <br>}|Object|Required|Variables that must be specified.  <br>  <br>- `id` - a required field. It is the identifier of item(QR)|

That’s why `query` and `operationName` fields are always static.  
  
Sample request:  

```
{
```

### **Response Parameters**

|   |   |   |
|---|---|---|
|Name|Type|**Description**|
|data|Object|Object data|

Sample response to a successful request:  

```
{
```

Sample response in error cases:  

{   
   "`errors`": [  
        {  
            "errorType": "ResourceNotFoundException",  
            "messase": "No item exists with this identifier: qr-id"  
        }  
   ]  
}

## Status codes

|statusCode|errorMessage|
|---|---|
|200|on success and error cases|

## Payments Status Callback

Finik Payments Status Webhook Documentation is available at [https://manchodevs.quip.com/fyLzAt6TDMtH](https://manchodevs.quip.com/fyLzAt6TDMtH).