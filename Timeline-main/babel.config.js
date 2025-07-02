module.exports = {
  presets: ['module:metro-react-native-babel-preset'],
  plugins: [
    'react-native-reanimated/plugin',
    ['@babel/transform-runtime', { helpers: true, regenerator: false }],
    ['@babel/plugin-proposal-decorators', { legacy: true }],

    ['module-resolver', {
      root: ['./src'],
      extensions: ['.ios.js', '.android.js', '.js', '.ts', '.tsx', '.json'],
      alias: {
        tests: ['./tests/'],
        Components: './src/Components',
        Utils: './src/Utils',
        Router: './src/Router',
        Network: './src/Network',
        Image: './src/Image',
        NativeModules: './src/NativeModules',
        Page: './src/Page',
        Store: './src/Store',
        underscore: ['lodash']
      },
      transformFunctions: [
        'require',
        'require.resolve',
        'System.import'
      ]
    }],
  ],
  sourceMaps: true
}
