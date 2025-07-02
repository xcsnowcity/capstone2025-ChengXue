import AsyncStorage from '@react-native-async-storage/async-storage';
import { action, makeObservable, observable, runInAction } from 'mobx';
import { isEmptyValue } from 'Utils/DataTool';

export enum AuthenticationStatus {
  authorized = 'authorized',
  unauthorized = 'unauthorized',
  none = 'none',
}

/**
 * First entering key
 */
export const FIRST_COME = 'first_come_in';

export default class AuthenticationStore {
  /**
   * if first entering, the status is none
   */
  @observable authenticationStatus?: AuthenticationStatus = AuthenticationStatus.none;
  private static sInstance: AuthenticationStore;

  private constructor() {
    makeObservable(this);
    this.initRNData();
  }

  private initRNData = () => {
    // if first entering, the status is none
    AsyncStorage.getItem(FIRST_COME).then(data => {
      this.authenticationStatus = isEmptyValue(data)
        ? AuthenticationStatus.unauthorized
        : AuthenticationStatus.authorized;
    });
  };

  @action
  public changeStatus(status: AuthenticationStatus) {
    runInAction(() => {
      this.authenticationStatus = status;
    });
    AsyncStorage.setItem(FIRST_COME, 'true');
  }

  /**
   * 获取单列
   */
  public static getInstance() {
    if (!AuthenticationStore.sInstance) {
      AuthenticationStore.sInstance = new AuthenticationStore();
    }
    return AuthenticationStore.sInstance;
  }
}
