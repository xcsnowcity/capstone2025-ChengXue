module.exports = {
  bracketSpacing: true,
  jsxBracketSameLine: false,
  singleQuote: true,
  trailingComma: 'all',
  arrowParens: 'avoid',
  endOfLine: 'lf',
  tabWidth: 2,
  importOrder: ["^react", "<THIRD_PARTY_MODULES>", "^@/(.*)$", "^[./]"],
  importOrderSeparation: false,
  importOrderSortSpecifiers: true,
  importOrderGroupNamespaceSpecifiers: true,
  importOrderCaseInsensitive: true,
  importOrderParserPlugins: ["typescript", "jsx", "classProperties", "decorators-legacy"],
  printWidth: 120,
  // parsers: ['decorators-legacy'],
  // experimentalBabelParserPluginsList: ["classProperties", "decorators-legacy"]
};
