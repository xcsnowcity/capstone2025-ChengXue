import { Alert, PermissionsAndroid, Platform } from 'react-native';
import { toast } from 'Utils/Toast';
//** Location Permission Checker(Haven;t used) */

class PermissionHelper {
  checkLocationPermission = async (grantedCallback: () => void) => {
    try {
      const hasPermission = await PermissionsAndroid.check(PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION);
      if (hasPermission) {
        grantedCallback();
      } else {
        this.requestLocationPermission(grantedCallback);
      }
    } catch (err) {
      toast('no permission');
    }
  };

  requestLocationPermission = async (grantedCallback: () => void) => {
    try {
      const granted = await PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION);
      if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        grantedCallback();
      } else {
        toast('no permission');
      }
    } catch (err) {
      toast('no permission');
    }
  };
}

export const permissionHelper = new PermissionHelper();
