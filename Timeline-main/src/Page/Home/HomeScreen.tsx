import React, { useState } from 'react';
import { Image, ScrollView, StyleSheet, TextInput, TouchableOpacity, View } from 'react-native';
import BgView from 'Components/BgView';
import { TextView } from 'Components/TextView';
import TitleBar from 'Components/TitleBar';
import { RouterPop, RouterReplace, RouterToPage } from 'Router/RouterAction';
import UserTypeStore from 'Store/UserTypeStore';
import serviceData from 'Components/ServiceData';
import { Text } from 'react-native';

type UserType = 'Male' | 'Female' | 'Others' | 'Youth';
console.log(UserTypeStore.getInstance() === UserTypeStore.getInstance());

const descriptions: Record<UserType, string> = {
  'Male': 'Men\’s Aid revealed that approximately 8,000 contacts to the service were received since January 1, 2021. Don’t feel shame and fear. Get supportive information and live a healthy life.',
  'Female': 'In the EU, roughly 1 in 3 women has experienced various forms of domestic violence. The EU works continuously to combat this issue through policies, legislation, and awareness-raising activities.You’re not alone.',
  'Others': 'You\’re not alone, Others warriors. Your strength is powerful. Reach out, break the silence, and reclaim your safety. You can overcome.',
  'Youth': 'You\’re brave, young hearts. Your voice matters in ending family violence. Speak up, seek help, and shape a safer home. You hold the key to change.'
};
const userImages: Record<UserType, any> = {
  'Male': require('Image/ic_person.png'),
  'Female': require('Image/ic_person.png'),
  'Others': require('Image/ic_nonb.png'),
  'Youth': require('Image/ic_teen.png')
};




const defaultConfig = [
  {
    icon: require('Image/ic_icon4.png'),
    title: 'Domestic Abuse Support',
    onPress: () => {
      RouterToPage('DomesticAbuse', null);
    },
  },
  {
    icon: require('Image/ic_icon3.png'),
    title: 'Legal Services',
    onPress: () => {
      RouterToPage('Legal', null);
    },
  },
  {
    icon: require('Image/ic_icon2.png'),
    title: 'Housing',
    onPress: () => {
      RouterToPage('Housing', null);
    },
  },
  {
    icon: require('Image/ic_icon6.png'),
    title: 'Financial',
    onPress: () => {
      RouterToPage('Financial', null);
    },
  },
  {
    icon: require('Image/ic_icon5.png'),
    title: 'Family Services',
    onPress: () => {
      RouterToPage('FamilyService', null);
    },
  },
  {
    icon: require('Image/ic_icon1.png'),
    title: 'Mental Well-being Support',
    onPress: () => {
      RouterToPage('Mental', null);
    },
  },
  {
    icon: require('Image/ic_icon8.png'),
    title: 'How to Support',
    onPress: () => {
      RouterToPage('HowtoSupport', null);
    },
  },
  {
    icon: require('Image/ic_icon7.png'),
    title: 'Education and Employment',
    onPress: () => {
      RouterToPage('EducationEmployment', null);
    },
  },
];

const teenagerChildConfig = [
  {
    icon: require('Image/ic_icon8.png'),
    title: 'How to Support',
    onPress: () => {
      RouterToPage('HowtoSupport', null);
    },
  },
  {
    icon: require('Image/ic_icon10.png'),
    title: 'Parenting',
    onPress: () => {
      RouterToPage('Parenting', null);
    },
  },
  {
    icon: require('Image/ic_icon1.png'),
    title: 'Mental Well-being Support',
    onPress: () => {
      RouterToPage('Mental', null);
    },
  },
  {
    icon: require('Image/ic_icon7.png'),
    title: 'Education',
    onPress: () => {
      RouterToPage('EducationEmployment', null);
    },
  },
];


export function HomeScreen() {

  //Search function
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);

  //Print LOG
  const searchServiceData = (searchTerm) => {
    const results = serviceData.filter(service =>
      service.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      service.description.toLowerCase().includes(searchTerm.toLowerCase())
    );

    console.log(results);
  }
  searchServiceData('counselling');


  const userType = UserTypeStore.getInstance().userType;
  console.log("HomeScreen userType:", userType);
  if (!userType) {
    // Handle the case where userType is undefined, maybe navigate back or show an error
    return null;
  }
  const description = descriptions[userType];
  const userImage = userImages[userType];
  const homeConfig = userType === 'Youth' ? teenagerChildConfig : defaultConfig;

  return (
    <BgView style={styles.container}>
      <ScrollView>
        <View>
          <TouchableOpacity
            style={{ position: 'absolute', top: 10, left: 15 }}
            onPress={() => {
              RouterReplace('Answer', null);
            }}
          >
            <Image source={require('Image/ic_back.png')} />
          </TouchableOpacity>
          <TitleBar title={'Did you know?'} />
          <TextView style={styles.desc}>
            {description}
          </TextView>
          <View style={styles.iconContainer}>
            <Image source={userImage} />
          </View>

          <View style={{ flexDirection: 'row-reverse', marginTop: 10 }}>
            <TouchableOpacity
              style={styles.exit}
              onPress={() => {
                RouterReplace('Weather', null);
              }}
            >
              <Image source={require('Image/ic_exit_left.png')} />
              <Image source={require('Image/ic_exit_right.png')} />
            </TouchableOpacity>
          </View>
          <View style={{ backgroundColor: '#ccc' }}>
            <View style={styles.searchContainer}>
              <Image source={require('Image/ic_search.png')} />
              <TextInput
                placeholder={'Search: Living with Crisis'}
                style={{ marginLeft: 10 }}
                onChangeText={(text) => {
                  if (text.trim() === '') {
                    setSearchResults([]);
                    setShowDropdown(false);
                  } else {
                    const results = serviceData.filter(service => {
                      return service.title.toLowerCase().includes(text.toLowerCase()) ||
                        service.description.toLowerCase().includes(text.toLowerCase());
                    });
                    setSearchResults(results);
                    setShowDropdown(results.length > 0);
                  }
                }}
              />
            </View>
            {showDropdown &&
              <View style={{ backgroundColor: 'rgb(255,255,255)', marginTop: 10 }}>
                {searchResults.map((result, index) => (
                  <Text key={index}>{result.title}</Text>
                ))}
              </View>
            }

            <View style={{ marginTop: 30 }}>
              {homeConfig.map((item, index) => {
                return (
                  <TouchableOpacity style={styles.touchContainer} onPress={item.onPress} key={`${item.title}`}>
                    <Image source={item.icon} />
                    <TextView style={{ marginLeft: 15 }}>{item.title}</TextView>
                  </TouchableOpacity>
                );
              })}
            </View>
          </View>
        </View>
      </ScrollView>
    </BgView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  desc: {
    marginHorizontal: 30,
    marginTop: 10,
  },
  iconContainer: {
    alignItems: 'center',
    marginTop: 30,
  },
  searchContainer: {
    height: 40,
    backgroundColor: 'white',
    borderRadius: 20,
    marginHorizontal: 10,
    marginTop: 20,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  touchContainer: {
    marginBottom: 10,
    height: 48,
    alignItems: 'center',
    flexDirection: 'row',
    paddingHorizontal: 20,
  },
  exit: {
    backgroundColor: 'red',
    width: 48,
    height: 48,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 15,
    borderRadius: 24,
    flexDirection: 'row',
  },
});
