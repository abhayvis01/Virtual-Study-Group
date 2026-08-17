# Generated TypeScript README
This README will guide you through the process of using the generated JavaScript SDK package for the connector `example`. It will also provide examples on how to use your generated SDK to call your Data Connect queries and mutations.

***NOTE:** This README is generated alongside the generated SDK. If you make changes to this file, they will be overwritten when the SDK is regenerated.*

# Table of Contents
- [**Overview**](#generated-javascript-readme)
- [**Accessing the connector**](#accessing-the-connector)
  - [*Connecting to the local Emulator*](#connecting-to-the-local-emulator)
- [**Queries**](#queries)
  - [*GetUser*](#getuser)
  - [*ListUsers*](#listusers)
  - [*GetStudyGroup*](#getstudygroup)
  - [*ListStudyGroups*](#liststudygroups)
  - [*ListGroupMembers*](#listgroupmembers)
  - [*GetResource*](#getresource)
  - [*ListResources*](#listresources)
  - [*GetSession*](#getsession)
  - [*ListMySessions*](#listmysessions)
  - [*GetVideoCall*](#getvideocall)
  - [*ListVideoCalls*](#listvideocalls)
  - [*ListCallParticipants*](#listcallparticipants)
- [**Mutations**](#mutations)
  - [*CreateUser*](#createuser)
  - [*UpdateUser*](#updateuser)
  - [*DeleteUser*](#deleteuser)
  - [*CreateStudyGroup*](#createstudygroup)
  - [*UpdateStudyGroup*](#updatestudygroup)
  - [*DeleteStudyGroup*](#deletestudygroup)
  - [*JoinGroup*](#joingroup)
  - [*LeaveGroup*](#leavegroup)
  - [*CreateResource*](#createresource)
  - [*UpdateResource*](#updateresource)
  - [*DeleteResource*](#deleteresource)
  - [*CreateSession*](#createsession)
  - [*UpdateSession*](#updatesession)
  - [*DeleteSession*](#deletesession)
  - [*CreateVideoCall*](#createvideocall)
  - [*UpdateVideoCall*](#updatevideocall)
  - [*DeleteVideoCall*](#deletevideocall)
  - [*JoinCall*](#joincall)
  - [*LeaveCall*](#leavecall)

# Accessing the connector
A connector is a collection of Queries and Mutations. One SDK is generated for each connector - this SDK is generated for the connector `example`. You can find more information about connectors in the [Data Connect documentation](https://firebase.google.com/docs/data-connect#how-does).

You can use this generated SDK by importing from the package `@dataconnect/generated` as shown below. Both CommonJS and ESM imports are supported.

You can also follow the instructions from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#set-client).

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig } from '@dataconnect/generated';

const dataConnect = getDataConnect(connectorConfig);
```

## Connecting to the local Emulator
By default, the connector will connect to the production service.

To connect to the emulator, you can use the following code.
You can also follow the emulator instructions from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#instrument-clients).

```typescript
import { connectDataConnectEmulator, getDataConnect } from 'firebase/data-connect';
import { connectorConfig } from '@dataconnect/generated';

const dataConnect = getDataConnect(connectorConfig);
connectDataConnectEmulator(dataConnect, 'localhost', 9399);
```

After it's initialized, you can call your Data Connect [queries](#queries) and [mutations](#mutations) from your generated SDK.

# Queries

There are two ways to execute a Data Connect Query using the generated Web SDK:
- Using a Query Reference function, which returns a `QueryRef`
  - The `QueryRef` can be used as an argument to `executeQuery()`, which will execute the Query and return a `QueryPromise`
- Using an action shortcut function, which returns a `QueryPromise`
  - Calling the action shortcut function will execute the Query and return a `QueryPromise`

The following is true for both the action shortcut function and the `QueryRef` function:
- The `QueryPromise` returned will resolve to the result of the Query once it has finished executing
- If the Query accepts arguments, both the action shortcut function and the `QueryRef` function accept a single argument: an object that contains all the required variables (and the optional variables) for the Query
- Both functions can be called with or without passing in a `DataConnect` instance as an argument. If no `DataConnect` argument is passed in, then the generated SDK will call `getDataConnect(connectorConfig)` behind the scenes for you.

Below are examples of how to use the `example` connector's generated functions to execute each query. You can also follow the examples from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#using-queries).

## GetUser
You can execute the `GetUser` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
getUser(options?: ExecuteQueryOptions): QueryPromise<GetUserData, undefined>;

interface GetUserRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<GetUserData, undefined>;
}
export const getUserRef: GetUserRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
getUser(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<GetUserData, undefined>;

interface GetUserRef {
  ...
  (dc: DataConnect): QueryRef<GetUserData, undefined>;
}
export const getUserRef: GetUserRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the getUserRef:
```typescript
const name = getUserRef.operationName;
console.log(name);
```

### Variables
The `GetUser` query has no variables.
### Return Type
Recall that executing the `GetUser` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `GetUserData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface GetUserData {
  user?: {
    username: string;
    email: string;
    totalHours: number;
  };
}
```
### Using `GetUser`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, getUser } from '@dataconnect/generated';


// Call the `getUser()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await getUser();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await getUser(dataConnect);

console.log(data.user);

// Or, you can use the `Promise` API.
getUser().then((response) => {
  const data = response.data;
  console.log(data.user);
});
```

### Using `GetUser`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, getUserRef } from '@dataconnect/generated';


// Call the `getUserRef()` function to get a reference to the query.
const ref = getUserRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = getUserRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.user);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.user);
});
```

## ListUsers
You can execute the `ListUsers` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listUsers(options?: ExecuteQueryOptions): QueryPromise<ListUsersData, undefined>;

interface ListUsersRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListUsersData, undefined>;
}
export const listUsersRef: ListUsersRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listUsers(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListUsersData, undefined>;

interface ListUsersRef {
  ...
  (dc: DataConnect): QueryRef<ListUsersData, undefined>;
}
export const listUsersRef: ListUsersRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listUsersRef:
```typescript
const name = listUsersRef.operationName;
console.log(name);
```

### Variables
The `ListUsers` query has no variables.
### Return Type
Recall that executing the `ListUsers` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListUsersData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListUsersData {
  users: ({
    username: string;
    totalHours: number;
  })[];
}
```
### Using `ListUsers`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listUsers } from '@dataconnect/generated';


// Call the `listUsers()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listUsers();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listUsers(dataConnect);

console.log(data.users);

// Or, you can use the `Promise` API.
listUsers().then((response) => {
  const data = response.data;
  console.log(data.users);
});
```

### Using `ListUsers`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listUsersRef } from '@dataconnect/generated';


// Call the `listUsersRef()` function to get a reference to the query.
const ref = listUsersRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listUsersRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.users);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.users);
});
```

## GetStudyGroup
You can execute the `GetStudyGroup` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
getStudyGroup(vars: GetStudyGroupVariables, options?: ExecuteQueryOptions): QueryPromise<GetStudyGroupData, GetStudyGroupVariables>;

interface GetStudyGroupRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetStudyGroupVariables): QueryRef<GetStudyGroupData, GetStudyGroupVariables>;
}
export const getStudyGroupRef: GetStudyGroupRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
getStudyGroup(dc: DataConnect, vars: GetStudyGroupVariables, options?: ExecuteQueryOptions): QueryPromise<GetStudyGroupData, GetStudyGroupVariables>;

interface GetStudyGroupRef {
  ...
  (dc: DataConnect, vars: GetStudyGroupVariables): QueryRef<GetStudyGroupData, GetStudyGroupVariables>;
}
export const getStudyGroupRef: GetStudyGroupRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the getStudyGroupRef:
```typescript
const name = getStudyGroupRef.operationName;
console.log(name);
```

### Variables
The `GetStudyGroup` query requires an argument of type `GetStudyGroupVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface GetStudyGroupVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `GetStudyGroup` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `GetStudyGroupData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface GetStudyGroupData {
  studyGroup?: {
    name: string;
    description?: string | null;
  };
}
```
### Using `GetStudyGroup`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, getStudyGroup, GetStudyGroupVariables } from '@dataconnect/generated';

// The `GetStudyGroup` query requires an argument of type `GetStudyGroupVariables`:
const getStudyGroupVars: GetStudyGroupVariables = {
  id: ..., 
};

// Call the `getStudyGroup()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await getStudyGroup(getStudyGroupVars);
// Variables can be defined inline as well.
const { data } = await getStudyGroup({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await getStudyGroup(dataConnect, getStudyGroupVars);

console.log(data.studyGroup);

// Or, you can use the `Promise` API.
getStudyGroup(getStudyGroupVars).then((response) => {
  const data = response.data;
  console.log(data.studyGroup);
});
```

### Using `GetStudyGroup`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, getStudyGroupRef, GetStudyGroupVariables } from '@dataconnect/generated';

// The `GetStudyGroup` query requires an argument of type `GetStudyGroupVariables`:
const getStudyGroupVars: GetStudyGroupVariables = {
  id: ..., 
};

// Call the `getStudyGroupRef()` function to get a reference to the query.
const ref = getStudyGroupRef(getStudyGroupVars);
// Variables can be defined inline as well.
const ref = getStudyGroupRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = getStudyGroupRef(dataConnect, getStudyGroupVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.studyGroup);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.studyGroup);
});
```

## ListStudyGroups
You can execute the `ListStudyGroups` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listStudyGroups(options?: ExecuteQueryOptions): QueryPromise<ListStudyGroupsData, undefined>;

interface ListStudyGroupsRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListStudyGroupsData, undefined>;
}
export const listStudyGroupsRef: ListStudyGroupsRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listStudyGroups(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListStudyGroupsData, undefined>;

interface ListStudyGroupsRef {
  ...
  (dc: DataConnect): QueryRef<ListStudyGroupsData, undefined>;
}
export const listStudyGroupsRef: ListStudyGroupsRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listStudyGroupsRef:
```typescript
const name = listStudyGroupsRef.operationName;
console.log(name);
```

### Variables
The `ListStudyGroups` query has no variables.
### Return Type
Recall that executing the `ListStudyGroups` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListStudyGroupsData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListStudyGroupsData {
  studyGroups: ({
    name: string;
  })[];
}
```
### Using `ListStudyGroups`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listStudyGroups } from '@dataconnect/generated';


// Call the `listStudyGroups()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listStudyGroups();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listStudyGroups(dataConnect);

console.log(data.studyGroups);

// Or, you can use the `Promise` API.
listStudyGroups().then((response) => {
  const data = response.data;
  console.log(data.studyGroups);
});
```

### Using `ListStudyGroups`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listStudyGroupsRef } from '@dataconnect/generated';


// Call the `listStudyGroupsRef()` function to get a reference to the query.
const ref = listStudyGroupsRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listStudyGroupsRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.studyGroups);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.studyGroups);
});
```

## ListGroupMembers
You can execute the `ListGroupMembers` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listGroupMembers(vars: ListGroupMembersVariables, options?: ExecuteQueryOptions): QueryPromise<ListGroupMembersData, ListGroupMembersVariables>;

interface ListGroupMembersRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: ListGroupMembersVariables): QueryRef<ListGroupMembersData, ListGroupMembersVariables>;
}
export const listGroupMembersRef: ListGroupMembersRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listGroupMembers(dc: DataConnect, vars: ListGroupMembersVariables, options?: ExecuteQueryOptions): QueryPromise<ListGroupMembersData, ListGroupMembersVariables>;

interface ListGroupMembersRef {
  ...
  (dc: DataConnect, vars: ListGroupMembersVariables): QueryRef<ListGroupMembersData, ListGroupMembersVariables>;
}
export const listGroupMembersRef: ListGroupMembersRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listGroupMembersRef:
```typescript
const name = listGroupMembersRef.operationName;
console.log(name);
```

### Variables
The `ListGroupMembers` query requires an argument of type `ListGroupMembersVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface ListGroupMembersVariables {
  groupId: UUIDString;
}
```
### Return Type
Recall that executing the `ListGroupMembers` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListGroupMembersData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListGroupMembersData {
  groupMembers: ({
    user: {
      username: string;
    };
  })[];
}
```
### Using `ListGroupMembers`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listGroupMembers, ListGroupMembersVariables } from '@dataconnect/generated';

// The `ListGroupMembers` query requires an argument of type `ListGroupMembersVariables`:
const listGroupMembersVars: ListGroupMembersVariables = {
  groupId: ..., 
};

// Call the `listGroupMembers()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listGroupMembers(listGroupMembersVars);
// Variables can be defined inline as well.
const { data } = await listGroupMembers({ groupId: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listGroupMembers(dataConnect, listGroupMembersVars);

console.log(data.groupMembers);

// Or, you can use the `Promise` API.
listGroupMembers(listGroupMembersVars).then((response) => {
  const data = response.data;
  console.log(data.groupMembers);
});
```

### Using `ListGroupMembers`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listGroupMembersRef, ListGroupMembersVariables } from '@dataconnect/generated';

// The `ListGroupMembers` query requires an argument of type `ListGroupMembersVariables`:
const listGroupMembersVars: ListGroupMembersVariables = {
  groupId: ..., 
};

// Call the `listGroupMembersRef()` function to get a reference to the query.
const ref = listGroupMembersRef(listGroupMembersVars);
// Variables can be defined inline as well.
const ref = listGroupMembersRef({ groupId: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listGroupMembersRef(dataConnect, listGroupMembersVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.groupMembers);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.groupMembers);
});
```

## GetResource
You can execute the `GetResource` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
getResource(vars: GetResourceVariables, options?: ExecuteQueryOptions): QueryPromise<GetResourceData, GetResourceVariables>;

interface GetResourceRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetResourceVariables): QueryRef<GetResourceData, GetResourceVariables>;
}
export const getResourceRef: GetResourceRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
getResource(dc: DataConnect, vars: GetResourceVariables, options?: ExecuteQueryOptions): QueryPromise<GetResourceData, GetResourceVariables>;

interface GetResourceRef {
  ...
  (dc: DataConnect, vars: GetResourceVariables): QueryRef<GetResourceData, GetResourceVariables>;
}
export const getResourceRef: GetResourceRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the getResourceRef:
```typescript
const name = getResourceRef.operationName;
console.log(name);
```

### Variables
The `GetResource` query requires an argument of type `GetResourceVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface GetResourceVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `GetResource` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `GetResourceData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface GetResourceData {
  resource?: {
    title: string;
    fileUrl: string;
  };
}
```
### Using `GetResource`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, getResource, GetResourceVariables } from '@dataconnect/generated';

// The `GetResource` query requires an argument of type `GetResourceVariables`:
const getResourceVars: GetResourceVariables = {
  id: ..., 
};

// Call the `getResource()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await getResource(getResourceVars);
// Variables can be defined inline as well.
const { data } = await getResource({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await getResource(dataConnect, getResourceVars);

console.log(data.resource);

// Or, you can use the `Promise` API.
getResource(getResourceVars).then((response) => {
  const data = response.data;
  console.log(data.resource);
});
```

### Using `GetResource`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, getResourceRef, GetResourceVariables } from '@dataconnect/generated';

// The `GetResource` query requires an argument of type `GetResourceVariables`:
const getResourceVars: GetResourceVariables = {
  id: ..., 
};

// Call the `getResourceRef()` function to get a reference to the query.
const ref = getResourceRef(getResourceVars);
// Variables can be defined inline as well.
const ref = getResourceRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = getResourceRef(dataConnect, getResourceVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.resource);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.resource);
});
```

## ListResources
You can execute the `ListResources` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listResources(vars: ListResourcesVariables, options?: ExecuteQueryOptions): QueryPromise<ListResourcesData, ListResourcesVariables>;

interface ListResourcesRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: ListResourcesVariables): QueryRef<ListResourcesData, ListResourcesVariables>;
}
export const listResourcesRef: ListResourcesRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listResources(dc: DataConnect, vars: ListResourcesVariables, options?: ExecuteQueryOptions): QueryPromise<ListResourcesData, ListResourcesVariables>;

interface ListResourcesRef {
  ...
  (dc: DataConnect, vars: ListResourcesVariables): QueryRef<ListResourcesData, ListResourcesVariables>;
}
export const listResourcesRef: ListResourcesRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listResourcesRef:
```typescript
const name = listResourcesRef.operationName;
console.log(name);
```

### Variables
The `ListResources` query requires an argument of type `ListResourcesVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface ListResourcesVariables {
  groupId: UUIDString;
}
```
### Return Type
Recall that executing the `ListResources` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListResourcesData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListResourcesData {
  resources: ({
    title: string;
    type: string;
  })[];
}
```
### Using `ListResources`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listResources, ListResourcesVariables } from '@dataconnect/generated';

// The `ListResources` query requires an argument of type `ListResourcesVariables`:
const listResourcesVars: ListResourcesVariables = {
  groupId: ..., 
};

// Call the `listResources()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listResources(listResourcesVars);
// Variables can be defined inline as well.
const { data } = await listResources({ groupId: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listResources(dataConnect, listResourcesVars);

console.log(data.resources);

// Or, you can use the `Promise` API.
listResources(listResourcesVars).then((response) => {
  const data = response.data;
  console.log(data.resources);
});
```

### Using `ListResources`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listResourcesRef, ListResourcesVariables } from '@dataconnect/generated';

// The `ListResources` query requires an argument of type `ListResourcesVariables`:
const listResourcesVars: ListResourcesVariables = {
  groupId: ..., 
};

// Call the `listResourcesRef()` function to get a reference to the query.
const ref = listResourcesRef(listResourcesVars);
// Variables can be defined inline as well.
const ref = listResourcesRef({ groupId: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listResourcesRef(dataConnect, listResourcesVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.resources);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.resources);
});
```

## GetSession
You can execute the `GetSession` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
getSession(vars: GetSessionVariables, options?: ExecuteQueryOptions): QueryPromise<GetSessionData, GetSessionVariables>;

interface GetSessionRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetSessionVariables): QueryRef<GetSessionData, GetSessionVariables>;
}
export const getSessionRef: GetSessionRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
getSession(dc: DataConnect, vars: GetSessionVariables, options?: ExecuteQueryOptions): QueryPromise<GetSessionData, GetSessionVariables>;

interface GetSessionRef {
  ...
  (dc: DataConnect, vars: GetSessionVariables): QueryRef<GetSessionData, GetSessionVariables>;
}
export const getSessionRef: GetSessionRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the getSessionRef:
```typescript
const name = getSessionRef.operationName;
console.log(name);
```

### Variables
The `GetSession` query requires an argument of type `GetSessionVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface GetSessionVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `GetSession` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `GetSessionData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface GetSessionData {
  session?: {
    topic?: string | null;
    durationMinutes: number;
  };
}
```
### Using `GetSession`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, getSession, GetSessionVariables } from '@dataconnect/generated';

// The `GetSession` query requires an argument of type `GetSessionVariables`:
const getSessionVars: GetSessionVariables = {
  id: ..., 
};

// Call the `getSession()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await getSession(getSessionVars);
// Variables can be defined inline as well.
const { data } = await getSession({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await getSession(dataConnect, getSessionVars);

console.log(data.session);

// Or, you can use the `Promise` API.
getSession(getSessionVars).then((response) => {
  const data = response.data;
  console.log(data.session);
});
```

### Using `GetSession`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, getSessionRef, GetSessionVariables } from '@dataconnect/generated';

// The `GetSession` query requires an argument of type `GetSessionVariables`:
const getSessionVars: GetSessionVariables = {
  id: ..., 
};

// Call the `getSessionRef()` function to get a reference to the query.
const ref = getSessionRef(getSessionVars);
// Variables can be defined inline as well.
const ref = getSessionRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = getSessionRef(dataConnect, getSessionVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.session);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.session);
});
```

## ListMySessions
You can execute the `ListMySessions` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listMySessions(options?: ExecuteQueryOptions): QueryPromise<ListMySessionsData, undefined>;

interface ListMySessionsRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListMySessionsData, undefined>;
}
export const listMySessionsRef: ListMySessionsRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listMySessions(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListMySessionsData, undefined>;

interface ListMySessionsRef {
  ...
  (dc: DataConnect): QueryRef<ListMySessionsData, undefined>;
}
export const listMySessionsRef: ListMySessionsRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listMySessionsRef:
```typescript
const name = listMySessionsRef.operationName;
console.log(name);
```

### Variables
The `ListMySessions` query has no variables.
### Return Type
Recall that executing the `ListMySessions` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListMySessionsData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListMySessionsData {
  sessions: ({
    topic?: string | null;
    durationMinutes: number;
  })[];
}
```
### Using `ListMySessions`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listMySessions } from '@dataconnect/generated';


// Call the `listMySessions()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listMySessions();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listMySessions(dataConnect);

console.log(data.sessions);

// Or, you can use the `Promise` API.
listMySessions().then((response) => {
  const data = response.data;
  console.log(data.sessions);
});
```

### Using `ListMySessions`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listMySessionsRef } from '@dataconnect/generated';


// Call the `listMySessionsRef()` function to get a reference to the query.
const ref = listMySessionsRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listMySessionsRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.sessions);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.sessions);
});
```

## GetVideoCall
You can execute the `GetVideoCall` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
getVideoCall(vars: GetVideoCallVariables, options?: ExecuteQueryOptions): QueryPromise<GetVideoCallData, GetVideoCallVariables>;

interface GetVideoCallRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetVideoCallVariables): QueryRef<GetVideoCallData, GetVideoCallVariables>;
}
export const getVideoCallRef: GetVideoCallRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
getVideoCall(dc: DataConnect, vars: GetVideoCallVariables, options?: ExecuteQueryOptions): QueryPromise<GetVideoCallData, GetVideoCallVariables>;

interface GetVideoCallRef {
  ...
  (dc: DataConnect, vars: GetVideoCallVariables): QueryRef<GetVideoCallData, GetVideoCallVariables>;
}
export const getVideoCallRef: GetVideoCallRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the getVideoCallRef:
```typescript
const name = getVideoCallRef.operationName;
console.log(name);
```

### Variables
The `GetVideoCall` query requires an argument of type `GetVideoCallVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface GetVideoCallVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `GetVideoCall` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `GetVideoCallData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface GetVideoCallData {
  videoCall?: {
    isActive: boolean;
    startTime?: TimestampString | null;
  };
}
```
### Using `GetVideoCall`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, getVideoCall, GetVideoCallVariables } from '@dataconnect/generated';

// The `GetVideoCall` query requires an argument of type `GetVideoCallVariables`:
const getVideoCallVars: GetVideoCallVariables = {
  id: ..., 
};

// Call the `getVideoCall()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await getVideoCall(getVideoCallVars);
// Variables can be defined inline as well.
const { data } = await getVideoCall({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await getVideoCall(dataConnect, getVideoCallVars);

console.log(data.videoCall);

// Or, you can use the `Promise` API.
getVideoCall(getVideoCallVars).then((response) => {
  const data = response.data;
  console.log(data.videoCall);
});
```

### Using `GetVideoCall`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, getVideoCallRef, GetVideoCallVariables } from '@dataconnect/generated';

// The `GetVideoCall` query requires an argument of type `GetVideoCallVariables`:
const getVideoCallVars: GetVideoCallVariables = {
  id: ..., 
};

// Call the `getVideoCallRef()` function to get a reference to the query.
const ref = getVideoCallRef(getVideoCallVars);
// Variables can be defined inline as well.
const ref = getVideoCallRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = getVideoCallRef(dataConnect, getVideoCallVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.videoCall);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.videoCall);
});
```

## ListVideoCalls
You can execute the `ListVideoCalls` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listVideoCalls(vars: ListVideoCallsVariables, options?: ExecuteQueryOptions): QueryPromise<ListVideoCallsData, ListVideoCallsVariables>;

interface ListVideoCallsRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: ListVideoCallsVariables): QueryRef<ListVideoCallsData, ListVideoCallsVariables>;
}
export const listVideoCallsRef: ListVideoCallsRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listVideoCalls(dc: DataConnect, vars: ListVideoCallsVariables, options?: ExecuteQueryOptions): QueryPromise<ListVideoCallsData, ListVideoCallsVariables>;

interface ListVideoCallsRef {
  ...
  (dc: DataConnect, vars: ListVideoCallsVariables): QueryRef<ListVideoCallsData, ListVideoCallsVariables>;
}
export const listVideoCallsRef: ListVideoCallsRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listVideoCallsRef:
```typescript
const name = listVideoCallsRef.operationName;
console.log(name);
```

### Variables
The `ListVideoCalls` query requires an argument of type `ListVideoCallsVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface ListVideoCallsVariables {
  groupId: UUIDString;
}
```
### Return Type
Recall that executing the `ListVideoCalls` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListVideoCallsData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListVideoCallsData {
  videoCalls: ({
    isActive: boolean;
  })[];
}
```
### Using `ListVideoCalls`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listVideoCalls, ListVideoCallsVariables } from '@dataconnect/generated';

// The `ListVideoCalls` query requires an argument of type `ListVideoCallsVariables`:
const listVideoCallsVars: ListVideoCallsVariables = {
  groupId: ..., 
};

// Call the `listVideoCalls()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listVideoCalls(listVideoCallsVars);
// Variables can be defined inline as well.
const { data } = await listVideoCalls({ groupId: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listVideoCalls(dataConnect, listVideoCallsVars);

console.log(data.videoCalls);

// Or, you can use the `Promise` API.
listVideoCalls(listVideoCallsVars).then((response) => {
  const data = response.data;
  console.log(data.videoCalls);
});
```

### Using `ListVideoCalls`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listVideoCallsRef, ListVideoCallsVariables } from '@dataconnect/generated';

// The `ListVideoCalls` query requires an argument of type `ListVideoCallsVariables`:
const listVideoCallsVars: ListVideoCallsVariables = {
  groupId: ..., 
};

// Call the `listVideoCallsRef()` function to get a reference to the query.
const ref = listVideoCallsRef(listVideoCallsVars);
// Variables can be defined inline as well.
const ref = listVideoCallsRef({ groupId: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listVideoCallsRef(dataConnect, listVideoCallsVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.videoCalls);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.videoCalls);
});
```

## ListCallParticipants
You can execute the `ListCallParticipants` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
listCallParticipants(vars: ListCallParticipantsVariables, options?: ExecuteQueryOptions): QueryPromise<ListCallParticipantsData, ListCallParticipantsVariables>;

interface ListCallParticipantsRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: ListCallParticipantsVariables): QueryRef<ListCallParticipantsData, ListCallParticipantsVariables>;
}
export const listCallParticipantsRef: ListCallParticipantsRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
listCallParticipants(dc: DataConnect, vars: ListCallParticipantsVariables, options?: ExecuteQueryOptions): QueryPromise<ListCallParticipantsData, ListCallParticipantsVariables>;

interface ListCallParticipantsRef {
  ...
  (dc: DataConnect, vars: ListCallParticipantsVariables): QueryRef<ListCallParticipantsData, ListCallParticipantsVariables>;
}
export const listCallParticipantsRef: ListCallParticipantsRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the listCallParticipantsRef:
```typescript
const name = listCallParticipantsRef.operationName;
console.log(name);
```

### Variables
The `ListCallParticipants` query requires an argument of type `ListCallParticipantsVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface ListCallParticipantsVariables {
  callId: UUIDString;
}
```
### Return Type
Recall that executing the `ListCallParticipants` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `ListCallParticipantsData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface ListCallParticipantsData {
  callParticipants: ({
    user: {
      username: string;
    };
  })[];
}
```
### Using `ListCallParticipants`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, listCallParticipants, ListCallParticipantsVariables } from '@dataconnect/generated';

// The `ListCallParticipants` query requires an argument of type `ListCallParticipantsVariables`:
const listCallParticipantsVars: ListCallParticipantsVariables = {
  callId: ..., 
};

// Call the `listCallParticipants()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await listCallParticipants(listCallParticipantsVars);
// Variables can be defined inline as well.
const { data } = await listCallParticipants({ callId: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await listCallParticipants(dataConnect, listCallParticipantsVars);

console.log(data.callParticipants);

// Or, you can use the `Promise` API.
listCallParticipants(listCallParticipantsVars).then((response) => {
  const data = response.data;
  console.log(data.callParticipants);
});
```

### Using `ListCallParticipants`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, listCallParticipantsRef, ListCallParticipantsVariables } from '@dataconnect/generated';

// The `ListCallParticipants` query requires an argument of type `ListCallParticipantsVariables`:
const listCallParticipantsVars: ListCallParticipantsVariables = {
  callId: ..., 
};

// Call the `listCallParticipantsRef()` function to get a reference to the query.
const ref = listCallParticipantsRef(listCallParticipantsVars);
// Variables can be defined inline as well.
const ref = listCallParticipantsRef({ callId: ..., });

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = listCallParticipantsRef(dataConnect, listCallParticipantsVars);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.callParticipants);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.callParticipants);
});
```

# Mutations

There are two ways to execute a Data Connect Mutation using the generated Web SDK:
- Using a Mutation Reference function, which returns a `MutationRef`
  - The `MutationRef` can be used as an argument to `executeMutation()`, which will execute the Mutation and return a `MutationPromise`
- Using an action shortcut function, which returns a `MutationPromise`
  - Calling the action shortcut function will execute the Mutation and return a `MutationPromise`

The following is true for both the action shortcut function and the `MutationRef` function:
- The `MutationPromise` returned will resolve to the result of the Mutation once it has finished executing
- If the Mutation accepts arguments, both the action shortcut function and the `MutationRef` function accept a single argument: an object that contains all the required variables (and the optional variables) for the Mutation
- Both functions can be called with or without passing in a `DataConnect` instance as an argument. If no `DataConnect` argument is passed in, then the generated SDK will call `getDataConnect(connectorConfig)` behind the scenes for you.

Below are examples of how to use the `example` connector's generated functions to execute each mutation. You can also follow the examples from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#using-mutations).

## CreateUser
You can execute the `CreateUser` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createUser(vars: CreateUserVariables): MutationPromise<CreateUserData, CreateUserVariables>;

interface CreateUserRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateUserVariables): MutationRef<CreateUserData, CreateUserVariables>;
}
export const createUserRef: CreateUserRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createUser(dc: DataConnect, vars: CreateUserVariables): MutationPromise<CreateUserData, CreateUserVariables>;

interface CreateUserRef {
  ...
  (dc: DataConnect, vars: CreateUserVariables): MutationRef<CreateUserData, CreateUserVariables>;
}
export const createUserRef: CreateUserRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createUserRef:
```typescript
const name = createUserRef.operationName;
console.log(name);
```

### Variables
The `CreateUser` mutation requires an argument of type `CreateUserVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateUserVariables {
  username: string;
  email: string;
  totalHours: number;
}
```
### Return Type
Recall that executing the `CreateUser` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateUserData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateUserData {
  user_insert: User_Key;
}
```
### Using `CreateUser`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createUser, CreateUserVariables } from '@dataconnect/generated';

// The `CreateUser` mutation requires an argument of type `CreateUserVariables`:
const createUserVars: CreateUserVariables = {
  username: ..., 
  email: ..., 
  totalHours: ..., 
};

// Call the `createUser()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createUser(createUserVars);
// Variables can be defined inline as well.
const { data } = await createUser({ username: ..., email: ..., totalHours: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createUser(dataConnect, createUserVars);

console.log(data.user_insert);

// Or, you can use the `Promise` API.
createUser(createUserVars).then((response) => {
  const data = response.data;
  console.log(data.user_insert);
});
```

### Using `CreateUser`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createUserRef, CreateUserVariables } from '@dataconnect/generated';

// The `CreateUser` mutation requires an argument of type `CreateUserVariables`:
const createUserVars: CreateUserVariables = {
  username: ..., 
  email: ..., 
  totalHours: ..., 
};

// Call the `createUserRef()` function to get a reference to the mutation.
const ref = createUserRef(createUserVars);
// Variables can be defined inline as well.
const ref = createUserRef({ username: ..., email: ..., totalHours: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createUserRef(dataConnect, createUserVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.user_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.user_insert);
});
```

## UpdateUser
You can execute the `UpdateUser` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
updateUser(vars?: UpdateUserVariables): MutationPromise<UpdateUserData, UpdateUserVariables>;

interface UpdateUserRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars?: UpdateUserVariables): MutationRef<UpdateUserData, UpdateUserVariables>;
}
export const updateUserRef: UpdateUserRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
updateUser(dc: DataConnect, vars?: UpdateUserVariables): MutationPromise<UpdateUserData, UpdateUserVariables>;

interface UpdateUserRef {
  ...
  (dc: DataConnect, vars?: UpdateUserVariables): MutationRef<UpdateUserData, UpdateUserVariables>;
}
export const updateUserRef: UpdateUserRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the updateUserRef:
```typescript
const name = updateUserRef.operationName;
console.log(name);
```

### Variables
The `UpdateUser` mutation has an optional argument of type `UpdateUserVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface UpdateUserVariables {
  username?: string | null;
}
```
### Return Type
Recall that executing the `UpdateUser` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `UpdateUserData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface UpdateUserData {
  user_update?: User_Key | null;
}
```
### Using `UpdateUser`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, updateUser, UpdateUserVariables } from '@dataconnect/generated';

// The `UpdateUser` mutation has an optional argument of type `UpdateUserVariables`:
const updateUserVars: UpdateUserVariables = {
  username: ..., // optional
};

// Call the `updateUser()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await updateUser(updateUserVars);
// Variables can be defined inline as well.
const { data } = await updateUser({ username: ..., });
// Since all variables are optional for this mutation, you can omit the `UpdateUserVariables` argument.
const { data } = await updateUser();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await updateUser(dataConnect, updateUserVars);

console.log(data.user_update);

// Or, you can use the `Promise` API.
updateUser(updateUserVars).then((response) => {
  const data = response.data;
  console.log(data.user_update);
});
```

### Using `UpdateUser`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, updateUserRef, UpdateUserVariables } from '@dataconnect/generated';

// The `UpdateUser` mutation has an optional argument of type `UpdateUserVariables`:
const updateUserVars: UpdateUserVariables = {
  username: ..., // optional
};

// Call the `updateUserRef()` function to get a reference to the mutation.
const ref = updateUserRef(updateUserVars);
// Variables can be defined inline as well.
const ref = updateUserRef({ username: ..., });
// Since all variables are optional for this mutation, you can omit the `UpdateUserVariables` argument.
const ref = updateUserRef();

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = updateUserRef(dataConnect, updateUserVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.user_update);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.user_update);
});
```

## DeleteUser
You can execute the `DeleteUser` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
deleteUser(): MutationPromise<DeleteUserData, undefined>;

interface DeleteUserRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): MutationRef<DeleteUserData, undefined>;
}
export const deleteUserRef: DeleteUserRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
deleteUser(dc: DataConnect): MutationPromise<DeleteUserData, undefined>;

interface DeleteUserRef {
  ...
  (dc: DataConnect): MutationRef<DeleteUserData, undefined>;
}
export const deleteUserRef: DeleteUserRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the deleteUserRef:
```typescript
const name = deleteUserRef.operationName;
console.log(name);
```

### Variables
The `DeleteUser` mutation has no variables.
### Return Type
Recall that executing the `DeleteUser` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `DeleteUserData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface DeleteUserData {
  user_delete?: User_Key | null;
}
```
### Using `DeleteUser`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, deleteUser } from '@dataconnect/generated';


// Call the `deleteUser()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await deleteUser();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await deleteUser(dataConnect);

console.log(data.user_delete);

// Or, you can use the `Promise` API.
deleteUser().then((response) => {
  const data = response.data;
  console.log(data.user_delete);
});
```

### Using `DeleteUser`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, deleteUserRef } from '@dataconnect/generated';


// Call the `deleteUserRef()` function to get a reference to the mutation.
const ref = deleteUserRef();

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = deleteUserRef(dataConnect);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.user_delete);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.user_delete);
});
```

## CreateStudyGroup
You can execute the `CreateStudyGroup` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createStudyGroup(vars: CreateStudyGroupVariables): MutationPromise<CreateStudyGroupData, CreateStudyGroupVariables>;

interface CreateStudyGroupRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateStudyGroupVariables): MutationRef<CreateStudyGroupData, CreateStudyGroupVariables>;
}
export const createStudyGroupRef: CreateStudyGroupRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createStudyGroup(dc: DataConnect, vars: CreateStudyGroupVariables): MutationPromise<CreateStudyGroupData, CreateStudyGroupVariables>;

interface CreateStudyGroupRef {
  ...
  (dc: DataConnect, vars: CreateStudyGroupVariables): MutationRef<CreateStudyGroupData, CreateStudyGroupVariables>;
}
export const createStudyGroupRef: CreateStudyGroupRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createStudyGroupRef:
```typescript
const name = createStudyGroupRef.operationName;
console.log(name);
```

### Variables
The `CreateStudyGroup` mutation requires an argument of type `CreateStudyGroupVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateStudyGroupVariables {
  name: string;
  description?: string | null;
}
```
### Return Type
Recall that executing the `CreateStudyGroup` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateStudyGroupData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateStudyGroupData {
  studyGroup_insert: StudyGroup_Key;
}
```
### Using `CreateStudyGroup`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createStudyGroup, CreateStudyGroupVariables } from '@dataconnect/generated';

// The `CreateStudyGroup` mutation requires an argument of type `CreateStudyGroupVariables`:
const createStudyGroupVars: CreateStudyGroupVariables = {
  name: ..., 
  description: ..., // optional
};

// Call the `createStudyGroup()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createStudyGroup(createStudyGroupVars);
// Variables can be defined inline as well.
const { data } = await createStudyGroup({ name: ..., description: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createStudyGroup(dataConnect, createStudyGroupVars);

console.log(data.studyGroup_insert);

// Or, you can use the `Promise` API.
createStudyGroup(createStudyGroupVars).then((response) => {
  const data = response.data;
  console.log(data.studyGroup_insert);
});
```

### Using `CreateStudyGroup`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createStudyGroupRef, CreateStudyGroupVariables } from '@dataconnect/generated';

// The `CreateStudyGroup` mutation requires an argument of type `CreateStudyGroupVariables`:
const createStudyGroupVars: CreateStudyGroupVariables = {
  name: ..., 
  description: ..., // optional
};

// Call the `createStudyGroupRef()` function to get a reference to the mutation.
const ref = createStudyGroupRef(createStudyGroupVars);
// Variables can be defined inline as well.
const ref = createStudyGroupRef({ name: ..., description: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createStudyGroupRef(dataConnect, createStudyGroupVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.studyGroup_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.studyGroup_insert);
});
```

## UpdateStudyGroup
You can execute the `UpdateStudyGroup` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
updateStudyGroup(vars: UpdateStudyGroupVariables): MutationPromise<UpdateStudyGroupData, UpdateStudyGroupVariables>;

interface UpdateStudyGroupRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateStudyGroupVariables): MutationRef<UpdateStudyGroupData, UpdateStudyGroupVariables>;
}
export const updateStudyGroupRef: UpdateStudyGroupRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
updateStudyGroup(dc: DataConnect, vars: UpdateStudyGroupVariables): MutationPromise<UpdateStudyGroupData, UpdateStudyGroupVariables>;

interface UpdateStudyGroupRef {
  ...
  (dc: DataConnect, vars: UpdateStudyGroupVariables): MutationRef<UpdateStudyGroupData, UpdateStudyGroupVariables>;
}
export const updateStudyGroupRef: UpdateStudyGroupRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the updateStudyGroupRef:
```typescript
const name = updateStudyGroupRef.operationName;
console.log(name);
```

### Variables
The `UpdateStudyGroup` mutation requires an argument of type `UpdateStudyGroupVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface UpdateStudyGroupVariables {
  id: UUIDString;
  name?: string | null;
}
```
### Return Type
Recall that executing the `UpdateStudyGroup` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `UpdateStudyGroupData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface UpdateStudyGroupData {
  studyGroup_update?: StudyGroup_Key | null;
}
```
### Using `UpdateStudyGroup`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, updateStudyGroup, UpdateStudyGroupVariables } from '@dataconnect/generated';

// The `UpdateStudyGroup` mutation requires an argument of type `UpdateStudyGroupVariables`:
const updateStudyGroupVars: UpdateStudyGroupVariables = {
  id: ..., 
  name: ..., // optional
};

// Call the `updateStudyGroup()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await updateStudyGroup(updateStudyGroupVars);
// Variables can be defined inline as well.
const { data } = await updateStudyGroup({ id: ..., name: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await updateStudyGroup(dataConnect, updateStudyGroupVars);

console.log(data.studyGroup_update);

// Or, you can use the `Promise` API.
updateStudyGroup(updateStudyGroupVars).then((response) => {
  const data = response.data;
  console.log(data.studyGroup_update);
});
```

### Using `UpdateStudyGroup`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, updateStudyGroupRef, UpdateStudyGroupVariables } from '@dataconnect/generated';

// The `UpdateStudyGroup` mutation requires an argument of type `UpdateStudyGroupVariables`:
const updateStudyGroupVars: UpdateStudyGroupVariables = {
  id: ..., 
  name: ..., // optional
};

// Call the `updateStudyGroupRef()` function to get a reference to the mutation.
const ref = updateStudyGroupRef(updateStudyGroupVars);
// Variables can be defined inline as well.
const ref = updateStudyGroupRef({ id: ..., name: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = updateStudyGroupRef(dataConnect, updateStudyGroupVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.studyGroup_update);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.studyGroup_update);
});
```

## DeleteStudyGroup
You can execute the `DeleteStudyGroup` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
deleteStudyGroup(vars: DeleteStudyGroupVariables): MutationPromise<DeleteStudyGroupData, DeleteStudyGroupVariables>;

interface DeleteStudyGroupRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteStudyGroupVariables): MutationRef<DeleteStudyGroupData, DeleteStudyGroupVariables>;
}
export const deleteStudyGroupRef: DeleteStudyGroupRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
deleteStudyGroup(dc: DataConnect, vars: DeleteStudyGroupVariables): MutationPromise<DeleteStudyGroupData, DeleteStudyGroupVariables>;

interface DeleteStudyGroupRef {
  ...
  (dc: DataConnect, vars: DeleteStudyGroupVariables): MutationRef<DeleteStudyGroupData, DeleteStudyGroupVariables>;
}
export const deleteStudyGroupRef: DeleteStudyGroupRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the deleteStudyGroupRef:
```typescript
const name = deleteStudyGroupRef.operationName;
console.log(name);
```

### Variables
The `DeleteStudyGroup` mutation requires an argument of type `DeleteStudyGroupVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface DeleteStudyGroupVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `DeleteStudyGroup` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `DeleteStudyGroupData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface DeleteStudyGroupData {
  studyGroup_delete?: StudyGroup_Key | null;
}
```
### Using `DeleteStudyGroup`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, deleteStudyGroup, DeleteStudyGroupVariables } from '@dataconnect/generated';

// The `DeleteStudyGroup` mutation requires an argument of type `DeleteStudyGroupVariables`:
const deleteStudyGroupVars: DeleteStudyGroupVariables = {
  id: ..., 
};

// Call the `deleteStudyGroup()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await deleteStudyGroup(deleteStudyGroupVars);
// Variables can be defined inline as well.
const { data } = await deleteStudyGroup({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await deleteStudyGroup(dataConnect, deleteStudyGroupVars);

console.log(data.studyGroup_delete);

// Or, you can use the `Promise` API.
deleteStudyGroup(deleteStudyGroupVars).then((response) => {
  const data = response.data;
  console.log(data.studyGroup_delete);
});
```

### Using `DeleteStudyGroup`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, deleteStudyGroupRef, DeleteStudyGroupVariables } from '@dataconnect/generated';

// The `DeleteStudyGroup` mutation requires an argument of type `DeleteStudyGroupVariables`:
const deleteStudyGroupVars: DeleteStudyGroupVariables = {
  id: ..., 
};

// Call the `deleteStudyGroupRef()` function to get a reference to the mutation.
const ref = deleteStudyGroupRef(deleteStudyGroupVars);
// Variables can be defined inline as well.
const ref = deleteStudyGroupRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = deleteStudyGroupRef(dataConnect, deleteStudyGroupVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.studyGroup_delete);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.studyGroup_delete);
});
```

## JoinGroup
You can execute the `JoinGroup` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
joinGroup(vars: JoinGroupVariables): MutationPromise<JoinGroupData, JoinGroupVariables>;

interface JoinGroupRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: JoinGroupVariables): MutationRef<JoinGroupData, JoinGroupVariables>;
}
export const joinGroupRef: JoinGroupRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
joinGroup(dc: DataConnect, vars: JoinGroupVariables): MutationPromise<JoinGroupData, JoinGroupVariables>;

interface JoinGroupRef {
  ...
  (dc: DataConnect, vars: JoinGroupVariables): MutationRef<JoinGroupData, JoinGroupVariables>;
}
export const joinGroupRef: JoinGroupRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the joinGroupRef:
```typescript
const name = joinGroupRef.operationName;
console.log(name);
```

### Variables
The `JoinGroup` mutation requires an argument of type `JoinGroupVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface JoinGroupVariables {
  groupId: UUIDString;
}
```
### Return Type
Recall that executing the `JoinGroup` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `JoinGroupData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface JoinGroupData {
  groupMember_insert: GroupMember_Key;
}
```
### Using `JoinGroup`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, joinGroup, JoinGroupVariables } from '@dataconnect/generated';

// The `JoinGroup` mutation requires an argument of type `JoinGroupVariables`:
const joinGroupVars: JoinGroupVariables = {
  groupId: ..., 
};

// Call the `joinGroup()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await joinGroup(joinGroupVars);
// Variables can be defined inline as well.
const { data } = await joinGroup({ groupId: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await joinGroup(dataConnect, joinGroupVars);

console.log(data.groupMember_insert);

// Or, you can use the `Promise` API.
joinGroup(joinGroupVars).then((response) => {
  const data = response.data;
  console.log(data.groupMember_insert);
});
```

### Using `JoinGroup`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, joinGroupRef, JoinGroupVariables } from '@dataconnect/generated';

// The `JoinGroup` mutation requires an argument of type `JoinGroupVariables`:
const joinGroupVars: JoinGroupVariables = {
  groupId: ..., 
};

// Call the `joinGroupRef()` function to get a reference to the mutation.
const ref = joinGroupRef(joinGroupVars);
// Variables can be defined inline as well.
const ref = joinGroupRef({ groupId: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = joinGroupRef(dataConnect, joinGroupVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.groupMember_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.groupMember_insert);
});
```

## LeaveGroup
You can execute the `LeaveGroup` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
leaveGroup(vars: LeaveGroupVariables): MutationPromise<LeaveGroupData, LeaveGroupVariables>;

interface LeaveGroupRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: LeaveGroupVariables): MutationRef<LeaveGroupData, LeaveGroupVariables>;
}
export const leaveGroupRef: LeaveGroupRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
leaveGroup(dc: DataConnect, vars: LeaveGroupVariables): MutationPromise<LeaveGroupData, LeaveGroupVariables>;

interface LeaveGroupRef {
  ...
  (dc: DataConnect, vars: LeaveGroupVariables): MutationRef<LeaveGroupData, LeaveGroupVariables>;
}
export const leaveGroupRef: LeaveGroupRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the leaveGroupRef:
```typescript
const name = leaveGroupRef.operationName;
console.log(name);
```

### Variables
The `LeaveGroup` mutation requires an argument of type `LeaveGroupVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface LeaveGroupVariables {
  groupId: UUIDString;
}
```
### Return Type
Recall that executing the `LeaveGroup` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `LeaveGroupData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface LeaveGroupData {
  groupMember_delete?: GroupMember_Key | null;
}
```
### Using `LeaveGroup`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, leaveGroup, LeaveGroupVariables } from '@dataconnect/generated';

// The `LeaveGroup` mutation requires an argument of type `LeaveGroupVariables`:
const leaveGroupVars: LeaveGroupVariables = {
  groupId: ..., 
};

// Call the `leaveGroup()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await leaveGroup(leaveGroupVars);
// Variables can be defined inline as well.
const { data } = await leaveGroup({ groupId: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await leaveGroup(dataConnect, leaveGroupVars);

console.log(data.groupMember_delete);

// Or, you can use the `Promise` API.
leaveGroup(leaveGroupVars).then((response) => {
  const data = response.data;
  console.log(data.groupMember_delete);
});
```

### Using `LeaveGroup`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, leaveGroupRef, LeaveGroupVariables } from '@dataconnect/generated';

// The `LeaveGroup` mutation requires an argument of type `LeaveGroupVariables`:
const leaveGroupVars: LeaveGroupVariables = {
  groupId: ..., 
};

// Call the `leaveGroupRef()` function to get a reference to the mutation.
const ref = leaveGroupRef(leaveGroupVars);
// Variables can be defined inline as well.
const ref = leaveGroupRef({ groupId: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = leaveGroupRef(dataConnect, leaveGroupVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.groupMember_delete);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.groupMember_delete);
});
```

## CreateResource
You can execute the `CreateResource` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createResource(vars: CreateResourceVariables): MutationPromise<CreateResourceData, CreateResourceVariables>;

interface CreateResourceRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateResourceVariables): MutationRef<CreateResourceData, CreateResourceVariables>;
}
export const createResourceRef: CreateResourceRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createResource(dc: DataConnect, vars: CreateResourceVariables): MutationPromise<CreateResourceData, CreateResourceVariables>;

interface CreateResourceRef {
  ...
  (dc: DataConnect, vars: CreateResourceVariables): MutationRef<CreateResourceData, CreateResourceVariables>;
}
export const createResourceRef: CreateResourceRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createResourceRef:
```typescript
const name = createResourceRef.operationName;
console.log(name);
```

### Variables
The `CreateResource` mutation requires an argument of type `CreateResourceVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateResourceVariables {
  groupId: UUIDString;
  title: string;
  fileUrl: string;
  type: string;
}
```
### Return Type
Recall that executing the `CreateResource` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateResourceData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateResourceData {
  resource_insert: Resource_Key;
}
```
### Using `CreateResource`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createResource, CreateResourceVariables } from '@dataconnect/generated';

// The `CreateResource` mutation requires an argument of type `CreateResourceVariables`:
const createResourceVars: CreateResourceVariables = {
  groupId: ..., 
  title: ..., 
  fileUrl: ..., 
  type: ..., 
};

// Call the `createResource()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createResource(createResourceVars);
// Variables can be defined inline as well.
const { data } = await createResource({ groupId: ..., title: ..., fileUrl: ..., type: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createResource(dataConnect, createResourceVars);

console.log(data.resource_insert);

// Or, you can use the `Promise` API.
createResource(createResourceVars).then((response) => {
  const data = response.data;
  console.log(data.resource_insert);
});
```

### Using `CreateResource`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createResourceRef, CreateResourceVariables } from '@dataconnect/generated';

// The `CreateResource` mutation requires an argument of type `CreateResourceVariables`:
const createResourceVars: CreateResourceVariables = {
  groupId: ..., 
  title: ..., 
  fileUrl: ..., 
  type: ..., 
};

// Call the `createResourceRef()` function to get a reference to the mutation.
const ref = createResourceRef(createResourceVars);
// Variables can be defined inline as well.
const ref = createResourceRef({ groupId: ..., title: ..., fileUrl: ..., type: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createResourceRef(dataConnect, createResourceVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.resource_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.resource_insert);
});
```

## UpdateResource
You can execute the `UpdateResource` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
updateResource(vars: UpdateResourceVariables): MutationPromise<UpdateResourceData, UpdateResourceVariables>;

interface UpdateResourceRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateResourceVariables): MutationRef<UpdateResourceData, UpdateResourceVariables>;
}
export const updateResourceRef: UpdateResourceRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
updateResource(dc: DataConnect, vars: UpdateResourceVariables): MutationPromise<UpdateResourceData, UpdateResourceVariables>;

interface UpdateResourceRef {
  ...
  (dc: DataConnect, vars: UpdateResourceVariables): MutationRef<UpdateResourceData, UpdateResourceVariables>;
}
export const updateResourceRef: UpdateResourceRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the updateResourceRef:
```typescript
const name = updateResourceRef.operationName;
console.log(name);
```

### Variables
The `UpdateResource` mutation requires an argument of type `UpdateResourceVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface UpdateResourceVariables {
  id: UUIDString;
  title?: string | null;
}
```
### Return Type
Recall that executing the `UpdateResource` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `UpdateResourceData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface UpdateResourceData {
  resource_update?: Resource_Key | null;
}
```
### Using `UpdateResource`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, updateResource, UpdateResourceVariables } from '@dataconnect/generated';

// The `UpdateResource` mutation requires an argument of type `UpdateResourceVariables`:
const updateResourceVars: UpdateResourceVariables = {
  id: ..., 
  title: ..., // optional
};

// Call the `updateResource()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await updateResource(updateResourceVars);
// Variables can be defined inline as well.
const { data } = await updateResource({ id: ..., title: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await updateResource(dataConnect, updateResourceVars);

console.log(data.resource_update);

// Or, you can use the `Promise` API.
updateResource(updateResourceVars).then((response) => {
  const data = response.data;
  console.log(data.resource_update);
});
```

### Using `UpdateResource`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, updateResourceRef, UpdateResourceVariables } from '@dataconnect/generated';

// The `UpdateResource` mutation requires an argument of type `UpdateResourceVariables`:
const updateResourceVars: UpdateResourceVariables = {
  id: ..., 
  title: ..., // optional
};

// Call the `updateResourceRef()` function to get a reference to the mutation.
const ref = updateResourceRef(updateResourceVars);
// Variables can be defined inline as well.
const ref = updateResourceRef({ id: ..., title: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = updateResourceRef(dataConnect, updateResourceVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.resource_update);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.resource_update);
});
```

## DeleteResource
You can execute the `DeleteResource` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
deleteResource(vars: DeleteResourceVariables): MutationPromise<DeleteResourceData, DeleteResourceVariables>;

interface DeleteResourceRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteResourceVariables): MutationRef<DeleteResourceData, DeleteResourceVariables>;
}
export const deleteResourceRef: DeleteResourceRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
deleteResource(dc: DataConnect, vars: DeleteResourceVariables): MutationPromise<DeleteResourceData, DeleteResourceVariables>;

interface DeleteResourceRef {
  ...
  (dc: DataConnect, vars: DeleteResourceVariables): MutationRef<DeleteResourceData, DeleteResourceVariables>;
}
export const deleteResourceRef: DeleteResourceRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the deleteResourceRef:
```typescript
const name = deleteResourceRef.operationName;
console.log(name);
```

### Variables
The `DeleteResource` mutation requires an argument of type `DeleteResourceVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface DeleteResourceVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `DeleteResource` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `DeleteResourceData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface DeleteResourceData {
  resource_delete?: Resource_Key | null;
}
```
### Using `DeleteResource`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, deleteResource, DeleteResourceVariables } from '@dataconnect/generated';

// The `DeleteResource` mutation requires an argument of type `DeleteResourceVariables`:
const deleteResourceVars: DeleteResourceVariables = {
  id: ..., 
};

// Call the `deleteResource()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await deleteResource(deleteResourceVars);
// Variables can be defined inline as well.
const { data } = await deleteResource({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await deleteResource(dataConnect, deleteResourceVars);

console.log(data.resource_delete);

// Or, you can use the `Promise` API.
deleteResource(deleteResourceVars).then((response) => {
  const data = response.data;
  console.log(data.resource_delete);
});
```

### Using `DeleteResource`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, deleteResourceRef, DeleteResourceVariables } from '@dataconnect/generated';

// The `DeleteResource` mutation requires an argument of type `DeleteResourceVariables`:
const deleteResourceVars: DeleteResourceVariables = {
  id: ..., 
};

// Call the `deleteResourceRef()` function to get a reference to the mutation.
const ref = deleteResourceRef(deleteResourceVars);
// Variables can be defined inline as well.
const ref = deleteResourceRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = deleteResourceRef(dataConnect, deleteResourceVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.resource_delete);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.resource_delete);
});
```

## CreateSession
You can execute the `CreateSession` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createSession(vars: CreateSessionVariables): MutationPromise<CreateSessionData, CreateSessionVariables>;

interface CreateSessionRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateSessionVariables): MutationRef<CreateSessionData, CreateSessionVariables>;
}
export const createSessionRef: CreateSessionRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createSession(dc: DataConnect, vars: CreateSessionVariables): MutationPromise<CreateSessionData, CreateSessionVariables>;

interface CreateSessionRef {
  ...
  (dc: DataConnect, vars: CreateSessionVariables): MutationRef<CreateSessionData, CreateSessionVariables>;
}
export const createSessionRef: CreateSessionRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createSessionRef:
```typescript
const name = createSessionRef.operationName;
console.log(name);
```

### Variables
The `CreateSession` mutation requires an argument of type `CreateSessionVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateSessionVariables {
  duration: number;
  topic?: string | null;
}
```
### Return Type
Recall that executing the `CreateSession` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateSessionData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateSessionData {
  session_insert: Session_Key;
}
```
### Using `CreateSession`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createSession, CreateSessionVariables } from '@dataconnect/generated';

// The `CreateSession` mutation requires an argument of type `CreateSessionVariables`:
const createSessionVars: CreateSessionVariables = {
  duration: ..., 
  topic: ..., // optional
};

// Call the `createSession()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createSession(createSessionVars);
// Variables can be defined inline as well.
const { data } = await createSession({ duration: ..., topic: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createSession(dataConnect, createSessionVars);

console.log(data.session_insert);

// Or, you can use the `Promise` API.
createSession(createSessionVars).then((response) => {
  const data = response.data;
  console.log(data.session_insert);
});
```

### Using `CreateSession`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createSessionRef, CreateSessionVariables } from '@dataconnect/generated';

// The `CreateSession` mutation requires an argument of type `CreateSessionVariables`:
const createSessionVars: CreateSessionVariables = {
  duration: ..., 
  topic: ..., // optional
};

// Call the `createSessionRef()` function to get a reference to the mutation.
const ref = createSessionRef(createSessionVars);
// Variables can be defined inline as well.
const ref = createSessionRef({ duration: ..., topic: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createSessionRef(dataConnect, createSessionVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.session_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.session_insert);
});
```

## UpdateSession
You can execute the `UpdateSession` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
updateSession(vars: UpdateSessionVariables): MutationPromise<UpdateSessionData, UpdateSessionVariables>;

interface UpdateSessionRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateSessionVariables): MutationRef<UpdateSessionData, UpdateSessionVariables>;
}
export const updateSessionRef: UpdateSessionRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
updateSession(dc: DataConnect, vars: UpdateSessionVariables): MutationPromise<UpdateSessionData, UpdateSessionVariables>;

interface UpdateSessionRef {
  ...
  (dc: DataConnect, vars: UpdateSessionVariables): MutationRef<UpdateSessionData, UpdateSessionVariables>;
}
export const updateSessionRef: UpdateSessionRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the updateSessionRef:
```typescript
const name = updateSessionRef.operationName;
console.log(name);
```

### Variables
The `UpdateSession` mutation requires an argument of type `UpdateSessionVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface UpdateSessionVariables {
  id: UUIDString;
  topic?: string | null;
}
```
### Return Type
Recall that executing the `UpdateSession` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `UpdateSessionData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface UpdateSessionData {
  session_update?: Session_Key | null;
}
```
### Using `UpdateSession`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, updateSession, UpdateSessionVariables } from '@dataconnect/generated';

// The `UpdateSession` mutation requires an argument of type `UpdateSessionVariables`:
const updateSessionVars: UpdateSessionVariables = {
  id: ..., 
  topic: ..., // optional
};

// Call the `updateSession()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await updateSession(updateSessionVars);
// Variables can be defined inline as well.
const { data } = await updateSession({ id: ..., topic: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await updateSession(dataConnect, updateSessionVars);

console.log(data.session_update);

// Or, you can use the `Promise` API.
updateSession(updateSessionVars).then((response) => {
  const data = response.data;
  console.log(data.session_update);
});
```

### Using `UpdateSession`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, updateSessionRef, UpdateSessionVariables } from '@dataconnect/generated';

// The `UpdateSession` mutation requires an argument of type `UpdateSessionVariables`:
const updateSessionVars: UpdateSessionVariables = {
  id: ..., 
  topic: ..., // optional
};

// Call the `updateSessionRef()` function to get a reference to the mutation.
const ref = updateSessionRef(updateSessionVars);
// Variables can be defined inline as well.
const ref = updateSessionRef({ id: ..., topic: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = updateSessionRef(dataConnect, updateSessionVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.session_update);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.session_update);
});
```

## DeleteSession
You can execute the `DeleteSession` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
deleteSession(vars: DeleteSessionVariables): MutationPromise<DeleteSessionData, DeleteSessionVariables>;

interface DeleteSessionRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteSessionVariables): MutationRef<DeleteSessionData, DeleteSessionVariables>;
}
export const deleteSessionRef: DeleteSessionRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
deleteSession(dc: DataConnect, vars: DeleteSessionVariables): MutationPromise<DeleteSessionData, DeleteSessionVariables>;

interface DeleteSessionRef {
  ...
  (dc: DataConnect, vars: DeleteSessionVariables): MutationRef<DeleteSessionData, DeleteSessionVariables>;
}
export const deleteSessionRef: DeleteSessionRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the deleteSessionRef:
```typescript
const name = deleteSessionRef.operationName;
console.log(name);
```

### Variables
The `DeleteSession` mutation requires an argument of type `DeleteSessionVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface DeleteSessionVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `DeleteSession` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `DeleteSessionData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface DeleteSessionData {
  session_delete?: Session_Key | null;
}
```
### Using `DeleteSession`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, deleteSession, DeleteSessionVariables } from '@dataconnect/generated';

// The `DeleteSession` mutation requires an argument of type `DeleteSessionVariables`:
const deleteSessionVars: DeleteSessionVariables = {
  id: ..., 
};

// Call the `deleteSession()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await deleteSession(deleteSessionVars);
// Variables can be defined inline as well.
const { data } = await deleteSession({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await deleteSession(dataConnect, deleteSessionVars);

console.log(data.session_delete);

// Or, you can use the `Promise` API.
deleteSession(deleteSessionVars).then((response) => {
  const data = response.data;
  console.log(data.session_delete);
});
```

### Using `DeleteSession`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, deleteSessionRef, DeleteSessionVariables } from '@dataconnect/generated';

// The `DeleteSession` mutation requires an argument of type `DeleteSessionVariables`:
const deleteSessionVars: DeleteSessionVariables = {
  id: ..., 
};

// Call the `deleteSessionRef()` function to get a reference to the mutation.
const ref = deleteSessionRef(deleteSessionVars);
// Variables can be defined inline as well.
const ref = deleteSessionRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = deleteSessionRef(dataConnect, deleteSessionVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.session_delete);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.session_delete);
});
```

## CreateVideoCall
You can execute the `CreateVideoCall` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createVideoCall(vars: CreateVideoCallVariables): MutationPromise<CreateVideoCallData, CreateVideoCallVariables>;

interface CreateVideoCallRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateVideoCallVariables): MutationRef<CreateVideoCallData, CreateVideoCallVariables>;
}
export const createVideoCallRef: CreateVideoCallRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createVideoCall(dc: DataConnect, vars: CreateVideoCallVariables): MutationPromise<CreateVideoCallData, CreateVideoCallVariables>;

interface CreateVideoCallRef {
  ...
  (dc: DataConnect, vars: CreateVideoCallVariables): MutationRef<CreateVideoCallData, CreateVideoCallVariables>;
}
export const createVideoCallRef: CreateVideoCallRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createVideoCallRef:
```typescript
const name = createVideoCallRef.operationName;
console.log(name);
```

### Variables
The `CreateVideoCall` mutation requires an argument of type `CreateVideoCallVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateVideoCallVariables {
  groupId: UUIDString;
  isActive: boolean;
}
```
### Return Type
Recall that executing the `CreateVideoCall` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateVideoCallData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateVideoCallData {
  videoCall_insert: VideoCall_Key;
}
```
### Using `CreateVideoCall`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createVideoCall, CreateVideoCallVariables } from '@dataconnect/generated';

// The `CreateVideoCall` mutation requires an argument of type `CreateVideoCallVariables`:
const createVideoCallVars: CreateVideoCallVariables = {
  groupId: ..., 
  isActive: ..., 
};

// Call the `createVideoCall()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createVideoCall(createVideoCallVars);
// Variables can be defined inline as well.
const { data } = await createVideoCall({ groupId: ..., isActive: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createVideoCall(dataConnect, createVideoCallVars);

console.log(data.videoCall_insert);

// Or, you can use the `Promise` API.
createVideoCall(createVideoCallVars).then((response) => {
  const data = response.data;
  console.log(data.videoCall_insert);
});
```

### Using `CreateVideoCall`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createVideoCallRef, CreateVideoCallVariables } from '@dataconnect/generated';

// The `CreateVideoCall` mutation requires an argument of type `CreateVideoCallVariables`:
const createVideoCallVars: CreateVideoCallVariables = {
  groupId: ..., 
  isActive: ..., 
};

// Call the `createVideoCallRef()` function to get a reference to the mutation.
const ref = createVideoCallRef(createVideoCallVars);
// Variables can be defined inline as well.
const ref = createVideoCallRef({ groupId: ..., isActive: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createVideoCallRef(dataConnect, createVideoCallVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.videoCall_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.videoCall_insert);
});
```

## UpdateVideoCall
You can execute the `UpdateVideoCall` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
updateVideoCall(vars: UpdateVideoCallVariables): MutationPromise<UpdateVideoCallData, UpdateVideoCallVariables>;

interface UpdateVideoCallRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateVideoCallVariables): MutationRef<UpdateVideoCallData, UpdateVideoCallVariables>;
}
export const updateVideoCallRef: UpdateVideoCallRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
updateVideoCall(dc: DataConnect, vars: UpdateVideoCallVariables): MutationPromise<UpdateVideoCallData, UpdateVideoCallVariables>;

interface UpdateVideoCallRef {
  ...
  (dc: DataConnect, vars: UpdateVideoCallVariables): MutationRef<UpdateVideoCallData, UpdateVideoCallVariables>;
}
export const updateVideoCallRef: UpdateVideoCallRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the updateVideoCallRef:
```typescript
const name = updateVideoCallRef.operationName;
console.log(name);
```

### Variables
The `UpdateVideoCall` mutation requires an argument of type `UpdateVideoCallVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface UpdateVideoCallVariables {
  id: UUIDString;
  isActive?: boolean | null;
}
```
### Return Type
Recall that executing the `UpdateVideoCall` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `UpdateVideoCallData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface UpdateVideoCallData {
  videoCall_update?: VideoCall_Key | null;
}
```
### Using `UpdateVideoCall`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, updateVideoCall, UpdateVideoCallVariables } from '@dataconnect/generated';

// The `UpdateVideoCall` mutation requires an argument of type `UpdateVideoCallVariables`:
const updateVideoCallVars: UpdateVideoCallVariables = {
  id: ..., 
  isActive: ..., // optional
};

// Call the `updateVideoCall()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await updateVideoCall(updateVideoCallVars);
// Variables can be defined inline as well.
const { data } = await updateVideoCall({ id: ..., isActive: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await updateVideoCall(dataConnect, updateVideoCallVars);

console.log(data.videoCall_update);

// Or, you can use the `Promise` API.
updateVideoCall(updateVideoCallVars).then((response) => {
  const data = response.data;
  console.log(data.videoCall_update);
});
```

### Using `UpdateVideoCall`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, updateVideoCallRef, UpdateVideoCallVariables } from '@dataconnect/generated';

// The `UpdateVideoCall` mutation requires an argument of type `UpdateVideoCallVariables`:
const updateVideoCallVars: UpdateVideoCallVariables = {
  id: ..., 
  isActive: ..., // optional
};

// Call the `updateVideoCallRef()` function to get a reference to the mutation.
const ref = updateVideoCallRef(updateVideoCallVars);
// Variables can be defined inline as well.
const ref = updateVideoCallRef({ id: ..., isActive: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = updateVideoCallRef(dataConnect, updateVideoCallVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.videoCall_update);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.videoCall_update);
});
```

## DeleteVideoCall
You can execute the `DeleteVideoCall` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
deleteVideoCall(vars: DeleteVideoCallVariables): MutationPromise<DeleteVideoCallData, DeleteVideoCallVariables>;

interface DeleteVideoCallRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteVideoCallVariables): MutationRef<DeleteVideoCallData, DeleteVideoCallVariables>;
}
export const deleteVideoCallRef: DeleteVideoCallRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
deleteVideoCall(dc: DataConnect, vars: DeleteVideoCallVariables): MutationPromise<DeleteVideoCallData, DeleteVideoCallVariables>;

interface DeleteVideoCallRef {
  ...
  (dc: DataConnect, vars: DeleteVideoCallVariables): MutationRef<DeleteVideoCallData, DeleteVideoCallVariables>;
}
export const deleteVideoCallRef: DeleteVideoCallRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the deleteVideoCallRef:
```typescript
const name = deleteVideoCallRef.operationName;
console.log(name);
```

### Variables
The `DeleteVideoCall` mutation requires an argument of type `DeleteVideoCallVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface DeleteVideoCallVariables {
  id: UUIDString;
}
```
### Return Type
Recall that executing the `DeleteVideoCall` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `DeleteVideoCallData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface DeleteVideoCallData {
  videoCall_delete?: VideoCall_Key | null;
}
```
### Using `DeleteVideoCall`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, deleteVideoCall, DeleteVideoCallVariables } from '@dataconnect/generated';

// The `DeleteVideoCall` mutation requires an argument of type `DeleteVideoCallVariables`:
const deleteVideoCallVars: DeleteVideoCallVariables = {
  id: ..., 
};

// Call the `deleteVideoCall()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await deleteVideoCall(deleteVideoCallVars);
// Variables can be defined inline as well.
const { data } = await deleteVideoCall({ id: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await deleteVideoCall(dataConnect, deleteVideoCallVars);

console.log(data.videoCall_delete);

// Or, you can use the `Promise` API.
deleteVideoCall(deleteVideoCallVars).then((response) => {
  const data = response.data;
  console.log(data.videoCall_delete);
});
```

### Using `DeleteVideoCall`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, deleteVideoCallRef, DeleteVideoCallVariables } from '@dataconnect/generated';

// The `DeleteVideoCall` mutation requires an argument of type `DeleteVideoCallVariables`:
const deleteVideoCallVars: DeleteVideoCallVariables = {
  id: ..., 
};

// Call the `deleteVideoCallRef()` function to get a reference to the mutation.
const ref = deleteVideoCallRef(deleteVideoCallVars);
// Variables can be defined inline as well.
const ref = deleteVideoCallRef({ id: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = deleteVideoCallRef(dataConnect, deleteVideoCallVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.videoCall_delete);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.videoCall_delete);
});
```

## JoinCall
You can execute the `JoinCall` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
joinCall(vars: JoinCallVariables): MutationPromise<JoinCallData, JoinCallVariables>;

interface JoinCallRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: JoinCallVariables): MutationRef<JoinCallData, JoinCallVariables>;
}
export const joinCallRef: JoinCallRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
joinCall(dc: DataConnect, vars: JoinCallVariables): MutationPromise<JoinCallData, JoinCallVariables>;

interface JoinCallRef {
  ...
  (dc: DataConnect, vars: JoinCallVariables): MutationRef<JoinCallData, JoinCallVariables>;
}
export const joinCallRef: JoinCallRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the joinCallRef:
```typescript
const name = joinCallRef.operationName;
console.log(name);
```

### Variables
The `JoinCall` mutation requires an argument of type `JoinCallVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface JoinCallVariables {
  callId: UUIDString;
}
```
### Return Type
Recall that executing the `JoinCall` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `JoinCallData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface JoinCallData {
  callParticipant_insert: CallParticipant_Key;
}
```
### Using `JoinCall`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, joinCall, JoinCallVariables } from '@dataconnect/generated';

// The `JoinCall` mutation requires an argument of type `JoinCallVariables`:
const joinCallVars: JoinCallVariables = {
  callId: ..., 
};

// Call the `joinCall()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await joinCall(joinCallVars);
// Variables can be defined inline as well.
const { data } = await joinCall({ callId: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await joinCall(dataConnect, joinCallVars);

console.log(data.callParticipant_insert);

// Or, you can use the `Promise` API.
joinCall(joinCallVars).then((response) => {
  const data = response.data;
  console.log(data.callParticipant_insert);
});
```

### Using `JoinCall`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, joinCallRef, JoinCallVariables } from '@dataconnect/generated';

// The `JoinCall` mutation requires an argument of type `JoinCallVariables`:
const joinCallVars: JoinCallVariables = {
  callId: ..., 
};

// Call the `joinCallRef()` function to get a reference to the mutation.
const ref = joinCallRef(joinCallVars);
// Variables can be defined inline as well.
const ref = joinCallRef({ callId: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = joinCallRef(dataConnect, joinCallVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.callParticipant_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.callParticipant_insert);
});
```

## LeaveCall
You can execute the `LeaveCall` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
leaveCall(vars: LeaveCallVariables): MutationPromise<LeaveCallData, LeaveCallVariables>;

interface LeaveCallRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: LeaveCallVariables): MutationRef<LeaveCallData, LeaveCallVariables>;
}
export const leaveCallRef: LeaveCallRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
leaveCall(dc: DataConnect, vars: LeaveCallVariables): MutationPromise<LeaveCallData, LeaveCallVariables>;

interface LeaveCallRef {
  ...
  (dc: DataConnect, vars: LeaveCallVariables): MutationRef<LeaveCallData, LeaveCallVariables>;
}
export const leaveCallRef: LeaveCallRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the leaveCallRef:
```typescript
const name = leaveCallRef.operationName;
console.log(name);
```

### Variables
The `LeaveCall` mutation requires an argument of type `LeaveCallVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface LeaveCallVariables {
  callId: UUIDString;
}
```
### Return Type
Recall that executing the `LeaveCall` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `LeaveCallData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface LeaveCallData {
  callParticipant_delete?: CallParticipant_Key | null;
}
```
### Using `LeaveCall`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, leaveCall, LeaveCallVariables } from '@dataconnect/generated';

// The `LeaveCall` mutation requires an argument of type `LeaveCallVariables`:
const leaveCallVars: LeaveCallVariables = {
  callId: ..., 
};

// Call the `leaveCall()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await leaveCall(leaveCallVars);
// Variables can be defined inline as well.
const { data } = await leaveCall({ callId: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await leaveCall(dataConnect, leaveCallVars);

console.log(data.callParticipant_delete);

// Or, you can use the `Promise` API.
leaveCall(leaveCallVars).then((response) => {
  const data = response.data;
  console.log(data.callParticipant_delete);
});
```

### Using `LeaveCall`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, leaveCallRef, LeaveCallVariables } from '@dataconnect/generated';

// The `LeaveCall` mutation requires an argument of type `LeaveCallVariables`:
const leaveCallVars: LeaveCallVariables = {
  callId: ..., 
};

// Call the `leaveCallRef()` function to get a reference to the mutation.
const ref = leaveCallRef(leaveCallVars);
// Variables can be defined inline as well.
const ref = leaveCallRef({ callId: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = leaveCallRef(dataConnect, leaveCallVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.callParticipant_delete);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.callParticipant_delete);
});
```

