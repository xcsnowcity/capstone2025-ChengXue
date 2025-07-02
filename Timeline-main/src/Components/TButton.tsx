import React from 'react';
import { ActivityIndicator, StyleProp, StyleSheet, Text, TextStyle, TouchableOpacity, ViewStyle } from 'react-native';

interface Props {
  style?: StyleProp<ViewStyle>;
  isLoading?: boolean;
  titleStyle?: StyleProp<TextStyle>;
  title: string;
  onPress: () => void;
}
export default class TButton extends React.PureComponent<Props> {
  render() {
    const { style, isLoading, titleStyle, title, onPress } = this.props;
    return (
      <TouchableOpacity
        style={[styles.button, style]}
        onPress={() => {
          if (isLoading) {
            return;
          }
          onPress();
        }}
      >
        {isLoading ? (
          <ActivityIndicator size={'small'} color={'white'} />
        ) : (
          <Text style={[styles.title, titleStyle]}>{title}</Text>
        )}
      </TouchableOpacity>
    );
  }
}

const styles = StyleSheet.create({
  button: {
    height: 40,
    borderRadius: 20,
    backgroundColor: '#50C2C9CC',
    justifyContent: 'center',
    marginHorizontal: 30,
    paddingLeft: 30,
  },
  title: {
    color: '#000',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
