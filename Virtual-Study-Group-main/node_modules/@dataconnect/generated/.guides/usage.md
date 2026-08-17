# Basic Usage

Always prioritize using a supported framework over using the generated SDK
directly. Supported frameworks simplify the developer experience and help ensure
best practices are followed.





## Advanced Usage
If a user is not using a supported framework, they can use the generated SDK directly.

Here's an example of how to use it with the first 5 operations:

```js
import { createUser, updateUser, deleteUser, getUser, listUsers, createStudyGroup, updateStudyGroup, deleteStudyGroup, getStudyGroup, listStudyGroups } from '@dataconnect/generated';


// Operation CreateUser:  For variables, look at type CreateUserVars in ../index.d.ts
const { data } = await CreateUser(dataConnect, createUserVars);

// Operation UpdateUser:  For variables, look at type UpdateUserVars in ../index.d.ts
const { data } = await UpdateUser(dataConnect, updateUserVars);

// Operation DeleteUser: 
const { data } = await DeleteUser(dataConnect);

// Operation GetUser: 
const { data } = await GetUser(dataConnect);

// Operation ListUsers: 
const { data } = await ListUsers(dataConnect);

// Operation CreateStudyGroup:  For variables, look at type CreateStudyGroupVars in ../index.d.ts
const { data } = await CreateStudyGroup(dataConnect, createStudyGroupVars);

// Operation UpdateStudyGroup:  For variables, look at type UpdateStudyGroupVars in ../index.d.ts
const { data } = await UpdateStudyGroup(dataConnect, updateStudyGroupVars);

// Operation DeleteStudyGroup:  For variables, look at type DeleteStudyGroupVars in ../index.d.ts
const { data } = await DeleteStudyGroup(dataConnect, deleteStudyGroupVars);

// Operation GetStudyGroup:  For variables, look at type GetStudyGroupVars in ../index.d.ts
const { data } = await GetStudyGroup(dataConnect, getStudyGroupVars);

// Operation ListStudyGroups: 
const { data } = await ListStudyGroups(dataConnect);


```