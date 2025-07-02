import React from 'react';
import { Image, StyleSheet, View } from 'react-native';
import BgView from 'Components/BgView';
import TButton from 'Components/TButton';
import { TextView } from 'Components/TextView';
import TitleBar from 'Components/TitleBar';
import { RouterReplace } from 'Router/RouterAction';

// New Screen component for "What is Domestic Violence?", jump from WelcomeScreen once user click "Next" button, keep the same style as WelcomeScreen
export function DVInfoScreen() {
  return (
    <BgView style={styles.container}>
      <TitleBar title={'What is Domestic Violence?'} />
      <TextView style={styles.title}>
        Domestic violence is a pattern of behaviours used by one person to maintain power and control over another person
        in an intimate relationship.
      </TextView>
      <View style={styles.iconContainer}>
        <Image source={require('Image/ic_wel_icon.png')} />
      </View>
      <View style={styles.container} />
      <TButton
        title={'Next'}
        onPress={() => {
          RouterReplace('DVInfoScreen', null);
        }}
        style={styles.button}
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
  desc: {
    marginHorizontal: 30,
    marginTop: 10,
  },
});


