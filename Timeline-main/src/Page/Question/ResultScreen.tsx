import React from 'react';
import { Image, ScrollView, StyleSheet, Text, View } from 'react-native';
import BgView from 'Components/BgView';
import TButton from 'Components/TButton';
import { TextView } from 'Components/TextView';
import TitleBar from 'Components/TitleBar';
import { RouterReplace } from 'Router/RouterAction';
import AuthenticationStore, { AuthenticationStatus } from 'Store/AuthenticationStore';

/**
 *  Result
 */
export function ResultScreen({ route }) {
  const userAnswers = route.params;
  let additionalInfo1 = '';
  let additionalInfo2 = '';
  let additionalInfo3 = '';
  // Verbal & Emotional Abuse
  if (userAnswers['1'] === 'Yes' || userAnswers['2'] === 'Yes' || userAnswers['3'] === 'Yes' || userAnswers['4'] === 'Yes' || userAnswers['5'] === 'Yes' || userAnswers['6'] === 'Yes' || userAnswers['7'] === 'Yes' || userAnswers['8'] === 'Yes' || userAnswers['9'] === 'Yes' || userAnswers['10'] === 'Yes' || userAnswers['11'] === 'Yes' || userAnswers['12'] === 'Yes') {
    additionalInfo1 += 'Based on your answers, you may face domestic violence. Your partner may show the following signs of domestic violence:\n'
    additionalInfo2 += 'You\'re not alone. Reach out, take the first step towards safety and support.\n'
    additionalInfo3 += 'If you or someone else is in an emergency, please contact Garda Síochána on 112.\n';
  }
  if (userAnswers['1'] === 'Yes') {
    additionalInfo1 += '• Verbal & Emotional Abuse\n';
  }
  // Control & Isolation
  if (userAnswers['2'] === 'Yes') {
    additionalInfo1 += '• Control & Isolation\n';
  }
  // Emotional Manipulation & Fear Induction
  if (userAnswers['3'] === 'Yes') {
    additionalInfo1 += '• Emotional Manipulation & Fear Induction\n';
  }
  // Anger & Aggression
  if (userAnswers['4'] === 'Yes') {
    additionalInfo1 += '• Anger & Aggression\n';
  }
  // Financial Control
  if (userAnswers['5'] === 'Yes') {
    additionalInfo1 += '• Financial Control\n';
  }
  // Physical Abuse & Child Endangerment
  if (userAnswers['6'] === 'Yes') {
    additionalInfo1 += '• Physical Abuse & Child Endangerment\n';
  }
  // Denial & Victim Blaming
  if (userAnswers['7'] === 'Yes') {
    additionalInfo1 += '• Denial & Victim Blaming\n';
  }
  // Property Destruction & Animal Cruelty
  if (userAnswers['8'] === 'Yes') {
    additionalInfo1 += '• Property Destruction & Animal Cruelty\n';
  }
  // Weaponized Threats & Intimidation
  if (userAnswers['9'] === 'Yes') {
    additionalInfo1 += '• Weaponized Threats & Intimidation\n';
  }
  // Sexual Coercion & Abuse
  if (userAnswers['10'] === 'Yes') {
    additionalInfo1 += '• Sexual Coercion & Abuse\n';
  }
  // Jealousy & Accusation
  if (userAnswers['11'] === 'Yes') {
    additionalInfo1 += '• Jealousy & Accusation\n';
  }
  // Manipulative Threats & Severe Emotional Manipulation
  if (userAnswers['12'] === 'Yes') {
    additionalInfo1 += '• Manipulative Threats & Severe Emotional Manipulation\n';
  }

  return (
    <BgView style={styles.container} source={require('Image/ic_red_bg.png')}>
      <ScrollView>
        <TitleBar title={'Result'} />
        <View style={styles.iconContainer}>
          <Image source={require('Image/ic_wel_icon.png')} />
        </View>
        <TextView style={styles.title}>{
          'Domestic Violence is not just physical, but also about control. The society is contributing to overcoming domestic violence.\n'
        }
        </TextView>
        {additionalInfo1 ? <TextView style={styles.descRed}>{additionalInfo1}</TextView> : null}
        <TextView style={styles.desc}>
          {additionalInfo2}
        </TextView>
        <TextView style={styles.descRed}>
          {additionalInfo3}
        </TextView>
        <TextView style={styles.desc}>
          {'Ellen Pence and others created the Power and Control wheel, used by many to demonstrate the workings of domestic violence.It\'s also called the Violence Wheel. By studying the wheel, you can understand how abusers commit these terrible crimes.'}
        </TextView>
        <View style={styles.picContainer}>
          <Image
            source={require('Image/ic_result.png')}
            style={styles.image}
            resizeMode="contain"
          />
        </View>

        <TextView style={styles.desc}>
          {"\n"}The Power and Control wheel has eight segments, each covering a specific violence category:
          {"\n"}{"\n"}
          <Text style={styles.boldText}>• Coercion & Threats {"\n"}</Text> Trying to control the victim through threats
          {"\n"}{"\n"}
          <Text style={styles.boldText}>• Intimidation {"\n"}</Text> May inflict harm to make the victim afraid
          {"\n"}{"\n"}
          <Text style={styles.boldText}>• Emotional Abuse {"\n"}</Text> Psychologically attacking the victim
          {"\n"}{"\n"}
          <Text style={styles.boldText}>• Isolation {"\n"}</Text> Controlling the victim's behaviors and social interactions
          {"\n"}{"\n"}
          <Text style={styles.boldText}>• Denying, Blaming, and Minimizing {"\n"}</Text> No remorse or empathy
          {"\n"}{"\n"}
          <Text style={styles.boldText}>• Using Children {"\n"}</Text> Hurting the victim through children
          {"\n"}{"\n"}
          <Text style={styles.boldText}>• Economic Abuse {"\n"}</Text> Controlling family income and finances
          {"\n"}{"\n"}
          <Text style={styles.boldText}>• Gender Privilege {"\n"}</Text> Unfair treatment based on gender
          {"\n"}
        </TextView>

        <TButton
          title={'Next'}
          onPress={() => {
            RouterReplace('BasicInformation', null);
          }}
          style={styles.button}
        />
        <View style={styles.container} />
      </ScrollView>
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
    fontSize: 16,
  },
  iconContainer: {
    alignItems: 'center',
    marginTop: 40,
  },
  desc: {
    marginHorizontal: 30,
    marginTop: 0,
    fontSize: 16,
  },
  descRed: {
    marginHorizontal: 30,
    marginTop: 0,
    fontSize: 16,
    color: 'red',
  },
  picContainer: {
    alignItems: 'center',
    marginTop: 20,
    width: '100%',
    height: 350,
    marginBottom: 20,
  },
  image: {
    width: '100%',
    height: '100%',
  },
  boldText: {
    fontWeight: 'bold',
  },
});
