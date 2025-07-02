import AsyncStorage from '@react-native-async-storage/async-storage';
import React, { useCallback } from 'react';
import { Image, StyleSheet, View } from 'react-native';
import BgView from 'Components/BgView';
import PasswordView from 'Components/PasswordView';
import { TextView } from 'Components/TextView';
import { RouterReplace } from 'Router/RouterAction';
import AuthenticationStore, { AuthenticationStatus } from 'Store/AuthenticationStore';
import { AsyncKey } from 'Utils/Constants';
import { toast } from 'Utils/Toast';

/**
 * 输入密码页面
 */
export function InputPasswordScreen() {
  /**
   * 保存密码，然后跳转到weather页面
   */
  const onPressNext = useCallback(async (password: string) => {
    const passwordCache = await AsyncStorage.getItem(AsyncKey.password);
    if (passwordCache === password) {
      const { authenticationStatus } = AuthenticationStore.getInstance();
      if (authenticationStatus === AuthenticationStatus.authorized) {
        RouterReplace('Home', null);
      } else {
        RouterReplace('Question', null);
      }
    } else {
      toast('Incorrect PIN code');
    }
  }, []);

  return (
    <BgView style={styles.container}>
      <View style={{ alignItems: 'center', marginTop: 60 }}>
        <Image source={require('Image/ic_we_logo.png')} />
      </View>
      <TextView style={styles.title}>Please enter the Pin</TextView>
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
    marginTop: 30,
    fontWeight: 'bold',
  },
  iconContainer: {
    alignItems: 'center',
    marginTop: 40,
  },
});
