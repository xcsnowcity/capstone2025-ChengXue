import React from 'react';
import { View, StyleSheet, Image } from 'react-native';

interface Props {
  children: any;
  style?: any;
  source?: any;
}

export default class BgView extends React.PureComponent<Props> {
  render() {
    const { children, style, source } = this.props;
    return (
      <View style={[styles.container, style]}>
        <Image style={styles.topIcon} source={source ?? require('Image/ic_bg_top.png')} />
        {children}
      </View>
    );
  }
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  topIcon: {
    position: 'absolute',
    left: 0,
    top: 0,
  },
});
