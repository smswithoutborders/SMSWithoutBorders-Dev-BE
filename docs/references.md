# SMSwithoutBorders Developers API

> Version 0.1.0

## Path Table

| Method | Path                                                                                            | Description                            |
| ------ | ----------------------------------------------------------------------------------------------- | -------------------------------------- |
| POST   | [/authenticate](#postauthenticate)                                                              | Get permission to use token externally |
| POST   | [/login](#postlogin)                                                                            | Authenticate a User                    |
| POST   | [/signup](#postsignup)                                                                          | Create a new User                      |
| GET    | [/users/{user_id}/products](#getusersuser_idproducts)                                           | Get all users products                 |
| DELETE | [/users/{user_id}/products/{product_name}](#deleteusersuser_idproductsproduct_name)             | Unsubscribe for a products             |
| POST   | [/users/{user_id}/products/{product_name}](#postusersuser_idproductsproduct_name)               | Subscribe for a products               |
| GET    | [/users/{user_id}/products/{product_name}/metrics](#getusersuser_idproductsproduct_namemetrics) | Get products metrics                   |
| GET    | [/users/{user_id}/tokens](#getusersuser_idtokens)                                               | Generate an auth_key and an auth_id    |

## Reference Table

| Name | Path | Description |
| ---- | ---- | ----------- |

## Path Details

---

### [POST]/authenticate

- Summary  
  Get permission to use token externally

#### RequestBody

- application/json

```ts
{
  auth_key?: string
  auth_id?: string
}
```

#### Responses

- 200 Successful. A cookie is set on the user's agent

`application/json`

```ts
{
}
```

- 400 Bad Request (e.g missing required fields)

`application/json`

```ts
{
  "type": "string"
}
```

- 401 Unauthorized (e.g User, Platform not found)

`application/json`

```ts
{
  "type": "string"
}
```

- 409 Conflict (e.g Duplicate Users, Platforms found)

`application/json`

```ts
{
  "type": "string"
}
```

- 500 Internal Server Error

`application/json`

```ts
{
  "type": "string"
}
```

---

### [POST]/login

- Summary  
  Authenticate a User

#### RequestBody

- application/json

```ts
{
  email?: string
  password?: string
}
```

#### Responses

- 200 Successful. A cookie is set on the user's agent

`application/json`

```ts
{
  uid?: string
  email?: string
  auth_key?: string
  auth_id?: string
}
```

- 400 Bad Request (e.g missing required fields)

`application/json`

```ts
{
  "type": "string"
}
```

- 401 Unauthorized (e.g User, Platform not found)

`application/json`

```ts
{
  "type": "string"
}
```

- 409 Conflict (e.g Duplicate Users, Platforms found)

`application/json`

```ts
{
  "type": "string"
}
```

- 500 Internal Server Error

`application/json`

```ts
{
  "type": "string"
}
```

---

### [POST]/signup

- Summary  
  Create a new User

#### RequestBody

- application/json

```ts
{
  email?: string
  password?: string
}
```

#### Responses

- 200 Successful

`application/json`

```ts
{
}
```

- 400 Bad Request (e.g missing required fields)

`application/json`

```ts
{
  "type": "string"
}
```

- 401 Unauthorized (e.g User, Platform not found)

`application/json`

```ts
{
  "type": "string"
}
```

- 409 Conflict (e.g Duplicate Users, Platforms found)

`application/json`

```ts
{
  "type": "string"
}
```

- 500 Internal Server Error

`application/json`

```ts
{
  "type": "string"
}
```

---

### [GET]/users/{user_id}/products

- Summary  
  Get all users products

#### RequestBody

- application/json

```ts
{
}
```

#### Responses

- 200 Successful. A cookie is set on the user's agent

`application/json`

```ts
{
  "subscribed": {
    "type": "array"
  },
  "unsubscribed": {
    "type": "array"
  }
}
```

- 400 Bad Request (e.g missing required fields)

`application/json`

```ts
{
  "type": "string"
}
```

- 401 Unauthorized (e.g User, Platform not found)

`application/json`

```ts
{
  "type": "string"
}
```

- 409 Conflict (e.g Duplicate Users, Platforms found)

`application/json`

```ts
{
  "type": "string"
}
```

- 500 Internal Server Error

`application/json`

```ts
{
  "type": "string"
}
```

---

### [DELETE]/users/{user_id}/products/{product_name}

- Summary  
  Unsubscribe for a products

#### RequestBody

- application/json

```ts
{
}
```

#### Responses

- 200 Successful. A cookie is set on the user's agent

`application/json`

```ts
{
}
```

- 400 Bad Request (e.g missing required fields)

`application/json`

```ts
{
  "type": "string"
}
```

- 401 Unauthorized (e.g User, Platform not found)

`application/json`

```ts
{
  "type": "string"
}
```

- 409 Conflict (e.g Duplicate Users, Platforms found)

`application/json`

```ts
{
  "type": "string"
}
```

- 500 Internal Server Error

`application/json`

```ts
{
  "type": "string"
}
```

---

### [POST]/users/{user_id}/products/{product_name}

- Summary  
  Subscribe for a products

#### RequestBody

- application/json

```ts
{
}
```

#### Responses

- 200 Successful. A cookie is set on the user's agent

`application/json`

```ts
{
}
```

- 400 Bad Request (e.g missing required fields)

`application/json`

```ts
{
  "type": "string"
}
```

- 401 Unauthorized (e.g User, Platform not found)

`application/json`

```ts
{
  "type": "string"
}
```

- 409 Conflict (e.g Duplicate Users, Platforms found)

`application/json`

```ts
{
  "type": "string"
}
```

- 500 Internal Server Error

`application/json`

```ts
{
  "type": "string"
}
```

---

### [GET]/users/{user_id}/products/{product_name}/metrics

- Summary  
  Get products metrics

#### RequestBody

- application/json

```ts
{
}
```

#### Responses

- 200 Successful. A cookie is set on the user's agent

`application/json`

```ts
{
  "data": {
    "type": "array"
    },
  "summary": {
    "type": "object"
    }
}
```

- 400 Bad Request (e.g missing required fields)

`application/json`

```ts
{
  "type": "string"
}
```

- 401 Unauthorized (e.g User, Platform not found)

`application/json`

```ts
{
  "type": "string"
}
```

- 409 Conflict (e.g Duplicate Users, Platforms found)

`application/json`

```ts
{
  "type": "string"
}
```

- 500 Internal Server Error

`application/json`

```ts
{
  "type": "string"
}
```

---

### [GET]/users/{user_id}/tokens

- Summary  
  Generate an auth_key and an auth_id

#### RequestBody

- application/json

```ts
{
}
```

#### Responses

- 200 Successful. A cookie is set on the user's agent

`application/json`

```ts
{
  auth_key?: string
  auth_id?: string
}
```

- 400 Bad Request (e.g missing required fields)

`application/json`

```ts
{
  "type": "string"
}
```

- 401 Unauthorized (e.g User, Platform not found)

`application/json`

```ts
{
  "type": "string"
}
```

- 409 Conflict (e.g Duplicate Users, Platforms found)

`application/json`

```ts
{
  "type": "string"
}
```

- 500 Internal Server Error

`application/json`

```ts
{
  "type": "string"
}
```

## References
