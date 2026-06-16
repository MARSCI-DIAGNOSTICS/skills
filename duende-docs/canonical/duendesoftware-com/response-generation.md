---
title: Response Generation
source_url: https://docs.duendesoftware.com/response-generation/
source_type: llms-full-txt
content_hash: sha256:b88ccb8a66f6452d204d54a852f1ce95b59f699d9e37e02df4b3224aa783c4d3
doc_id: response-generation
---

> Reference documentation for dynamic client registration response generation, including interfaces and implementations for handling HTTP responses in the registration process.

## IDynamicClientRegistrationResponseGenerator

[Section titled "IDynamicClientRegistrationResponseGenerator"](#idynamicclientregistrationresponsegenerator)

The `IDynamicClientRegistrationResponseGenerator` interface defines the contract for a service that generates dynamic client registration responses.

```csharp
public interface IDynamicClientRegistrationResponseGenerator
```

### Members

[Section titled "Members"](#members)

| name                     | description                                                              |
| ------------------------ | ------------------------------------------------------------------------ |
| WriteBadRequestError(...)  | Writes a bad request error to the HTTP context.                          |
| WriteContentTypeError(...) | Writes a content type error to the HTTP response.                        |
| WriteProcessingError(...)  | Writes a processing error to the HTTP context.                           |
| WriteResponse(...)         | Writes a response object to the HTTP context with the given status code. |
| WriteSuccessResponse(...)  | Writes a success response to the HTTP context.                           |
| WriteValidationError(...)  | Writes a validation error to the HTTP context.                           |

## DynamicClientRegistrationResponseGenerator

[Section titled "DynamicClientRegistrationResponseGenerator"](#dynamicclientregistrationresponsegenerator)

The `DynamicClientRegistrationResponseGenerator` is the default implementation of the `IDynamicClientRegistrationResponseGenerator`. If you wish to customize a particular aspect of response generation, you can extend this class and override the appropriate methods. You can also set JSON serialization options by overriding its `SerializerOptions` property.

### Members

[Section titled "Members"](#members-1)

| name                            | description                                         |
| ------------------------------- | --------------------------------------------------- |
| SerializerOptions { get; set; } | The options used for serializing json in responses. |
