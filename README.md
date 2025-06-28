**DATA VALIDATION VS DATA SANTIZATION :**

|                      | **Data Validation**                        | **Data Sanitization**                   |
| -------------------- | ------------------------------------------ | --------------------------------------- |
| **Goal**             | Check if data is _correct_                 | Make data _safe and clean_              |
| **When used**        | Before insert/update to ensure correctness | Before using/storing/displaying data    |
| **Example check**    | `email.includes('@')`                      | `email.trim().toLowerCase()`            |
| **Common use cases** | Forms, API validation, DB constraints      | Prevent XSS, SQL injection, consistency |

**MONGOSSE DOCUMENT :** https://mongoosejs.com/docs/

**VALIDATOR - npm pkg :**

validating data like email is tuff and to make validations easy we have a npm pkg "validator"

validates :
URL,
email,
pass, ..... etc.

installation :

        npm i validator

encryption pass we use npm pkg called "bcrypt"
gives us encrypt and validate fn

installation :

```bash
npm i bcrypt
```

**JWT : JSON WEB TOKEN** https://jwt.io/

![JWT Image](src/assets/JWT.png)

- jwt contains special information inside them
- it has threee thing :
- **GREEN (header) :**
- **WHITE (payload = secret data which we can hide inside token from the server) :**
- **BLUE (signature = JWT uses it to validate token) :**

- when we hit the login api , the login api will validate user pass and generate the JWT token
- this JWT token will attached with cookies and send back to client/browser as cookie
- the cliet/browser will keep this cookie safely
- after this whenever we hit any api the cookie will be sent along JWT token tot he server
- the API will extract token Validate and then perfom its work

**CREATING JWT TOKEN :**

- we need another pkg for that called `jsonwebtoken` dev by auth0
- install `npm i jsonwebtoken`
- require `const JWT = require("jsonwebtoken");`
- `const token = await JWT.sign({_id : userExist._id}, "DEV@tinder$1234");`
  - `{_id : userExist._id}` ==> secret/hidden data which we/server is sending
  - `"DEV@tinder$1234"` ==> secret key is like a password

**sending cookies to client :**

- `res.cookie("token", token);`

**reading cookies:**

const cookies = req.cookies; // O/P => undefined

- to read cookies we need another library which will provide a middleware to parse cookies know as "cookie-parser"
- npm i cookie-parser //dev by express
- import => const cookieParser = require("cookie-parser);
- middleware ==> app.use(cookieParser());

**VERIFYING TOKEN :**

- `const decodedMessage = await JWT.verify(token, "DEV@tinder$1234");`
  - token ==> token sent along cookies by client
  - `"DEV@tinder$1234"` ==> secret key used during generation
  - this verify() method return the secret message used during generation (ie \_id) not bool
  - we can extract secret msg ==> const {\_id} = decodedMessage
  - and the perform the work and send res back
  - if token invalid we dont have to explicitly throw error it handeled automatically

**add token expiry time :**

  ```javascript
  const token = await JWT.sign({_id : userExist._id}, "DEV@tinder$1234", {expiresIn : "1d"});
  ```

**add cookies expiry time :**

```javascript
res.cookie("token", token, {
expires : new Date(Date.now() + 8 * 3600000),
});
```
#
# MONGOOSE SCHEMA METHOD :

- custom function that you define on a schema,
- it becomes available on instances (documents) created from that schema.
- It's a way to encapsulate behavior related to your data model, making your code more modular and expressive.

```javascript
MySchema.methods.myCustomMethod = function() {
  // `this` refers to the document
};
```
- always use `function () {} ` while creating custome method beacuse in this custom method `this` keyword is used
- `this` keyword cannot be used inside arrow fn

**JWT TOKEN GENEARTION USING SCHEMA METHODS :**

```javascript
//generating JWT Token    //standard way
userSchema.methods.getJWT = async function () {
  const user = this   //point to current instance
  const token = await jwt.sign({ _id: user._id }, "DEV@tinder$1234");

  return token;
}

// usage
// standard way, we offloaded generating JWT to schema methods ie we created ahelper fn
const token = await userExist.getJWT();
console.log(token);
```

# Schema Methods vs. Static Methods

| Feature             | **Schema Method**                           | **Static Method**                           |
| ------------------- | ------------------------------------------- | ------------------------------------------- |
| 👤 Called on        | A **document (record)**                     | The **model (collection/class)**            |
| 🛠 Purpose          | Add functions to **individual documents**   | Add functions to the **model itself**       |
| 📍 Where to use     | `schema.methods.methodName = function() {}` | `schema.statics.methodName = function() {}` |
| 📌 Example use case | Check if a user is adult (`user.isAdult()`) | Find all adults (`User.findAdults()`)       |




---

### ❓ **Question:**

Can I only use schema methods when reading data from the schema, like creating a JWT token or validating a password? Can't I use them while writing to the schema, like encrypting the password before saving it to the database?

---

### ✅ **Answer:**

Schema methods are meant to be used on documents that already exist — for example, when you're reading data or working with a document after fetching or creating it. They do **not** automatically run during the save process.

If you want to **encrypt a password before saving it to the database**, you should use **Mongoose middleware** (like `pre('save')`) instead of schema methods. Middleware allows you to modify or validate data **before** it's written to the database.

---


#### SCHEMA METHODS :
- Schema methods are custom functions attached to a schema.
- They can only be called on an instance (i.e., a document) of the schema.
- these custom fn are build to perform some task on schema instance data. 
- EXAMPLES :
  - generating token  (JWT or others)
  - validating pass
  - checking user belongs to specific county
  - checking user is abv 18 or not
- `this` keyword is used to point the instance of schema
- use function () {} beacuse `this` keyword only work in this fn type
- Schema methods are always user-defined.

#### SCHEMA STATICS : 
- Schema statics are functions you define on a Mongoose schema that are called on the Model itself — not on individual documents (instances).
- They are used for operations that involve querying or working with multiple documents, or that don't need access to a specific document's data.
- Schema statics can be either built-in or user-defined.

#### SCHEMA METHODS VS SCHEMA STATICS :

| Feature       | Schema Methods                      | Schema Statics                   |
| ------------- | ----------------------------------- | -------------------------------- |
| Called on     | Document instance (`user`)          | Model (`User`)                   |
| Use case      | Operate on a single document's data | Operate on the entire collection |
| Example usage | `user.isAdult()`                    | `User.findByEmail(email)`        |

- here, isAdult( ) is schema methods & findByEmail( ) is schema statics


---

# API VS ENDPOINTS :

  **API :**
  - When we talk about an API, we're referring to a group of related operations.
  - For example, when we say "Users API", it includes all operations that can be performed on users — typically based on HTTP methods : 
     
     - | HTTP Method | Full path        | Action             |
       | ----------- | ---------------- | ------------------ |
       | `GET`       | `/api/users`     | Get all users      |
       | `GET`       | `/api/users/:id` | Get one user by ID |
       | `POST`      | `/api/users`     | Create a new user  |
       | `PUT`       | `/api/users/:id` | Update a user      |
       | `DELETE`    | `/api/users/:id` | Delete a user      |

  **ENDPOINTS :**
  - Endpoint = req method + full path
  - Eg :- GET /api/users/:id
  - Each combination (e.g. GET /api/users/:id) is a unique endpoint within the API.
---

# EXPRESS ROUTER :

- In Express.js, Router is a mini application (or sub-application) that handles routes.
- It allows you to organize your code better, especially when your app has many endpoints
- Instead of putting all routes in one file, you can split them into multiple files using express.Router( ).

## Why Use express.Router( )?
- Clean and modular route definitions
- Easier to manage and scale as your app grows
- Helps keep related routes grouped (e.g., all user-related routes in userRoutes.js)
