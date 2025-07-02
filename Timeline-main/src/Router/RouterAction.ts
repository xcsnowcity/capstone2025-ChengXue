import { CommonActions, StackActions } from '@react-navigation/native';

let currentNavigator: any = null;

export const SetCurrentNavigator = navigationRef => {
  navigationRef && (currentNavigator = navigationRef);
};

const navigate = (screenName, params?: any) => {
  currentNavigator.dispatch(
    CommonActions.navigate({
      name: screenName,
      params,
    }),
  );
};

export const RouterPop = (count = 1) => {
  currentNavigator.dispatch(StackActions.pop(count));
};

export const RouterPopToPop = () => {
  currentNavigator.dispatch(StackActions.popToTop());
};

export const RouterToPage = (pageKey, params) => {
  navigate(pageKey, params);
};

export const RouterReplace = (routeName, params) => {
  currentNavigator.dispatch(StackActions.replace(routeName, params));
};
