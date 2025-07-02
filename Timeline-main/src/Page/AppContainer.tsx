import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { observer } from 'mobx-react';
import React from 'react';
import { Platform, StatusBar, View } from 'react-native';
import { SetCurrentNavigator } from 'Router/RouterAction';
import RouterTable, { WelcomeTable } from 'Router/RouterTable';
import AuthenticationStore, { AuthenticationStatus } from 'Store/AuthenticationStore';

const MainStack = createStackNavigator();
const navOption: any = {
  headerMode: 'screen',
  headerTintColor: '#666',
  cardStyle: {
    backgroundColor: 'white',
  },
  headerTitleStyle: {
    color: '#333',
    textAlign: 'center',
    fontSize: 22,
    fontWeight: 'bold',
  },
  headerStyle: {
    backgroundColor: 'white',
    ...Platform.select({
      android: { height: StatusBar.currentHeight ?? 0 + 49 },
    }),
  },
};

@observer
export default class AppContainer extends React.Component {
  authenticationStore;
  navigationRef;
  constructor(props) {
    super(props);
    this.authenticationStore = AuthenticationStore.getInstance();
  }

  renderScreens() {
    switch (this.authenticationStore.authenticationStatus) {
      // 没有回答过问题
      case AuthenticationStatus.unauthorized:
        return (
          <MainStack.Navigator
            screenOptions={({ route, navigation }) => {
              this.navigationRef = navigation;
              SetCurrentNavigator(navigation);
              return navOption;
            }}
          >
            {Object.keys(WelcomeTable).map(key => {
              const { screen } = WelcomeTable[key];
              const { options = {} } = WelcomeTable[key];
              return (
                <MainStack.Screen
                  key={key}
                  name={key}
                  component={screen}
                  options={({ route, navigation }) => {
                    return {
                      ...options,
                      headerTitleAlign: 'center',
                    };
                  }}
                />
              );
            })}
          </MainStack.Navigator>
        );
      // 回答过问题
      case AuthenticationStatus.authorized:
        return (
          <MainStack.Navigator
            screenOptions={({ route, navigation }) => {
              this.navigationRef = navigation;
              SetCurrentNavigator(navigation);
              return navOption;
            }}
          >
            {Object.keys(RouterTable).map(key => {
              const { screen } = RouterTable[key];
              const { options = {} } = RouterTable[key];
              return (
                <MainStack.Screen
                  key={key}
                  name={key}
                  component={screen}
                  options={({ route, navigation }) => {
                    return {
                      ...options,
                      headerTitleAlign: 'center',
                    };
                  }}
                />
              );
            })}
          </MainStack.Navigator>
        );
      default:
        return (
          <MainStack.Navigator
            screenOptions={({ route, navigation }) => {
              this.navigationRef = navigation;
              SetCurrentNavigator(navigation);
              return navOption;
            }}
          >
            <MainStack.Screen key={'none'} name={'none'} component={() => <View />} options={{ headerShown: false }} />
          </MainStack.Navigator>
        );
    }
  }

  render() {
    return <NavigationContainer independent>{this.renderScreens()}</NavigationContainer>;
  }
}
