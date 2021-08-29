<template>
    <div id="home">
        <el-container>
            <el-header style="height:64px"><div class="layout" style="display:block">
                <el-row  type="flex" class="row-bg el-row" justify="space-between" id="el-row">
                    <el-col :span="2" style="display: flex;align-items: center;justify-content: center;">
                        <div class="grid-content bg-purple">
                            <span style="color:#666666; font-size: 1.2vw;">ICCACE 2021</span>
                        </div>
                    </el-col>
                    <el-col :span="19">
                        <div class="grid-content bg-purple">
                            <el-menu text-color="#909399;" :default-active="activeIndex"
                                     class="el-menu-title" mode="horizontal" router>
                                <el-menu-item v-for="(item) in Routers" :index="item.path">{{ item.title }}
                                </el-menu-item>
                            </el-menu>
                        </div>
                    </el-col>
                    <el-col :span="3" class="user-name">
                        <div class="grid-content bg-purple">
                            <el-dropdown trigger="hover" @command="handleCommand">
                                <div style="display: flex;align-items: center;justify-content: center;" >
                                    <img style="height:40px; border-radius:15px; margin-right:15px"
                                         src="../../assets/OIP.jpg"/>
                                    <span class="el-dropdown-link">
                                        {{ user ? user : '访客'  }}
                                    <i class="el-icon-caret-bottom el-icon--right"></i>
                                </span>
                                </div>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item v-if="user != ''" divided command="logout">Logout</el-dropdown-item>
                                    <el-dropdown-item v-else divided command="login">Login / Register</el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>
                        </div>
                    </el-col>

                </el-row>
            </div></el-header>

            <el-main >
                <router-view/>
            </el-main>
<!--            <el-footer><div class="layout"></div></el-footer>-->
        </el-container>
    </div>

</template>

<script>
    import {getCaCheRoleType} from '../../utils/localStorage'
    import service from "../../utils/request";
    export default {
        name: "home",
        data() {
            return {
                mainHeight: '',
                heightReset: true,
                activeIndex: 'index',
                user:'',
                roleType:'',
                swiperOptions1: {
                    pagination:{
                        el:'.swiper-pagination',
                        clickable:true,
                    },
                    slidePreView:1,
                    autoplay:{
                        autoplay:false,
                        delay:2000,
                        disableOnInteraction:false
                    },
                    spaceBetween:0,
                    loop:true,
                    navigation: {
                        nextEl: '.swiper-button-next',
                        prevEl: '.swiper-button-prev'
                    },

                },
                Routers: [
                    {path: 'index', title: 'Home'},
                    {path: 'cfp', title: ' CALL FOR PAPERS'},
                    {path: 'commoittees', title: ' COMMITTEES'},
                    {path: 'speakers', title: ' SPEAKERS'},
                    {path: 'paper', title: ' SUBMISSION'},
                    {path: 'reg', title: ' REGISTRATION'},
                    {path: 'program', title: ' PROGRAM'},
                    {path: 'venue', title: ' VENUE'},
                    {path: 'contact', title: ' CONTACT'},
                    {path: 'news', title: ' 中文'},
                ],
                isShow:true
            }
        },

        methods: {
            logout(){
                service.request({
                    method: "delete",
                    url: "/login",
                    params: {}
                }).then(res=>{
                    this.user = ''
                    this.activeIndex = 'index'
                    this.$router.push('/index')
                    this.$store.dispatch('RESET', true)
                })
            },
            // 用户名下拉菜单选择事件
            handleCommand(command) {
                if (command === 'logout') {
                    this.logout()
                } else {
                    this.$router.push({name: 'login'})
                }

            },
        },
        computed: {
          userNameIsChange:function (){
            return this.$store.getters.getUserNameIsChange;
          }
        },
        watch:{
            userNameIsChange: {
                handler(val) {
                    if (val) {
                        this.user = this.$store.getters.getUserName
                        if(getCaCheRoleType() === '2'){
                            this.Routers = [{path: 'manage', title: 'MANAGE'}]
                            this.activeIndex = 'manage'
                        }else{
                            this.Routers = [
                                {path: 'index', title: 'Home'},
                                {path: 'cfp', title: ' CALL FOR PAPERS'},
                                {path: 'commoittees', title: ' COMMITTEES'},
                                {path: 'speakers', title: ' SPEAKERS'},
                                {path: 'paper', title: ' SUBMISSION'},
                                {path: 'reg', title: ' REGISTRATION'},
                                {path: 'program', title: ' PROGRAM'},
                                {path: 'venue', title: ' VENUE'},
                                {path: 'contact', title: ' CONTACT'},
                                {path: 'news', title: ' 中文'},
                            ]
                        }
                        if(getCaCheRoleType() === '1'){this.activeIndex='paper'}
                        this.$store.commit("setUserNameIsChange", false)
                    }
                },
            },

        },
        mounted() {
            this.user = this.$store.getters.getUserName
            if (getCaCheRoleType() === '2') {
                this.Routers = [{path: 'manage', title: 'MANAGE'}]
                this.activeIndex = 'manage'
            } else {
                this.Routers = [
                    {path: 'index', title: 'Home'},
                    {path: 'cfp', title: ' CALL FOR PAPERS'},
                    {path: 'commoittees', title: ' COMMITTEES'},
                    {path: 'speakers', title: ' SPEAKERS'},
                    {path: 'paper', title: ' SUBMISSION'},
                    {path: 'reg', title: ' REGISTRATION'},
                    {path: 'program', title: ' PROGRAM'},
                    {path: 'venue', title: ' VENUE'},
                    {path: 'contact', title: ' CONTACT'},
                    {path: 'news', title: ' 中文'},
                ]
            }
            if(this.$route.path === '/paper'){
                this.activeIndex = 'paper'
            }
        }
    }
</script>

<style scoped>
    .user-name{
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .el-menu.el-menu--horizontal{
        border-bottom:none
    }
    .el-header, .el-footer {
        background-color: #ffffff;
        position: fixed;
        top: 0;
        height: 64px;
        width: 100%;
        z-index:1000;
        border-bottom: solid 4px #007944;
    }
    .title{
        font-weight: 600;
        font-size: 1em;
        color: #f9f8f6;
        background: rgb(28, 35, 39);
        border: none;
        cursor: pointer;
        margin-right:20px
    }

    .user{
        font-weight: 600;
        font-size: 12px;
        border: none;
        line-height:35px;
        cursor: pointer;
        transition: all 0.6s;
    }

    .name{
        color:black;
        font-weight: 600;
        font-size: 18px;
        border: none;
        line-height:35px;
        cursor: pointer;
        transition: all 0.6s;
        margin-right:20px
    }
    .el-aside {
        background-color: #D3DCE6;
        color: #333;
        text-align: center;
        line-height: 200px;
    }

    .el-main {
        color: #333;
    }

    body > .el-container {
        margin-bottom: 40px;
    }

    .el-container:nth-child(5) .el-aside,
    .el-container:nth-child(6) .el-aside {
        line-height: 260px;
    }

    .el-container:nth-child(7) .el-aside {
        line-height: 320px;
    }

    .slide_img{
        width:100%;
        cursor: pointer;
        transition: all 0.4s;
    }

    .slide_img:hover{
        transform: scale(1.05);
    }

    .banner{
        margin-top:60px;
        overflow:hidden
    }

    /*.el-row {*/
    /*    box-shadow: 0px 0px 5px 0px rgba(0,0,0,0.95);*/
	/*    -webkit-box-shadow: 0px 0px 5px 0px rgba(0,0,0,0.95);*/
	/*    -moz-box-shadow: 0px 0px 5px 0px rgba(0,0,0,0.95);*/
    /*}*/
    /*.el-menu{*/
    /*    background-color:rgb(28,35,39)*/
    /*}*/

    .el-menu--horizontal>.el-menu-item.is-active{
            /*color: #409EFF !important;*/
        border-bottom:none;
        background-color: #eeeeee;
    }

    .el-menu--horizontal>.el-menu-item{
        border-bottom:none;
    }

    #home .el-menu-item{
        font-size:13px
    }

    .el-menu-title .el-menu-item:focus{
        background-color:#eeeeee !important;
    }

    .el-menu-title .el-menu-item:onblur{
        background-color:#ffffff !important;
        border-bottom-color:#ffffff
    }
</style>