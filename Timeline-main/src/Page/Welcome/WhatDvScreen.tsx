import React from 'react';
import { Image, StyleSheet, TouchableOpacity, View, ScrollView, Text } from 'react-native';
import BgView from 'Components/BgView';
import TButton from 'Components/TButton';
import { TextView } from 'Components/TextView';
import TitleBar from 'Components/TitleBar';
import { RouterReplace } from 'Router/RouterAction';

// New Screen component for "What is Domestic Violence?",but not using it right now.
export function WhatDvScreen() {
  return (
    <BgView style={styles.container}>
      <ScrollView style={{ flex: 1 }}>
        <TitleBar title={'What is DV?'} />
        <TouchableOpacity
          style={{ position: 'absolute', top: 10, left: 15 }}
          onPress={() => {
            RouterReplace('Welcome', null);
          }}
        >
          <Image source={require('Image/ic_back.png')} />
        </TouchableOpacity>

        <TextView style={styles.title}>
          Domestic Violence is not just physical, but also about control.
        </TextView>

        <View style={styles.picContainer}>
          <Image
            source={require('Image/ic_result.png')}
            style={styles.image}
            resizeMode="contain"
          />
        </View>

        <TextView style={styles.desc}>
          This picture is called the Violence Wheel. By studying the wheel, you can understand how abusers commit these terrible behaviours.{"\n"}
          {"\n"}
          The Power and Control wheel has eight segments, each covering a specific violence category:{"\n"}
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

        <View style={styles.container} />

        <TButton
          style={styles.button}
          title={'Next'}
          onPress={() => {
            RouterReplace('SetPassword', null);
          }}
        />
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
    marginTop: 90,
  },
  picContainer: {
    alignItems: 'center',
    marginTop: 40,
    width: '100%',
    height: 350,
    marginBottom: 10,
  },
  image: {
    width: '100%',
    height: '100%',
  },
  desc: {
    marginHorizontal: 30,
    marginTop: 10,
    marginBottom: 10,
  },
  boldText: {
    fontWeight: 'bold',
  },
});