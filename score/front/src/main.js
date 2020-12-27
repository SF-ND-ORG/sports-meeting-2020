import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueRouter from 'vue-router'
Vue.use(VueRouter) //启用vue-router插件
import router from './router' //引入我们自己的路由定义表
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)

Vue.config.productionTip = false

new Vue({
  vuetify: vuetify,
  router: router, //这行也可以简写为: router,
  render: function (h) { return h(App) }
}).$mount('#app')
