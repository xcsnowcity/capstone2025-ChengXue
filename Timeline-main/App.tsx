import React from 'react';
import * as SplashScreen from 'expo-splash-screen';
import AppContainer from 'Page/AppContainer';

SplashScreen.preventAutoHideAsync()
  .then(result => console.log(`SplashScreen.preventAutoHideAsync() succeeded: ${result}`))
  .catch(console.warn); // it's good to explicitly catch and inspect any error

export default class App extends React.PureComponent {
  componentDidMount() {
    setTimeout(async () => {
      await SplashScreen.hideAsync();
    }, 1000);
  }

  render() {
    return <AppContainer {...this.props} />;
  }
}
