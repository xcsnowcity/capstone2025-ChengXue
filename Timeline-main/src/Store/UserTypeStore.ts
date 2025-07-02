import AsyncStorage from '@react-native-async-storage/async-storage';
import { action, makeObservable, observable, runInAction } from 'mobx';

export const USER_TYPE_KEY = 'user_type_key';

export default class UserTypeStore {
  @observable userType?: string = undefined;

  private static instance: UserTypeStore;

  private constructor() {
    makeObservable(this);
    this.initUserTypeData();
  }

  private async initUserTypeData() {
    try {
      const userType = await AsyncStorage.getItem(USER_TYPE_KEY);
      console.log("Retrieved userType from storage:", userType);
      runInAction(() => {
        this.userType = userType || undefined;
      });
    } catch (error) {
      console.error("Failed to load user type from storage:", error);
    }
  }

  @action
  public setUserType(userType: string) {
    console.log("Setting userType:", userType);
    runInAction(() => {
      this.userType = userType;
    });
    AsyncStorage.setItem(USER_TYPE_KEY, userType);
  }

  public static getInstance() {
    if (!UserTypeStore.instance) {
      UserTypeStore.instance = new UserTypeStore();
    }
    return UserTypeStore.instance;
  }
}
