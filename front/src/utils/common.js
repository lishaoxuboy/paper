
//计算浏览器可视化宽高
export function getClientHeight() {
    return document.documentElement.clientHeight
}

export function getClientWidth() {
    return document.documentElement.clientWidth
}

/**
 * 通过键值获取列表中的json数据
 * 通过 key 获取列表元素 再获取 type 值
 * */

export const getValueByKey = (attrs, key, type) => {
    return objectMap(attrs, key).get(type) || false;
}
const objectMap = (objs, key) => {
    return new Map(objs.map(obj => [obj[key], obj]));
}


export function emailVerify(email){
    var regEmail = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
    if (email != '' && !regEmail.test(email)) {
       return false
    }
    return true
}