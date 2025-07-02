import React from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';
import BgView from 'Components/BgView';
import TButton from 'Components/TButton';
import { TextView } from 'Components/TextView';
import TitleBar from 'Components/TitleBar';
import { RouterReplace } from 'Router/RouterAction';

/**
 * welcome page
 */
export function WelcomeScreen() {
  return (
    <BgView style={styles.container}>
      <TitleBar title={'Welcome'} />
      <TextView style={styles.title}>
        Timeline is a prototype app to provide information to you to support you at this stressful time in your family’s
        life. The App does not store any personal data. It is designed to be used by you to get information and support.
      </TextView>
      <View style={styles.iconContainer}>
        <Image source={require('Image/ic_wel_icon.png')} />
      </View>
      <View style={styles.container} />
      <TButton
        style={styles.button}
        title={'Next'}
        onPress={() => {
          RouterReplace('SetPassword', null);
          {/*RouterReplace('BasicInformation', null)); 减少解锁次数用的*/ }
        }
        }
      />
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
    marginTop: 90,
  },
  iconContainer: {
    alignItems: 'center',
    marginTop: 40,
  },
});
