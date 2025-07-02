// eslint-disable-next-line import/no-extraneous-dependencies
const _ = require('lodash')

/**
 * Checks if `value` is an empty object, collection, map, or set.
 *
 * Objects are considered empty if they have no own enumerable string keyed
 * properties.
 *
 * Array-like values such as `arguments` objects, arrays, buffers, strings, or
 * jQuery-like collections are considered empty if they have a `length` of `0`.
 * Similarly, maps and sets are considered empty if they have a `size` of `0`.
 *
 * @static
 * @memberOf _
 * @since 0.1.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is empty, else `false`.
 * @example
 *
 * _.isEmpty(null);
 * // => true
 *
 * _.isEmpty(true);
 * // => true
 *
 * _.isEmpty(1);
 * // => false
 *
 * _.isEmpty([1, 2, 3]);
 * // => false
 *
 * _.isEmpty({ 'a': 1 });
 * // => false
 */
export function isEmptyValue(value) {
  if (typeof value === 'number') {
    return false
  }
  return _.isEmpty(value)
}

/**
 * 判断资源文件路径是不是本地路径
 * 判断标准：安卓 以"file:///"做前缀，iOS以"/var"做前缀
 * @param {value} 资源路径
 */
export function isLocalFile(value) {
  if (!value) {
    return false
  }
  if (typeof value !== 'string') {
    return false
  }
  const prefixIndexAndroid = value.indexOf('file:///')
  const prefixIndexIos = value.indexOf('/var')
  if (prefixIndexAndroid === 0 || prefixIndexIos === 0) {
    return true
  }
  return false
}

/**
 * js判断字符串是否为JSON格式
 *@param str
 * */
export function isJSONString(str) {
  if (typeof str === 'string') {
    try {
      const obj = JSON.parse(str)
      if (typeof obj === 'object' && obj) {
        return true
      }
      return false

    } catch (e) {
      return false
    }
  }
  return false
}

/**
 * 查找指定 url地址中的指定参数
 * @param url
 * @param paraName
 * @returns {string}
 */
export function getUrlParam(url, paraName) {
  const arrObj = url.split('?')
  if (arrObj.length > 1) {
    const arrPara = arrObj[1].split('&')
    let arr

    for (let i = 0; i < arrPara.length; i++) {
      arr = arrPara[i].split('=')
      if (arr != null && arr[0] === paraName) {
        return arr[1]
      }
    }
    return ''
  }
  return ''

}

// 字符串首字母大写
export function firstUpperCase(str) {
  return str.toLowerCase().replace(/^\S/g, (s) => s.toUpperCase())
}

/**
 * 浮点数处理
 * @param {Number} number 原始输入数
 *
 * @returns {Number} 四舍五入之后的数字
 * @description
 * 由于特殊数字（比如：0.285）在 round 时会丢失精度（变成 0.28），
 * 0.92 * 10 = 9.200000000000001
 * 所以与 web 端统一使用 0.000001 矫正精度
 */
export function roundNumber(number) {
  return Math.round(100 * number + 0.000001) / 100
}
