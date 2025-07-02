import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import BgView from 'Components/BgView';
import TButton from 'Components/TButton';
import { TextView } from 'Components/TextView';
import TitleBar from 'Components/TitleBar';
import { RouterReplace } from 'Router/RouterAction';
import AuthenticationStore, { AuthenticationStatus } from 'Store/AuthenticationStore';
import { AnswerList } from './AnswerConfig';
import UserTypeStore from 'Store/UserTypeStore';

/**
 *  BasicInformation
 * Asking gender, than based on the gender, go to male, female, and Others homescreens.
 */

export function BasicInformationScreen() {
  const data = {
    key: '13',
    title: 'Last Step',
    desc: 'For more personalised information, please anwser: Are you...?',
    buttons: [
      {
        title: 'Male',
        onPress: () => {
          UserTypeStore.getInstance().setUserType('Male');
          console.log("Setting user type to:", 'Male');
          AuthenticationStore.getInstance().changeStatus(AuthenticationStatus.authorized);
          setTimeout(() => {
            RouterReplace('Home', null);
          }, 0);
        },
      },
      {
        title: 'Female',
        onPress: () => {
          UserTypeStore.getInstance().setUserType('Female');
          console.log("Setting user type to:", 'Female');
          AuthenticationStore.getInstance().changeStatus(AuthenticationStatus.authorized);
          setTimeout(() => {
            RouterReplace('Home', null);
          }, 0);
        },
      },
      {
        title: 'Others',
        onPress: () => {
          UserTypeStore.getInstance().setUserType('Others');
          console.log("Setting user type to:", 'Others');
          AuthenticationStore.getInstance().changeStatus(AuthenticationStatus.authorized);
          setTimeout(() => {
            RouterReplace('Home', null);
          }, 0);
        },
      },
      {
        title: 'Youth',
        onPress: () => {
          UserTypeStore.getInstance().setUserType('Youth');
          console.log("Setting user type to:", 'Youth');
          AuthenticationStore.getInstance().changeStatus(AuthenticationStatus.authorized);
          setTimeout(() => {
            RouterReplace('Home', null);
          }, 0);
        },
      },
    ],
  };
  return (
    <BgView style={styles.container}>
      <TitleBar title={data.title} />
      <TextView style={styles.title}>{data.desc}</TextView>
      <View style={{ marginTop: 40 }}>
        {data.buttons.map(item => {
          console.log(UserTypeStore.getInstance() === UserTypeStore.getInstance());
          return <TButton key={`${item.title}`} title={item.title} onPress={item.onPress} style={styles.button} />;
        })}
      </View>
    </BgView>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  button: {
    marginBottom: 15,
  },
  buttonTitle: {
    fontSize: 16,
  },
  title: {
    marginHorizontal: 30,
    marginTop: 40,
  },
  iconContainer: {
    alignItems: 'center',
    marginTop: 40,
  },
});
