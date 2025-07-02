import { HomeScreen } from 'Page/Home/HomeScreen';
import { LegalScreen } from 'Page/Home/LegalScreen';
import { MentalScreen } from 'Page/Home/MentalScreen';
import { InputPasswordScreen } from 'Page/Password/InputPasswordScreen';
import { SetPasswordScreen } from 'Page/Password/SetPasswordScreen';
import { AnswerScreen } from 'Page/Question/AnswerScreen';
import { BasicInformationScreen } from 'Page/Question/BasicInformationScreen';
import { QuestionScreen } from 'Page/Question/QuestionScreen';
import { ResultScreen } from 'Page/Question/ResultScreen';
import { WeatherScreen } from 'Page/Weather/WeatherScreen';
import { WhatDvScreen } from 'Page/Welcome/WhatDvScreen';
import { WelcomeScreen } from 'Page/Welcome/WelcomeScreen';
import { HousingScreen } from 'Page/Home/HousingScreen';
import { DomesticAbuseSupportScreen } from 'Page/Home/DomesticAbuseSupportScreen';
import { FamilyServiceScreen } from 'Page/Home/FamilyServiceScreen';
import { FinancialScreen } from 'Page/Home/FinancialScreen';
import { EducationEmploymentScreen } from 'Page/Home/EducationEmploymentScreen';
import { HowtoSupportScreen } from 'Page/Home/HowtoSupportScreen';
import { ParentingScreen } from 'Page/Home/ParentingScreen';

export const WelcomeTable = {
  Welcome: {
    screen: WelcomeScreen,
    options: {
      headerShown: false,
      title: 'Welcome',
    },
  },
  WhatDv: {
    screen: WhatDvScreen,
    options: {
      headerShown: false,
      title: 'What is Domestic Violence?',
    },
  },
  SetPassword: {
    screen: SetPasswordScreen,
    options: {
      headerShown: false,
      title: 'SetPassword'
    },
  },
  Weather: {
    screen: WeatherScreen,
    options: {
      headerShown: false,
      title: 'Weather',
    },
  },
  InputPassword: {
    screen: InputPasswordScreen,
    options: {
      headerShown: false,
      title: 'InputPassword',
    },
  },
  Question: {
    screen: QuestionScreen,
    options: {
      headerShown: false,
      title: 'What’s Domestic Violence?',
    },
  },
  Answer: {
    screen: AnswerScreen,
    options: {
      headerShown: false,
      title: 'Answer',
    },
  },
  Result: {
    screen: ResultScreen,
    options: {
      headerShown: false,
      title: 'Result',
    },
  },
  BasicInformation: {
    screen: BasicInformationScreen,
    options: {
      headerShown: false,
      title: 'BasicInformation ',
    },
  },
};

const RouterTable: any = {
  Weather: {
    screen: WeatherScreen,
    options: { headerShown: false },
  },
  BasicInformation: {
    screen: BasicInformationScreen,
    options: { headerShown: false },
  },
  InputPassword: {
    screen: InputPasswordScreen,
    options: { headerShown: false },
  },
  Answer: {
    screen: AnswerScreen,
    options: { headerShown: false },
  },
  Result: {
    screen: ResultScreen,
    options: { headerShown: false },
  },
  Home: {
    screen: HomeScreen,
    options: {
      headerShown: false,
      title: 'Home page',
    },
  },
  Legal: {
    screen: LegalScreen,
    options: {
      headerShown: false,
      title: 'Legal Services',
    },
  },
  Mental: {
    screen: MentalScreen,
    options: {
      headerShown: false,
      title: 'Mental Well-being Support',
    },
  },
  Housing: {
    screen: HousingScreen,
    options: {
      headerShown: false,
      title: 'Housing',
    },
  },
  DomesticAbuse: {
    screen: DomesticAbuseSupportScreen,
    options: {
      headerShown: false,
      title: 'DomesticAbuse',
    },
  },
  FamilyService: {
    screen: FamilyServiceScreen,
    options: {
      headerShown: false,
      title: 'Family Service',
    },
  },
  Financial: {
    screen: FinancialScreen,
    options: {
      headerShown: false,
      title: 'Financial',
    },
  },
  EducationEmployment: {
    screen: EducationEmploymentScreen,
    options: {
      headerShown: false,
      title: 'Education Employment',
    },
  },
  HowtoSupport: {
    screen: HowtoSupportScreen,
    options: {
      headerShown: false,
      title: 'How to Support',
    },
  },
  Parenting: {
    screen: ParentingScreen,
    options: {
      headerShown: false,
      title: 'Parenting',
    },
  },
};

export default RouterTable;
