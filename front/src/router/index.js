import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/layout/home'
import Main from '../components/index/main'
import Index from '../components/index/show'
import Paper from '../components/index/paper/paper'
import Login from '../components/index/login'
import Cfp from '../components/index/show/cfp'
import Contact from '../components/index/show/contact'
import News from '../components/index/show/news'
import Reg from '../components/index/show/reg'
import Speakers from '../components/index/show/speakers'
import Venue from '../components/index/show/venue'
import Commoittees from '../components/index/show/committees'
import Program from '../components/index/show/program'
import Manage from '../components/index/manage/manage'


Vue.use(VueRouter);
const originalPush = VueRouter.prototype.push;

VueRouter.prototype.push = function push(location, onResolve, onReject) {
  if (onResolve || onReject)
    return originalPush.call(this, location, onResolve, onReject);
  return originalPush.call(this, location).catch((err) => err);
};

const  Router= new VueRouter({
    routes:[
        { path: '/', name: 'home', component: Home, redirect:'/index', children: [
                {path:'/paper',name: 'paper', component: Paper},
                {path: '/login', name: 'login', component: Login},
                {path: '/manage', name: 'manage', component: Manage},
                {
                    path: '/main', name: 'main', component: Main, redirect:'/index',children: [
                        {path: '/index', name: 'index', component: Index},
                        {path: '/cfp', name: 'cfp', component: Cfp},
                        {path: '/contact', name: 'contact', component: Contact},
                        {path: '/commoittees', name: 'commoittees', component: Commoittees},
                        {path: '/venue', name: 'venue', component: Venue},
                        {path: '/speakers', name: 'speakers', component: Speakers},
                        {path: '/reg', name: 'reg', component: Reg},
                        {path: '/news', name: 'news', component: News},
                        {path: '/program', name: 'program', component: Program},
                    ]
                },


            ]
        }
    ]
});

export default Router
