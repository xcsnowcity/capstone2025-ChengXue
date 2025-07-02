import React from 'react';
import { View, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { toast } from 'Utils/Toast';
import { TextView } from './TextView';

interface Props {
  style?: any;
  onPressNext: (password: string) => void;
}
interface State {
  password: string;
}

export default class PasswordView extends React.PureComponent<Props, State> {
  constructor(props) {
    super(props);
    this.state = {
      password: '',
    };
  }

  private dealPassword = (num: number) => {
    const { password } = this.state;
    if (password.length >= 4) {
      return;
    }
    const newPassword = `${password}${num}`;
    this.setState({
      password: newPassword,
    });
  };

  private delete = () => {
    const { password } = this.state;
    if (password.length === 0) {
      return;
    }
    const newPassword = password.substring(0, password.length - 1);
    this.setState({
      password: newPassword,
    });
  };

  changeToStar = str => {
    const strLen = str.length;
    let stars = '';
    for (let i = 0; i < strLen; i++) {
      stars += ' *';
    }
    return stars;
  };

  private next = () => {
    const { onPressNext } = this.props;
    const { password } = this.state;
    if (password.length !== 4) {
      toast('Please set your 4-digit Pin code');
      return;
    }
    onPressNext?.(password);
  };

  render() {
    const { style } = this.props;
    const { password } = this.state;
    return (
      <View style={[styles.container, style]}>
        <View style={styles.header}>
          <TextView style={{ fontSize: 28 }}>{this.changeToStar(password)}</TextView>
        </View>
        <View style={styles.itemContainer}>
          <TouchableOpacity
            style={styles.touch}
            onPress={() => {
              this.dealPassword(1);
            }}
          >
            <TextView style={{ fontSize: 30, fontWeight: 'bold' }}>1</TextView>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.touch}
            onPress={() => {
              this.dealPassword(2);
            }}
          >
            <TextView style={{ fontSize: 30, fontWeight: 'bold' }}>2</TextView>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.touch}
            onPress={() => {
              this.dealPassword(3);
            }}
          >
            <TextView style={{ fontSize: 30, fontWeight: 'bold' }}>3</TextView>
          </TouchableOpacity>
        </View>
        <View style={styles.itemContainer}>
          <TouchableOpacity
            style={styles.touch}
            onPress={() => {
              this.dealPassword(4);
            }}
          >
            <TextView style={{ fontSize: 30, fontWeight: 'bold' }}>4</TextView>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.touch}
            onPress={() => {
              this.dealPassword(5);
            }}
          >
            <TextView style={{ fontSize: 30, fontWeight: 'bold' }}>5</TextView>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.touch}
            onPress={() => {
              this.dealPassword(6);
            }}
          >
            <TextView style={{ fontSize: 30, fontWeight: 'bold' }}>6</TextView>
          </TouchableOpacity>
        </View>
        <View style={styles.itemContainer}>
          <TouchableOpacity
            style={styles.touch}
            onPress={() => {
              this.dealPassword(7);
            }}
          >
            <TextView style={{ fontSize: 30, fontWeight: 'bold' }}>7</TextView>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.touch}
            onPress={() => {
              this.dealPassword(8);
            }}
          >
            <TextView style={{ fontSize: 30, fontWeight: 'bold' }}>8</TextView>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.touch}
            onPress={() => {
              this.dealPassword(9);
            }}
          >
            <TextView style={{ fontSize: 30, fontWeight: 'bold' }}>9</TextView>
          </TouchableOpacity>
        </View>
        <View style={styles.itemContainer}>
          <TouchableOpacity style={styles.touch} onPress={this.delete}>
            <Image source={require('Image/ic_delete.png')} style={styles.delete} />
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.touch}
            onPress={() => {
              this.dealPassword(0);
            }}
          >
            <TextView style={{ fontSize: 30, fontWeight: 'bold' }}>0</TextView>
          </TouchableOpacity>
          <TouchableOpacity style={styles.touch} onPress={this.next}>
            <View style={styles.next}>
              <Image source={require('Image/ic_arrow_right.png')} />
            </View>
          </TouchableOpacity>
        </View>
      </View>
    );
  }
}
const styles = StyleSheet.create({
  container: {
    width: 210,
  },
  header: {
    backgroundColor: '#D9D9D9',
    height: 44,
    alignItems: 'center',
    flexDirection: 'row',
    paddingHorizontal: 10,
  },
  itemContainer: {
    flexDirection: 'row',
  },
  touch: {
    flex: 1,
    height: 55,
    alignItems: 'center',
    justifyContent: 'center',
  },
  delete: {
    height: 51,
    width: 51,
  },
  next: {
    height: 51,
    width: 51,
    borderRadius: 26,
    backgroundColor: '#A259FF',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
