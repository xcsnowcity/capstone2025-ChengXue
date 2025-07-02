import { ToastAndroid } from 'react-native';

export function toast(msg) {
  ToastAndroid.showWithGravityAndOffset(msg, ToastAndroid.SHORT, ToastAndroid.CENTER, 0, 0);
}
