import axios from "axios";
import router from "../router";
import store from '../store'
import {getCaCheSession} from "./localStorage";
import {Message} from 'element-ui';

const service = axios.create({
    timeout: 15000,   // 超时
});


// 拦截器
// 添加请求拦截器
service.interceptors.request.use(function (config) {
    if(config.method === 'get' || config.method === 'delete'){
        config.params['session'] = getCaCheSession()
    }else{
        config.data['session'] = getCaCheSession()
    }
    return config;
}, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
});

// 添加响应拦截器
service.interceptors.response.use((res) => {
    // 不为0，即接口异常时
    if (res.data.code !== 0) {
        if (res.data.code === -1000) {
            store.dispatch('RESET', true)
            router.currentRoute.path !== 'login' &&
            router.replace({
                path: 'login',
                query: {redirect: router.currentRoute.path},
            })
             Message.warning('会话已过期或者用户未登录，请重新登录');
        }else{
            Message.warning(res.data.msg);
        }
        return Promise.reject(res.data);
    } else {
        return res.data
    }
},(error) => {
    // 对响应错误做点什么
    // if (error.response.status == '403') {
    //     store.dispatch('RESET', true)
    //     router.currentRoute.path !== 'login' &&
    //     router.replace({
    //         path: 'login',
    //         query: {redirect: router.currentRoute.path},
    //     })
    //     Message.warning('会话已过期或者用户未登录，请重新登录');
    // }else {
     Message.error('接口异常:' + error);

    // }
    return Promise.reject(error);
});
// 暴露service
export default service;