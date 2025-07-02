import React from 'react';
import { View, StyleSheet, Text } from 'react-native';

interface Props {
  title: string;
}
export default class TitleBar extends React.PureComponent<Props> {
  render() {
    const { title } = this.props;
    return (
      <View style={styles.container}>
        <Text style={styles.title}>{title}</Text>
      </View>
    );
  }
}
const styles = StyleSheet.create({
  container: {
    marginLeft: 25,
    marginTop: 45,
  },
  title: {
    fontSize: 24,
    color: '#000',
    fontWeight: 'bold',
  },
});
