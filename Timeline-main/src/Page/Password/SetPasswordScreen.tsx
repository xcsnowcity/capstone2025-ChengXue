import AsyncStorage from '@react-native-async-storage/async-storage';
import React, { useCallback } from 'react';
import { StyleSheet, View } from 'react-native';
import BgView from 'Components/BgView';
import PasswordView from 'Components/PasswordView';
import { TextView } from 'Components/TextView';
import TitleBar from 'Components/TitleBar';
import { RouterReplace } from 'Router/RouterAction';
import { AsyncKey } from 'Utils/Constants';

/**
 * 设置密码页面
 */
export function SetPasswordScreen() {
  /**
   * Save password and jump to weather page
   */
  const onPressNext = useCallback((password: string) => {
    AsyncStorage.setItem(AsyncKey.password, password);
    RouterReplace('Weather', null);
  }, []);

  return (
    <BgView style={styles.container}>
      <TitleBar title={'Your security and privacy is our first concern'} />
      <TextView style={styles.title}>
        Please set your 4-digit Pin to protect your privacy. Keep the Pin in mind and you will need to enter it before each use of the App.
        A weather screen is displayed by default, and a long press on the TimeLine Logo at the top will bring up the unlock page.
      </TextView>
      <View style={{ alignItems: 'center', marginTop: 20 }}>
        <PasswordView onPressNext={onPressNext} />
      </View>
    </BgView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  button: {
    marginBottom: 50,
  },
  buttonTitle: {
    fontSize: 16,
  },
  title: {
    marginHorizontal: 30,
    marginTop: 70,
  },
  iconContainer: {
    alignItems: 'center',
    marginTop: 40,
  },
  boldText: {
    fontWeight: 'bold',
  },
});
