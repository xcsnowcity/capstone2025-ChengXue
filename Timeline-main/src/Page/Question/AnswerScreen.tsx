import React, { useState } from 'react';
import { Alert, Image, StyleSheet, TouchableOpacity, View } from 'react-native';
import BgView from 'Components/BgView';
import TButton from 'Components/TButton';
import { TextView } from 'Components/TextView';
import TitleBar from 'Components/TitleBar';
import { RouterReplace } from 'Router/RouterAction';
import { AnswerList } from './AnswerConfig';

export function AnswerScreen() {
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [userAnswers, setUserAnswers] = useState<{ [key: string]: string }>({});

  return (
    <BgView style={styles.container}>
      {currentIndex !== 0 ? (
        <TouchableOpacity
          style={{ position: 'absolute', top: 10, left: 15 }}
          onPress={() => {
            setCurrentIndex(currentIndex - 1);
          }}
        >
          <Image source={require('Image/ic_back.png')} />
        </TouchableOpacity>
      ) : null}

      <TitleBar title={AnswerList[currentIndex].title} />
      <TextView style={styles.title}>{AnswerList[currentIndex].desc}</TextView>

      <View style={{ marginTop: 40 }}>
        {AnswerList[currentIndex].buttons.map(item => {
          return (
            <TButton
              key={`${item.title}`}
              title={item.title}
              onPress={() => {
                // Record the user's answer
                setUserAnswers({
                  ...userAnswers,
                  [AnswerList[currentIndex].key]: item.title,
                });
                if (item.title === 'Yes' && [6, 8, 9].includes(currentIndex)) {
                  // Show the emergency alert
                  Alert.alert(
                    'Emergency',
                    'In case of emergency, please dial 112 or 999.',
                    [
                      {
                        text: 'OK',
                        onPress: () => {
                          // Handle OK press if needed
                        },
                      },
                    ]
                  );
                }
                switch (item.title) {
                  case 'Yes':
                  case 'No':
                    if (currentIndex === AnswerList.length - 1) {
                      RouterReplace('Result', userAnswers);
                    } else {
                      setCurrentIndex(currentIndex + 1);
                    }
                    break;
                  case 'Skip':
                    RouterReplace('BasicInformation', null);
                    break;
                  default:
                    break;
                }
              }}
              style={styles.button}
            />
          );
        })}
      </View>
      {/**add a Progress Bar on the bottom*/}
      <View style={styles.progressBar}>
        {AnswerList.map((item, index) => {
          return (
            <View
              key={`progress-${index}`}
              style={{
                width: 10,
                height: 10,
                borderRadius: 5,
                backgroundColor: index <= currentIndex ? '#50C2C9' : '#CCCCCC',
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
    marginBottom: 15,
  },
  buttonTitle: {
    fontSize: 16,
  },
  title: {
    marginHorizontal: 30,
    marginTop: 40,
  },
  iconContainer: {
    alignItems: 'center',
    marginTop: 40,
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