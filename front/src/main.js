import Vue from 'vue'
import App from './App.vue'
import router from './router/index'
import elementUI from 'element-ui'
import store from "./store";
import 'element-ui/lib/theme-chalk/index.css';
import './assets/css/common.css'
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
import VueAwesomeSwiper from 'vue-awesome-swiper'
import 'swiper/dist/css/swiper.css'
import './assets/icon/iconfont.css'


Vue.use(VueAwesomeSwiper);
//设置点击遮罩不关闭dialog对话框
elementUI.Dialog.props.closeOnClickModal.default = false;
Vue.config.productionTip = false
document.onselectstart = function () { return false; }
Vue.use(elementUI)

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
