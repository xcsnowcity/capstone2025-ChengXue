import React from 'react';
import { StyleSheet, View } from 'react-native';
import BgView from 'Components/BgView';
import TButton from 'Components/TButton';
import { TextView } from 'Components/TextView';
import TitleBar from 'Components/TitleBar';
import { RouterReplace } from 'Router/RouterAction';

/**
 *  What’s Domestic Violence?
 */
export function QuestionScreen() {
  return (
    <BgView style={styles.container}>
      <TitleBar title={'What’s Domestic Violence?'} />
      <TextView style={styles.title}>
        As of January 2023, 5.2% of males and 14.8% of females report being victims of domestic violence in the past
        year.
      </TextView>
      <TextView style={{ marginHorizontal: 30, marginTop: 15 }}>
        Source: A survey in 19 European countries by the Domestic Abuse and Violence International
        Alliance:http://endtodv.org/davia/
      </TextView>
      <TextView style={{ marginHorizontal: 30, marginTop: 15 }}>
        Next there will be a questionnaire to assess whether you are at risk of domestic violence, which you can skip at
        any time.
      </TextView>
      <View style={styles.container} />
      <TButton
        title={'Next'}
        onPress={() => {
          RouterReplace('Answer', null);
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
    marginTop: 40,
  },
  iconContainer: {
    alignItems: 'center',
    marginTop: 40,
  },
});
