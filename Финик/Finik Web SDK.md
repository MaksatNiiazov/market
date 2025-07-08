# Finik Web SDK Documentation

## Introduction to the documentation

1. This documentation helps you integrate Finik Payment System into your program so that your clients can make payments easily using any financial application in Kyrgyzstan.
2. Primarily you will be dealing with Finik Acquiring Service that serves as payment provider for your application.
3. In order to work with the Finik Acquiring Service you need to:

4. [Obtain API Key and your corporate account ID from Finik representatives](https://manchodevs.quip.com/dTaoApuzXEn1/Finik-Web-SDK-Documentation#temp:C:fYQ6f10fb71eee9405092ae98ab9)
5. [Generate Private & Public Keys for the first step of your authorization into Finik Acquiring API](https://manchodevs.quip.com/dTaoApuzXEn1/Finik-Web-SDK-Documentation#temp:C:fYQc8b064e1d53e46e98d72e306f)
6. [Set signature generation process for the second step of your authorization into Finik Acquiring API](https://manchodevs.quip.com/dTaoApuzXEn1/Finik-Web-SDK-Documentation#temp:C:fYQ0fdd6a24d7f247bd80edb7a3e)
7. [Learn how to send requests to Finik Acquiring API](https://manchodevs.quip.com/dTaoApuzXEn1/Finik-Web-SDK-Documentation#temp:C:fYQc3f42b520c094b4ebca6d8333)
8. [Learn how to handle responses from Finik Acquiring API](https://manchodevs.quip.com/dTaoApuzXEn1/Finik-Web-SDK-Documentation#temp:C:fYQaccdeb15ab524b03b6b3080ec)

## Prerequisites

This document describes the interface to interact with **Finik Payment System** through **Finik Web SDK**.  
  
In order to successfully work with the **Finik Web SDK** you need to:  

1. Obtain the `API Key` from Finik representatives.
2. Obtain your corporate account ID from Finik representatives. In some cases companies may have more than one account for different purposes.

## Generate SSL Keys

Before proceeding to service integration, generate **private key** and **public key** certificates for your company. Use the following command to generate the keys on your command line terminal.  

openssl genrsa -out finik_private.pem 2048  
  
openssl rsa -in finik_private.pem -pubout > finik_public.pem

- **Private key:**

- Sign each request to **Finik Acquiring API** using this private key.
- **Important:** Keep it **secret**. If someone gains access to this private key, they may send requests on your behalf.

- **Public key:**

- Send this public key to Finik representatives via a secure channel (Finik email) in order for the service to verify your requests.

## **Authorization via Signature**

In **Finik Acquiring Service** each request is validated using the `signature` provided in the request HTTP header. In order to send a request it is necessary to generate `signature` using the private key.  
  
For Node.js and Python there are available packages that provide convenient classes to generate signatures. We will soon provide similar libraries for other programming languages. In the meantime, for other languages use the signature algorithm explained at the end of this document.  

### Node.js

In Node.js you can use [@mancho.devs/authorizer](https://www.npmjs.com/package/@mancho.devs/authorizer) NPM package.  

### Python

In Python you can use [mancho-devs/python-authorizer](https://github.com/mancho-devs/python-authorizer) package (you can get all the information in README section)  

### Other languages

**1)** Collect data required for generate signature (pseudocode).  

1) data  = Lowercase(HTTP method) + "\n"  
2) data += URIAbsolutePath + "\n"  
3) data += ( header["Host"] and headers that start with x-api-*) + "\n"  
4) data += queryStringParams + "\n"  
5) data += `json``(``request``.``body``)`

**Notes:**  

1. Convert the HTTP header to a lower case. For example: `post`, `get`.
2. Append the `path` part of the URL that starts with a leading `/` (forward slash) and ends before any query parameter (excluding the `?`).
3. Append all headers in the following way:

4. Take header [“Host”].
5. Take all headers that start with `x-api-*`.
6. Take all headers that start with `x-api-*`.
7. Sort by header names alphabetically.
8. Then concatenate in with following way:

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

If the query parameter value is empty, use an empty string as a value. For example, in `http://mancho.dev/examplebucket?acl` the `acl` query parameter has no value. Then, the concatenation should be as follows:  

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

## Create Payment

The signature is required for the request.  
  
**Request type:** `POST`  
**Request URL:**  

- Beta - [https://beta.api.acquiring.averspay.kg/v1/payment](https://beta.api.acquiring.averspay.kg/v1/payment)
- Production - [https://api.acquiring.averspay.kg/v1/payment](https://api.acquiring.averspay.kg/v1/payment)

  
**Headers:** `signature: **<signature>**`  
`x-api-key: **<apiKey**`**`>`**  
`x-api-timestamp: **<timestamp**`**`>`**  

### **HTTP header parameters**

|   |   |   |   |
|---|---|---|---|
|Name|Type|Required/Optional|Description|
|signature|String|Required|Authorization signature generated by you.|
|x-api-key|String|Required|API client key; provided by Finik. Must also be provided in the signature generation step.|
|x-api-timestamp|String|Required|Current timestamp in milliseconds in UNIX type. The same timestamp must also be provided in the signature generation step.|

### **Request body parameters**

|   |   |   |   |
|---|---|---|---|
|Name|Type|Required/Optional|Description|
|`Amount`|Number|Required|A QR is generated with this specific amount. The merchant's client will not be able to specify any custom amount.|
|`CardType`|String|Required|The value must be `FINIK_QR`.|
|`PaymentId`|String|Required|A required field to control the uniqueness of a request. For each request it must be unique so that Finik makes sure there are no dublicate Payment being created for the current client.|
|`RedirectUrl`|String|Required|On success payment Finik Acquiring API will redirect you to this url.|
|`Data`: {  <br>`accountId`: string,  <br>`merchantCategoryCode`: string,  <br>`name_en`: string  <br>}|Json Object|Required|Variables that must be specified.  <br>  <br>- `accountId` - a required field. It is the Finik account where the funds will be deposited acquired from merchant's clients. Reach out to Finik representatives to receive your corporate `accountId` along with `x-api-key`.  <br>  <br>- `merchantCategoryCode` - a required field used as mcc.  <br>  <br>- `name_en` - a required field used as a QR name that will be displayed to merchant's clients on their devices upon payment.|

Sample request:  

`{`  
`"Amount"``:` `100``,`  
`"CardType"``:` `"FINIK_QR"``,`  
`"PaymentId"``:` `uuid``(),`  
"RedirectUrl": "https://example.com/success",  
`"Data"``:` `` ` ```{`  
`"accountId"``:` `"your-account-id"``,`  
`"merchantCategoryCode"``:` `"0742",`  
`"name_en": "your-qr-name",`  
`` }` ``  
`}`

## **Response Parameters**

**On success response Finik Acquiring Service will redirect the user to the provided** `RedirectUrl` .  
  
Sample response to an erroneous request:  

```
{
```

```
{
```

```
{
```

```
{
```

## Payments Status Callback

Finik Payments Status Webhook Documentation is available at [https://manchodevs.quip.com/fyLzAt6TDMtH](https://manchodevs.quip.com/fyLzAt6TDMtH).