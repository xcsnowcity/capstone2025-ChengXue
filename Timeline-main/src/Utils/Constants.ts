import { StatusBar } from 'react-native';

const StatusbarHeight = () => {
  return StatusBar.currentHeight;
};

const NavBarHeight = () => {
  return StatusBar.currentHeight ?? 0 + 49;
};

const BottomSafeAreaInset = () => {
  return 0;
};

const TabBarHeight = () => {
  return 49;
};

export const NAV_BAR_HEIGHT = NavBarHeight();
export const STATUS_BAR_HEIGHT = StatusbarHeight();
export const BOTTOM_SAFE_AREA_INSET = BottomSafeAreaInset();
export const TAB_BAR_HEIGHT = TabBarHeight();

export const AsyncKey = {
  password: 'password',
};
