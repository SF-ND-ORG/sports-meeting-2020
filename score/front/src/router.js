import VueRouter from "vue-router";
import welcome from './components/welcome'
import book from './components/book'
import query from './components/query'

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
} //以上三行是为了解决相同路由报错的问题，不用深究，照原样放在此就行了

export default new VueRouter({
    routes: [
        {path: '/', component: welcome},
        {path: '/Query', component: query},
        {path: '/Book', component: book},
    ]
}) 
/*以上代码创建了两个路由，“/” 根路由和“/msg”
   大白话解释根路由就是当我们在浏览器地址栏什么参数都不带,直接输入网址比如qq.com，页面应该跳到哪，
   第二个路由/msg，就是说当我们在网址后面加一个/msg，比如qq.com/msg，页面应该跳到哪，所谓路由就是这个意思。*/