import React, { useCallback, useEffect, useState } from 'react';
import { Image, ImageBackground, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import BgView from 'Components/BgView';
import { TextView } from 'Components/TextView';
import TitleBar from 'Components/TitleBar';
import { RouterPop } from 'Router/RouterAction';
import serviceData from 'Components/ServiceData';
import { Linking } from 'react-native';
import UserTypeStore from 'Store/UserTypeStore';
/**
 * ParentingScreen
 * 
*/
export function ParentingScreen() {
  const [step, setStep] = useState(0);
  const UserType = UserTypeStore.getInstance().userType;
  if (!UserType) {
    // Handle the case where userType is undefined, maybe navigate back or show an error
    return null;
  }
  type users = 'Male' | 'Female' | 'Others' | 'Youth';
  const housingServices = serviceData.filter(service =>
    service.serviceType.includes("Parenting") &&
    service.users.includes(UserType)
  ); const imageMap = {
    "Image/serviceLogo/COPE_Galway_Homeless_Services.png": require('Image/serviceLogo/COPE_Galway_Homeless_Services.png'),
    "Image/serviceLogo/Counselling_in_Primary_Care.png": require('Image/serviceLogo/Counselling_in_Primary_Care.png'),
    "Image/serviceLogo/Family_Law_Court.png": require('Image/serviceLogo/Family_Law_Court.png'),
    "Image/serviceLogo/FORUM_Connemara.png": require('Image/serviceLogo/FORUM_Connemara.png'),
    "Image/serviceLogo/Galway_Traveller_Movement.png": require('Image/serviceLogo/Galway_Traveller_Movement.png'),
    "Image/serviceLogo/Garda_Síochána.png": require('Image/serviceLogo/Garda_Síochána.png'),
    "Image/serviceLogo/Jigsaw.png": require('Image/serviceLogo/Jigsaw.png'),
    "Image/serviceLogo/Legal_Aid.png": require('Image/serviceLogo/Legal_Aid.png'),
    "Image/serviceLogo/Money_Advice.png": require('Image/serviceLogo/Money_Advice.png'),
    "Image/serviceLogo/No_4_Youth_Service.png": require('Image/serviceLogo/No_4_Youth_Service.png'),
    "Image/serviceLogo/Parenting_After_Domestic_Violence.png": require('Image/serviceLogo/Parenting_After_Domestic_Violence.png'),
    "Image/serviceLogo/Parenting_Positively.png": require('Image/serviceLogo/Parenting_Positively.png'),
    "Image/serviceLogo/Parents_Plus.png": require('Image/serviceLogo/Parents_Plus.png'),
    "Image/serviceLogo/Pieta_House.png": require('Image/serviceLogo/Pieta_House.png'),
    "Image/serviceLogo/Rainbows.png": require('Image/serviceLogo/Rainbows.png'),
    "Image/serviceLogo/Simon_Community.png": require('Image/serviceLogo/Simon_Community.png'),
    "Image/serviceLogo/Social_Welfare.png": require('Image/serviceLogo/Social_Welfare.png'),
    "Image/serviceLogo/Solas_Og.png": require('Image/serviceLogo/Solas_Og.png'),
    "Image/serviceLogo/The_National_Childcare_Scheme.png": require('Image/serviceLogo/The_National_Childcare_Scheme.png'),
    "Image/serviceLogo/The_National_Male_Advice_Line.png": require('Image/serviceLogo/The_National_Male_Advice_Line.png'),
    "Image/serviceLogo/TUSLA_Family_Services.png": require('Image/serviceLogo/TUSLA_Family_Services.png'),
    "Image/serviceLogo/TUSLA_Social_Work.png": require('Image/serviceLogo/TUSLA_Social_Work.png'),
    "Image/serviceLogo/Western_Region_Drug_and_Alcohol_Task_Force_Family_Support.png": require('Image/serviceLogo/Western_Region_Drug_and_Alcohol_Task_Force_Family_Support.png'),
    "Image/serviceLogo/Your_Mental_Health_information_line.png": require('Image/serviceLogo/Your_Mental_Health_information_line.png'),
    "Image/serviceLogo/Youth_Work_Ireland_Counselling.png": require('Image/serviceLogo/Youth_Work_Ireland_Counselling.png'),
    "Image/serviceLogo/AMACH_LGBTI_Galway.png": require('Image/serviceLogo/AMACH_LGBTI_Galway.png'),
    "Image/serviceLogo/Aware.png": require('Image/serviceLogo/Aware.png'),
    "Image/serviceLogo/Clann_Resource_Centre.png": require('Image/serviceLogo/Clann_Resource_Centre.png'),
    "Image/serviceLogo/Community_Welfare_Service.png": require('Image/serviceLogo/Community_Welfare_Service.png'),
    "Image/serviceLogo/DVR.png": require('Image/serviceLogo/DVR.png'),
  };
  const renderService = useCallback((service) => {
    return (
      <>
        <TextView style={styles.title}>{service.title}</TextView>
        <TextView style={styles.title2}>What is {service.title} </TextView>
        <TextView style={styles.desc}>{service.description}</TextView>
        <TextView style={styles.title2}>Contact</TextView>
        {service.otherContact && <TextView style={styles.desc}>Other Contact: {service.otherContact}</TextView>}
        {service.address && <TextView style={styles.desc}>Address: {service.address}</TextView>}
        {service.phone && (
          <TouchableOpacity onPress={() => Linking.openURL(`tel:${service.phone}`)}>
            <TextView style={[styles.desc, styles.clickableText]}>Phone: {service.phone}</TextView>
          </TouchableOpacity>
        )}
        {service.email && (
          <TouchableOpacity onPress={() => Linking.openURL(`mailto:${service.email}`)}>
            <TextView style={[styles.desc, styles.clickableText]}>Email: {service.email}</TextView>
          </TouchableOpacity>
        )}
        {service.website && (
          <TouchableOpacity onPress={() => Linking.openURL(service.website)}>
            <TextView style={[styles.desc, styles.clickableText]}>Website: {service.website}</TextView>
          </TouchableOpacity>
        )}
        <View style={{ marginVertical: 20, marginLeft: 30 }}>
          <View style={{ marginVertical: 20, marginLeft: 30 }}>
            <Image source={imageMap[service.image]} />
          </View>
        </View>
      </>
    );
  }, []);


  return (
    <BgView style={styles.container}>
      <ScrollView>
        <TouchableOpacity
          style={{ position: 'absolute', top: 10, left: 15 }}
          onPress={() => {
            RouterPop();
          }}
        >
          <Image source={require('Image/ic_back.png')} />
        </TouchableOpacity>
        <TitleBar title={'Parenting'} />
        {step < housingServices.length ? renderService(housingServices[step]) : null}
      </ScrollView>
      {step < housingServices.length - 1 && (
        <View style={styles.bottomRightContainer}>
          <TouchableOpacity onPress={() => setStep(step + 1)}>
            <Image source={require('Image/ic_next.png')} />
          </TouchableOpacity>
        </View>
      )}
      <View style={styles.progressBar}>
        {housingServices.map((_, index) => {
          return (
            <View
              key={`progress-${index}`}
              style={{
                width: 10,
                height: 10,
                borderRadius: 5,
                backgroundColor: index <= step ? '#50C2C9' : '#CCCCCC',
                marginHorizontal: 5,
              }}
            />
          );
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
    marginBottom: 50,
  },
  buttonTitle: {
    fontSize: 16,
  },
  title: {
    marginHorizontal: 30,
    marginTop: 40,
    fontWeight: 'bold',
    fontSize: 22,
  },
  title2: {
    marginHorizontal: 30,
    marginTop: 20,
    fontWeight: 'bold',
    fontSize: 20,
  },
  desc: {
    fontSize: 14,
    marginLeft: 30,
  },
  detail: {
    fontSize: 14,
    marginRight: 30,
    flex: 1,
  },
  iconContainer: {
    alignItems: 'center',
    marginTop: 40,
  },
  bottomRightContainer: {
    position: 'absolute',
    right: 10,
    bottom: 10,
  },
  clickableText: {
    color: 'blue',
    textDecorationLine: 'underline'
  },
  progressBar: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    position: 'absolute',
    bottom: 20,
    left: 0,
    right: 0,
  },
});
