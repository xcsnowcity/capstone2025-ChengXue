import React, { useCallback, useEffect, useState } from 'react';
import { Dimensions, Image, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { getLocation, getWeather, showWeather } from 'react-native-weather-api';
import BgView from 'Components/BgView';
import { TextView } from 'Components/TextView';
import { RouterReplace } from 'Router/RouterAction';
import { permissionHelper } from './BookPermissionHelper';
import AuthenticationStore, { AuthenticationStatus } from 'Store/AuthenticationStore';

const { width } = Dimensions.get('window');

/**
 * Weather Page
 * Press the logo and jump to password pad page
 */
export function WeatherScreen() {
  // Current Location Data
  const [data, setData] = useState<any>(null);
  // Galway Location Data
  const [galwayData, setGalwayData] = useState<any>(null);
  // Show tutorial
  const [showTutorial, setShowTutorial] = useState(false);

  const fetchPermission = useCallback(async () => {
    getWeather({
      key: 'e9763cee4abdb26bb1869c3fd70a1a8b',
      city: 'Dublin',
      country: "IE",
      unit: 'metric',
    })
      .then(status => {
        // eslint-disable-next-line new-cap
        const weather = new showWeather();
        setData(weather);
      })
      .catch(err => { });
  }, []);

  // Fetch Galway's Location date
  const fetchGalwayWeather = useCallback(async () => {
    getWeather({
      key: 'e9763cee4abdb26bb1869c3fd70a1a8b',
      city: 'Galway',
      country: "Ireland",
      unit: 'metric',
    })
      .then(status => {
        // eslint-disable-next-line new-cap
        const weather = new showWeather();
        setGalwayData(weather);
      })
      .catch(err => { });
  }, []);

  useEffect(() => {
    const { authenticationStatus } = AuthenticationStore.getInstance();
    if (authenticationStatus === AuthenticationStatus.unauthorized) {
      setShowTutorial(true);
    }
    setTimeout(() => {
      fetchPermission();
      fetchGalwayWeather();
    }, 200);
  }, []);

  return (
    <BgView style={styles.container}>
      {showTutorial && (
        <View style={styles.tutorialOverlay}>
          <Text style={styles.tutorialText}>This app normally opens as a weather app by default. Long press the logo on the top to call out the unlock screen.</Text>
          <TouchableOpacity style={styles.closeTutorialButton} onPress={() => setShowTutorial(false)}>
            <Text>Got it</Text>
          </TouchableOpacity>
        </View>
      )}
      <View style={styles.top}>
        <TouchableOpacity
          onLongPress={() => {
            RouterReplace('InputPassword', null);
          }}
        >
          <Image source={require('Image/ic_we_logo.png')} />
        </TouchableOpacity>
        <TextView style={styles.title}>Timeline Weather</TextView>
      </View>
      <View style={{ marginTop: 40 }}>
        <Image source={require('Image/ic_we_bg.png')} style={styles.bg} resizeMode={'contain'} />
        <TextView style={styles.temp}>{Math.round(data?.temp ?? '0')}°</TextView>
        <TextView style={styles.temp2}>
          H:{Math.round(data?.temp_max ?? '0')}° L:{Math.round(data?.temp_min ?? '0')}°{' '}
        </TextView>
        <TextView style={styles.name}>{data?.name ?? ''}</TextView>
        <Image style={styles.icon} source={{ uri: data?.icon }} />
        <TextView style={styles.weName}>{data?.description ?? ''}</TextView>
      </View>
      {/*add galway location weather card */}
      <View style={{ marginTop: 40 }}>
        <Image source={require('Image/ic_we_bg.png')} style={styles.bg} resizeMode={'contain'} />
        <TextView style={styles.temp}>{Math.round(galwayData?.temp ?? '0')}°</TextView>
        <TextView style={styles.temp2}>
          H:{Math.round(galwayData?.temp_max ?? '0')}° L:{Math.round(galwayData?.temp_min ?? '0')}°{' '}
        </TextView>
        <TextView style={styles.name}>{galwayData?.name ?? ''}</TextView>
        <Image style={styles.icon} source={{ uri: galwayData?.icon }} />
        <TextView style={styles.weName}>{galwayData?.description ?? ''}</TextView>
      </View>
      {/* <TextView style={{ fontSize: 12, marginTop: 40, marginHorizontal: 30 }}>
        {data ? JSON.stringify(data) : ''}
      </TextView> */}
    </BgView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  top: {
    alignItems: 'center',
    marginTop: 50,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#E54B0B',
  },
  bg: {
    width: width - 20,
    aspectRatio: 342 / 184,
    position: 'absolute',
    left: 10,
    top: 0,
  },
  temp: {
    marginLeft: 40,
    marginTop: 20,
    fontSize: 60,
    color: 'white',
  },
  temp2: {
    marginLeft: 40,
    fontSize: 14,
    color: '#EBEBF599',
  },
  name: {
    marginLeft: 40,
    color: 'white',
  },
  icon: {
    position: 'absolute',
    width: 100,
    height: 100,
    right: 30,
  },
  weName: {
    position: 'absolute',
    right: 30,
    bottom: 0,
    color: 'white',
    fontSize: 16,
  },
  tutorialOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)', // semi-transparent
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 999, // ensure the tutorial is on top
  },
  tutorialText: {
    color: 'white',
    fontSize: 20,
    marginBottom: 20,
  },
  closeTutorialButton: {
    padding: 10,
    backgroundColor: 'white',
    borderRadius: 5,
  }

});
