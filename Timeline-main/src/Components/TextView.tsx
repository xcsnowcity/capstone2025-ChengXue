import React, { PureComponent } from 'react';
import { Text, TextProps, TextStyle, StyleSheet } from 'react-native';

interface Props extends TextProps { }

/**
 * fontSize---set: lineHeight
 */
export class TextView extends PureComponent<Props> {
  render() {
    const { style } = this.props;
    const singleObjectStyle = Array.isArray(style) ? StyleSheet.flatten(style) : style;

    const { fontSize } = (singleObjectStyle || {}) as TextStyle;
    const defaultFontSize = 18;
    const size = fontSize || defaultFontSize;
    const lineHeight = Math.round(size * 1.3);

    // eslint-disable-next-line react/jsx-props-no-spreading
    return <Text {...this.props} style={[{ lineHeight, fontSize: 18, color: '#000' }, style]} />;
  }
}
