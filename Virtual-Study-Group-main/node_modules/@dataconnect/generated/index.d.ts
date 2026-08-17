import { ConnectorConfig, DataConnect, QueryRef, QueryPromise, ExecuteQueryOptions, MutationRef, MutationPromise, DataConnectSettings } from 'firebase/data-connect';

export const connectorConfig: ConnectorConfig;
export const dataConnectSettings: DataConnectSettings;

export type TimestampString = string;
export type UUIDString = string;
export type Int64String = string;
export type DateString = string;




export interface CallParticipant_Key {
  callId: UUIDString;
  userId: UUIDString;
  __typename?: 'CallParticipant_Key';
}

export interface CreateResourceData {
  resource_insert: Resource_Key;
}

export interface CreateResourceVariables {
  groupId: UUIDString;
  title: string;
  fileUrl: string;
  type: string;
}

export interface CreateSessionData {
  session_insert: Session_Key;
}

export interface CreateSessionVariables {
  duration: number;
  topic?: string | null;
}

export interface CreateStudyGroupData {
  studyGroup_insert: StudyGroup_Key;
}

export interface CreateStudyGroupVariables {
  name: string;
  description?: string | null;
}

export interface CreateUserData {
  user_insert: User_Key;
}

export interface CreateUserVariables {
  username: string;
  email: string;
  totalHours: number;
}

export interface CreateVideoCallData {
  videoCall_insert: VideoCall_Key;
}

export interface CreateVideoCallVariables {
  groupId: UUIDString;
  isActive: boolean;
}

export interface DeleteResourceData {
  resource_delete?: Resource_Key | null;
}

export interface DeleteResourceVariables {
  id: UUIDString;
}

export interface DeleteSessionData {
  session_delete?: Session_Key | null;
}

export interface DeleteSessionVariables {
  id: UUIDString;
}

export interface DeleteStudyGroupData {
  studyGroup_delete?: StudyGroup_Key | null;
}

export interface DeleteStudyGroupVariables {
  id: UUIDString;
}

export interface DeleteUserData {
  user_delete?: User_Key | null;
}

export interface DeleteVideoCallData {
  videoCall_delete?: VideoCall_Key | null;
}

export interface DeleteVideoCallVariables {
  id: UUIDString;
}

export interface GetResourceData {
  resource?: {
    title: string;
    fileUrl: string;
  };
}

export interface GetResourceVariables {
  id: UUIDString;
}

export interface GetSessionData {
  session?: {
    topic?: string | null;
    durationMinutes: number;
  };
}

export interface GetSessionVariables {
  id: UUIDString;
}

export interface GetStudyGroupData {
  studyGroup?: {
    name: string;
    description?: string | null;
  };
}

export interface GetStudyGroupVariables {
  id: UUIDString;
}

export interface GetUserData {
  user?: {
    username: string;
    email: string;
    totalHours: number;
  };
}

export interface GetVideoCallData {
  videoCall?: {
    isActive: boolean;
    startTime?: TimestampString | null;
  };
}

export interface GetVideoCallVariables {
  id: UUIDString;
}

export interface GroupMember_Key {
  userId: UUIDString;
  groupId: UUIDString;
  __typename?: 'GroupMember_Key';
}

export interface JoinCallData {
  callParticipant_insert: CallParticipant_Key;
}

export interface JoinCallVariables {
  callId: UUIDString;
}

export interface JoinGroupData {
  groupMember_insert: GroupMember_Key;
}

export interface JoinGroupVariables {
  groupId: UUIDString;
}

export interface LeaveCallData {
  callParticipant_delete?: CallParticipant_Key | null;
}

export interface LeaveCallVariables {
  callId: UUIDString;
}

export interface LeaveGroupData {
  groupMember_delete?: GroupMember_Key | null;
}

export interface LeaveGroupVariables {
  groupId: UUIDString;
}

export interface ListCallParticipantsData {
  callParticipants: ({
    user: {
      username: string;
    };
  })[];
}

export interface ListCallParticipantsVariables {
  callId: UUIDString;
}

export interface ListGroupMembersData {
  groupMembers: ({
    user: {
      username: string;
    };
  })[];
}

export interface ListGroupMembersVariables {
  groupId: UUIDString;
}

export interface ListMySessionsData {
  sessions: ({
    topic?: string | null;
    durationMinutes: number;
  })[];
}

export interface ListResourcesData {
  resources: ({
    title: string;
    type: string;
  })[];
}

export interface ListResourcesVariables {
  groupId: UUIDString;
}

export interface ListStudyGroupsData {
  studyGroups: ({
    name: string;
  })[];
}

export interface ListUsersData {
  users: ({
    username: string;
    totalHours: number;
  })[];
}

export interface ListVideoCallsData {
  videoCalls: ({
    isActive: boolean;
  })[];
}

export interface ListVideoCallsVariables {
  groupId: UUIDString;
}

export interface Resource_Key {
  id: UUIDString;
  __typename?: 'Resource_Key';
}

export interface Session_Key {
  id: UUIDString;
  __typename?: 'Session_Key';
}

export interface StudyGroup_Key {
  id: UUIDString;
  __typename?: 'StudyGroup_Key';
}

export interface UpdateResourceData {
  resource_update?: Resource_Key | null;
}

export interface UpdateResourceVariables {
  id: UUIDString;
  title?: string | null;
}

export interface UpdateSessionData {
  session_update?: Session_Key | null;
}

export interface UpdateSessionVariables {
  id: UUIDString;
  topic?: string | null;
}

export interface UpdateStudyGroupData {
  studyGroup_update?: StudyGroup_Key | null;
}

export interface UpdateStudyGroupVariables {
  id: UUIDString;
  name?: string | null;
}

export interface UpdateUserData {
  user_update?: User_Key | null;
}

export interface UpdateUserVariables {
  username?: string | null;
}

export interface UpdateVideoCallData {
  videoCall_update?: VideoCall_Key | null;
}

export interface UpdateVideoCallVariables {
  id: UUIDString;
  isActive?: boolean | null;
}

export interface User_Key {
  id: UUIDString;
  __typename?: 'User_Key';
}

export interface VideoCall_Key {
  id: UUIDString;
  __typename?: 'VideoCall_Key';
}

interface CreateUserRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateUserVariables): MutationRef<CreateUserData, CreateUserVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateUserVariables): MutationRef<CreateUserData, CreateUserVariables>;
  operationName: string;
}
export const createUserRef: CreateUserRef;

export function createUser(vars: CreateUserVariables): MutationPromise<CreateUserData, CreateUserVariables>;
export function createUser(dc: DataConnect, vars: CreateUserVariables): MutationPromise<CreateUserData, CreateUserVariables>;

interface UpdateUserRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars?: UpdateUserVariables): MutationRef<UpdateUserData, UpdateUserVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars?: UpdateUserVariables): MutationRef<UpdateUserData, UpdateUserVariables>;
  operationName: string;
}
export const updateUserRef: UpdateUserRef;

export function updateUser(vars?: UpdateUserVariables): MutationPromise<UpdateUserData, UpdateUserVariables>;
export function updateUser(dc: DataConnect, vars?: UpdateUserVariables): MutationPromise<UpdateUserData, UpdateUserVariables>;

interface DeleteUserRef {
  /* Allow users to create refs without passing in DataConnect */
  (): MutationRef<DeleteUserData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): MutationRef<DeleteUserData, undefined>;
  operationName: string;
}
export const deleteUserRef: DeleteUserRef;

export function deleteUser(): MutationPromise<DeleteUserData, undefined>;
export function deleteUser(dc: DataConnect): MutationPromise<DeleteUserData, undefined>;

interface GetUserRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<GetUserData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<GetUserData, undefined>;
  operationName: string;
}
export const getUserRef: GetUserRef;

export function getUser(options?: ExecuteQueryOptions): QueryPromise<GetUserData, undefined>;
export function getUser(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<GetUserData, undefined>;

interface ListUsersRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListUsersData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<ListUsersData, undefined>;
  operationName: string;
}
export const listUsersRef: ListUsersRef;

export function listUsers(options?: ExecuteQueryOptions): QueryPromise<ListUsersData, undefined>;
export function listUsers(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListUsersData, undefined>;

interface CreateStudyGroupRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateStudyGroupVariables): MutationRef<CreateStudyGroupData, CreateStudyGroupVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateStudyGroupVariables): MutationRef<CreateStudyGroupData, CreateStudyGroupVariables>;
  operationName: string;
}
export const createStudyGroupRef: CreateStudyGroupRef;

export function createStudyGroup(vars: CreateStudyGroupVariables): MutationPromise<CreateStudyGroupData, CreateStudyGroupVariables>;
export function createStudyGroup(dc: DataConnect, vars: CreateStudyGroupVariables): MutationPromise<CreateStudyGroupData, CreateStudyGroupVariables>;

interface UpdateStudyGroupRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateStudyGroupVariables): MutationRef<UpdateStudyGroupData, UpdateStudyGroupVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: UpdateStudyGroupVariables): MutationRef<UpdateStudyGroupData, UpdateStudyGroupVariables>;
  operationName: string;
}
export const updateStudyGroupRef: UpdateStudyGroupRef;

export function updateStudyGroup(vars: UpdateStudyGroupVariables): MutationPromise<UpdateStudyGroupData, UpdateStudyGroupVariables>;
export function updateStudyGroup(dc: DataConnect, vars: UpdateStudyGroupVariables): MutationPromise<UpdateStudyGroupData, UpdateStudyGroupVariables>;

interface DeleteStudyGroupRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteStudyGroupVariables): MutationRef<DeleteStudyGroupData, DeleteStudyGroupVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: DeleteStudyGroupVariables): MutationRef<DeleteStudyGroupData, DeleteStudyGroupVariables>;
  operationName: string;
}
export const deleteStudyGroupRef: DeleteStudyGroupRef;

export function deleteStudyGroup(vars: DeleteStudyGroupVariables): MutationPromise<DeleteStudyGroupData, DeleteStudyGroupVariables>;
export function deleteStudyGroup(dc: DataConnect, vars: DeleteStudyGroupVariables): MutationPromise<DeleteStudyGroupData, DeleteStudyGroupVariables>;

interface GetStudyGroupRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetStudyGroupVariables): QueryRef<GetStudyGroupData, GetStudyGroupVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: GetStudyGroupVariables): QueryRef<GetStudyGroupData, GetStudyGroupVariables>;
  operationName: string;
}
export const getStudyGroupRef: GetStudyGroupRef;

export function getStudyGroup(vars: GetStudyGroupVariables, options?: ExecuteQueryOptions): QueryPromise<GetStudyGroupData, GetStudyGroupVariables>;
export function getStudyGroup(dc: DataConnect, vars: GetStudyGroupVariables, options?: ExecuteQueryOptions): QueryPromise<GetStudyGroupData, GetStudyGroupVariables>;

interface ListStudyGroupsRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListStudyGroupsData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<ListStudyGroupsData, undefined>;
  operationName: string;
}
export const listStudyGroupsRef: ListStudyGroupsRef;

export function listStudyGroups(options?: ExecuteQueryOptions): QueryPromise<ListStudyGroupsData, undefined>;
export function listStudyGroups(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListStudyGroupsData, undefined>;

interface JoinGroupRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: JoinGroupVariables): MutationRef<JoinGroupData, JoinGroupVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: JoinGroupVariables): MutationRef<JoinGroupData, JoinGroupVariables>;
  operationName: string;
}
export const joinGroupRef: JoinGroupRef;

export function joinGroup(vars: JoinGroupVariables): MutationPromise<JoinGroupData, JoinGroupVariables>;
export function joinGroup(dc: DataConnect, vars: JoinGroupVariables): MutationPromise<JoinGroupData, JoinGroupVariables>;

interface LeaveGroupRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: LeaveGroupVariables): MutationRef<LeaveGroupData, LeaveGroupVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: LeaveGroupVariables): MutationRef<LeaveGroupData, LeaveGroupVariables>;
  operationName: string;
}
export const leaveGroupRef: LeaveGroupRef;

export function leaveGroup(vars: LeaveGroupVariables): MutationPromise<LeaveGroupData, LeaveGroupVariables>;
export function leaveGroup(dc: DataConnect, vars: LeaveGroupVariables): MutationPromise<LeaveGroupData, LeaveGroupVariables>;

interface ListGroupMembersRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: ListGroupMembersVariables): QueryRef<ListGroupMembersData, ListGroupMembersVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: ListGroupMembersVariables): QueryRef<ListGroupMembersData, ListGroupMembersVariables>;
  operationName: string;
}
export const listGroupMembersRef: ListGroupMembersRef;

export function listGroupMembers(vars: ListGroupMembersVariables, options?: ExecuteQueryOptions): QueryPromise<ListGroupMembersData, ListGroupMembersVariables>;
export function listGroupMembers(dc: DataConnect, vars: ListGroupMembersVariables, options?: ExecuteQueryOptions): QueryPromise<ListGroupMembersData, ListGroupMembersVariables>;

interface CreateResourceRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateResourceVariables): MutationRef<CreateResourceData, CreateResourceVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateResourceVariables): MutationRef<CreateResourceData, CreateResourceVariables>;
  operationName: string;
}
export const createResourceRef: CreateResourceRef;

export function createResource(vars: CreateResourceVariables): MutationPromise<CreateResourceData, CreateResourceVariables>;
export function createResource(dc: DataConnect, vars: CreateResourceVariables): MutationPromise<CreateResourceData, CreateResourceVariables>;

interface UpdateResourceRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateResourceVariables): MutationRef<UpdateResourceData, UpdateResourceVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: UpdateResourceVariables): MutationRef<UpdateResourceData, UpdateResourceVariables>;
  operationName: string;
}
export const updateResourceRef: UpdateResourceRef;

export function updateResource(vars: UpdateResourceVariables): MutationPromise<UpdateResourceData, UpdateResourceVariables>;
export function updateResource(dc: DataConnect, vars: UpdateResourceVariables): MutationPromise<UpdateResourceData, UpdateResourceVariables>;

interface DeleteResourceRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteResourceVariables): MutationRef<DeleteResourceData, DeleteResourceVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: DeleteResourceVariables): MutationRef<DeleteResourceData, DeleteResourceVariables>;
  operationName: string;
}
export const deleteResourceRef: DeleteResourceRef;

export function deleteResource(vars: DeleteResourceVariables): MutationPromise<DeleteResourceData, DeleteResourceVariables>;
export function deleteResource(dc: DataConnect, vars: DeleteResourceVariables): MutationPromise<DeleteResourceData, DeleteResourceVariables>;

interface GetResourceRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetResourceVariables): QueryRef<GetResourceData, GetResourceVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: GetResourceVariables): QueryRef<GetResourceData, GetResourceVariables>;
  operationName: string;
}
export const getResourceRef: GetResourceRef;

export function getResource(vars: GetResourceVariables, options?: ExecuteQueryOptions): QueryPromise<GetResourceData, GetResourceVariables>;
export function getResource(dc: DataConnect, vars: GetResourceVariables, options?: ExecuteQueryOptions): QueryPromise<GetResourceData, GetResourceVariables>;

interface ListResourcesRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: ListResourcesVariables): QueryRef<ListResourcesData, ListResourcesVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: ListResourcesVariables): QueryRef<ListResourcesData, ListResourcesVariables>;
  operationName: string;
}
export const listResourcesRef: ListResourcesRef;

export function listResources(vars: ListResourcesVariables, options?: ExecuteQueryOptions): QueryPromise<ListResourcesData, ListResourcesVariables>;
export function listResources(dc: DataConnect, vars: ListResourcesVariables, options?: ExecuteQueryOptions): QueryPromise<ListResourcesData, ListResourcesVariables>;

interface CreateSessionRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateSessionVariables): MutationRef<CreateSessionData, CreateSessionVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateSessionVariables): MutationRef<CreateSessionData, CreateSessionVariables>;
  operationName: string;
}
export const createSessionRef: CreateSessionRef;

export function createSession(vars: CreateSessionVariables): MutationPromise<CreateSessionData, CreateSessionVariables>;
export function createSession(dc: DataConnect, vars: CreateSessionVariables): MutationPromise<CreateSessionData, CreateSessionVariables>;

interface UpdateSessionRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateSessionVariables): MutationRef<UpdateSessionData, UpdateSessionVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: UpdateSessionVariables): MutationRef<UpdateSessionData, UpdateSessionVariables>;
  operationName: string;
}
export const updateSessionRef: UpdateSessionRef;

export function updateSession(vars: UpdateSessionVariables): MutationPromise<UpdateSessionData, UpdateSessionVariables>;
export function updateSession(dc: DataConnect, vars: UpdateSessionVariables): MutationPromise<UpdateSessionData, UpdateSessionVariables>;

interface DeleteSessionRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteSessionVariables): MutationRef<DeleteSessionData, DeleteSessionVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: DeleteSessionVariables): MutationRef<DeleteSessionData, DeleteSessionVariables>;
  operationName: string;
}
export const deleteSessionRef: DeleteSessionRef;

export function deleteSession(vars: DeleteSessionVariables): MutationPromise<DeleteSessionData, DeleteSessionVariables>;
export function deleteSession(dc: DataConnect, vars: DeleteSessionVariables): MutationPromise<DeleteSessionData, DeleteSessionVariables>;

interface GetSessionRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetSessionVariables): QueryRef<GetSessionData, GetSessionVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: GetSessionVariables): QueryRef<GetSessionData, GetSessionVariables>;
  operationName: string;
}
export const getSessionRef: GetSessionRef;

export function getSession(vars: GetSessionVariables, options?: ExecuteQueryOptions): QueryPromise<GetSessionData, GetSessionVariables>;
export function getSession(dc: DataConnect, vars: GetSessionVariables, options?: ExecuteQueryOptions): QueryPromise<GetSessionData, GetSessionVariables>;

interface ListMySessionsRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<ListMySessionsData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<ListMySessionsData, undefined>;
  operationName: string;
}
export const listMySessionsRef: ListMySessionsRef;

export function listMySessions(options?: ExecuteQueryOptions): QueryPromise<ListMySessionsData, undefined>;
export function listMySessions(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<ListMySessionsData, undefined>;

interface CreateVideoCallRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateVideoCallVariables): MutationRef<CreateVideoCallData, CreateVideoCallVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateVideoCallVariables): MutationRef<CreateVideoCallData, CreateVideoCallVariables>;
  operationName: string;
}
export const createVideoCallRef: CreateVideoCallRef;

export function createVideoCall(vars: CreateVideoCallVariables): MutationPromise<CreateVideoCallData, CreateVideoCallVariables>;
export function createVideoCall(dc: DataConnect, vars: CreateVideoCallVariables): MutationPromise<CreateVideoCallData, CreateVideoCallVariables>;

interface UpdateVideoCallRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: UpdateVideoCallVariables): MutationRef<UpdateVideoCallData, UpdateVideoCallVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: UpdateVideoCallVariables): MutationRef<UpdateVideoCallData, UpdateVideoCallVariables>;
  operationName: string;
}
export const updateVideoCallRef: UpdateVideoCallRef;

export function updateVideoCall(vars: UpdateVideoCallVariables): MutationPromise<UpdateVideoCallData, UpdateVideoCallVariables>;
export function updateVideoCall(dc: DataConnect, vars: UpdateVideoCallVariables): MutationPromise<UpdateVideoCallData, UpdateVideoCallVariables>;

interface DeleteVideoCallRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: DeleteVideoCallVariables): MutationRef<DeleteVideoCallData, DeleteVideoCallVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: DeleteVideoCallVariables): MutationRef<DeleteVideoCallData, DeleteVideoCallVariables>;
  operationName: string;
}
export const deleteVideoCallRef: DeleteVideoCallRef;

export function deleteVideoCall(vars: DeleteVideoCallVariables): MutationPromise<DeleteVideoCallData, DeleteVideoCallVariables>;
export function deleteVideoCall(dc: DataConnect, vars: DeleteVideoCallVariables): MutationPromise<DeleteVideoCallData, DeleteVideoCallVariables>;

interface GetVideoCallRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: GetVideoCallVariables): QueryRef<GetVideoCallData, GetVideoCallVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: GetVideoCallVariables): QueryRef<GetVideoCallData, GetVideoCallVariables>;
  operationName: string;
}
export const getVideoCallRef: GetVideoCallRef;

export function getVideoCall(vars: GetVideoCallVariables, options?: ExecuteQueryOptions): QueryPromise<GetVideoCallData, GetVideoCallVariables>;
export function getVideoCall(dc: DataConnect, vars: GetVideoCallVariables, options?: ExecuteQueryOptions): QueryPromise<GetVideoCallData, GetVideoCallVariables>;

interface ListVideoCallsRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: ListVideoCallsVariables): QueryRef<ListVideoCallsData, ListVideoCallsVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: ListVideoCallsVariables): QueryRef<ListVideoCallsData, ListVideoCallsVariables>;
  operationName: string;
}
export const listVideoCallsRef: ListVideoCallsRef;

export function listVideoCalls(vars: ListVideoCallsVariables, options?: ExecuteQueryOptions): QueryPromise<ListVideoCallsData, ListVideoCallsVariables>;
export function listVideoCalls(dc: DataConnect, vars: ListVideoCallsVariables, options?: ExecuteQueryOptions): QueryPromise<ListVideoCallsData, ListVideoCallsVariables>;

interface JoinCallRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: JoinCallVariables): MutationRef<JoinCallData, JoinCallVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: JoinCallVariables): MutationRef<JoinCallData, JoinCallVariables>;
  operationName: string;
}
export const joinCallRef: JoinCallRef;

export function joinCall(vars: JoinCallVariables): MutationPromise<JoinCallData, JoinCallVariables>;
export function joinCall(dc: DataConnect, vars: JoinCallVariables): MutationPromise<JoinCallData, JoinCallVariables>;

interface LeaveCallRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: LeaveCallVariables): MutationRef<LeaveCallData, LeaveCallVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: LeaveCallVariables): MutationRef<LeaveCallData, LeaveCallVariables>;
  operationName: string;
}
export const leaveCallRef: LeaveCallRef;

export function leaveCall(vars: LeaveCallVariables): MutationPromise<LeaveCallData, LeaveCallVariables>;
export function leaveCall(dc: DataConnect, vars: LeaveCallVariables): MutationPromise<LeaveCallData, LeaveCallVariables>;

interface ListCallParticipantsRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: ListCallParticipantsVariables): QueryRef<ListCallParticipantsData, ListCallParticipantsVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: ListCallParticipantsVariables): QueryRef<ListCallParticipantsData, ListCallParticipantsVariables>;
  operationName: string;
}
export const listCallParticipantsRef: ListCallParticipantsRef;

export function listCallParticipants(vars: ListCallParticipantsVariables, options?: ExecuteQueryOptions): QueryPromise<ListCallParticipantsData, ListCallParticipantsVariables>;
export function listCallParticipants(dc: DataConnect, vars: ListCallParticipantsVariables, options?: ExecuteQueryOptions): QueryPromise<ListCallParticipantsData, ListCallParticipantsVariables>;

