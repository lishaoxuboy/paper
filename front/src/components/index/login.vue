<template>
    <div id="login" v-if="heightReset" :style="`height:${clientHeight}px; overflow:scrool`">
        <el-card v-if="loginType===1" class="box-card login-card" >
            <div style="line-height:30px; margin-bottom:20px; text-align: center;">账号密码登陆</div>
            <el-form  :model="loginInfo" label-width="100px" ref="loginInfo" :rules="loginRules">
              <el-form-item label="登陆账号:" prop="account">
                <el-input class="input" v-model="loginInfo.account" placeholder="请输入账号或者注册邮箱登录"></el-input>
              </el-form-item>
                 <el-form-item label="登录密码:" prop="password">
                <el-input type="password"   class="input" v-model="loginInfo.password" @keyup.enter.native="loginIn" placeholder="请输入密码"></el-input>
              </el-form-item>
               <el-button class="button" type="primary" round @click="loginIn">登陆</el-button>
               <el-button  type="text"  @click="toRegister()" >邮箱注册登陆</el-button>
                <el-button  type="text"  @click="loginType=3" >忘记密码</el-button>
            </el-form>
        </el-card>
        <el-card v-else-if="loginType===2" class="box-card login-card" >
            <div style="line-height:30px; margin-bottom:20px; text-align: center;">注册用户信息</div>
            <el-form  :model="registerInfo" label-width="110px" ref="registerInfo" :rules="registerRules">
                <el-form-item label="用户名称:" prop="name">
                <el-input class="input" v-model="registerInfo.name" placeholder="请输入用户名称"></el-input>
              </el-form-item>
              <el-form-item label="用户账号:" prop="account">
                <el-input class="input" v-model="registerInfo.account" placeholder="请输入用户账号"></el-input>
              </el-form-item>
                <el-form-item label="登录密码:" prop="password">
                <el-input   class="input" type="password" v-model="registerInfo.password" placeholder="请输入登录密码"></el-input>
              </el-form-item>
                <el-form-item label="确认密码:" prop="check_password">
                <el-input type="password"   class="input" v-model="registerInfo.check_password" placeholder="请输入登录密码"></el-input>
              </el-form-item>
              <el-form-item label="邮箱地址:"  prop="email_addr">
                <el-input   class="input" v-model="registerInfo.email_addr" placeholder="请输入邮箱地址"></el-input>
              </el-form-item>
                <el-form-item label="验证码:"  prop="code">
                <el-input @keyup.enter.native="register"   class="auth_code" style="width:60%" v-model="registerInfo.code" placeholder="请输入接收到验证码"></el-input>
                <el-button :disabled="disabled" style="float:right;height:35px;width: 120px;" @click="getAuthCode">{{butName}}</el-button>
              </el-form-item>

               <el-button class="button" type="primary" round @click="register">注册</el-button>
               <el-button  type="text" @click="toLogin()" >返回登陆</el-button>
            </el-form>
        </el-card>

        <el-card v-else class="box-card login-card" >
            <my-pwd :pwdType=2 :loginType.sync="loginType" />
        </el-card>


    </div>
    
</template>

<script>
    import {getClientHeight, emailVerify} from '../../utils/common'
    import {setCaCheSession, setCaCheAcc, setCaCheName, setCaCheRoleType, setCaCheEmail} from '../../utils/localStorage'
    import service from "../../utils/request";
    import {Message} from 'element-ui';
    import myPwd from '../common/person'

    export default {
        name: "login",
        components:{myPwd},
        data() {
            var validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入密码'));
                } else {
                    if (this.registerInfo.check_password !== '') {
                        this.$refs.registerInfo.validateField('checkPass');
                    }
                    callback();
                }
            };
            var validatePass2 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                } else if (value !== this.registerInfo.password) {
                    callback(new Error('两次输入密码不一致!'));
                } else {
                    callback();
                }
            };
            return {
                loginType:1, //邮箱是1,注册是2,找回密码3
                clientHeight:'',
                heightReset:true,
                loginInfoCopy:{
                    account:'',
                    password:'',
                    type:1,  //邮箱是2,用户是1

                },
                loginInfo:{},
                isLogin:true,
                registerInfoCopy:{
                    name:'',
                    account:'',
                    password:'',
                    check_password:'',
                    email_addr:'',
                    code:'',
                    type:1
                },
                registerInfo:{},
                loginRules: {
                     account: [
                         {required: true, message: '请输入用户账号', trigger: 'blur'},
                     ],
                     password: [
                         {required: true, message: '请输入用户密码', trigger: 'blur'},
                     ],
                 },
                registerRules: {
                     account: [
                         {required: true, message: '请输入用户账号', trigger: 'blur'},
                     ],
                     name: [
                         {required: true, message: '请输入用户名称', trigger: 'blur'},
                     ],
                    password: [
                        {required: true, message: '请输入密码', trigger: 'blur'},
                        {validator: validatePass, trigger: 'blur'}
                    ],
                    check_password: [
                        {required: true, message: '请输入密码', trigger: 'blur'},
                        {validator: validatePass2, trigger: 'blur' }
                     ],
                    email_addr: [
                         {required: true, message: '请输入邮箱获取验证码', trigger: 'blur'},
                     ],

                 },
                timerout:null,
                disabled:false,
                butName:'获取验证码'
            }
        },
        methods: {
            loginIn(){
                this.loginInfo.type = emailVerify(this.loginInfo.account) ? 2 : 1
                this.$refs.loginInfo.validate(async valid => {
                    if (!valid) return;
                    service.request({
                        method: "post",
                        url: "/login",
                        data: this.loginInfo
                    }).then(res => {
                        setCaCheSession(res.data.session)
                        setCaCheAcc(res.data.account)
                        setCaCheEmail(res.data.email_addr)
                        setCaCheName(res.data.name)
                        setCaCheRoleType(res.data.roleType)
                        this.$store.commit("setUserName", res.data.name);
                        this.$store.commit("setRoleType", res.data.roleType);
                        this.$store.commit("setUserNameIsChange", true)
                        if (res.data.roleType === '1') {
                            this.$router.push('/paper')
                        } else {
                            this.$router.push('/manage')
                        }
                    })
                })
            },
            getAuthCode(){
                this.$refs.registerInfo.validate(async valid => {
                    if (!valid) return;
                    if (emailVerify(this.registerInfo.email_addr)) {
                        service.request({
                            method: "post",
                            url: "/verification",
                            data: this.registerInfo
                        }).then(res => {
                            this.setInterval()
                            Message.success('发送验证码成功，请登录邮箱查收');
                        })
                    } else {
                        Message.warning('登录邮箱为空或者登录邮箱格式不正确');
                    }
                })
            },
            toRegister(){
                this.loginType = 2
                this.registerInfo = {...this.registerInfoCopy}
                this.$nextTick(() => {
                    this.$refs.registerInfo.resetFields();
                });

            },
            toLogin() {
                this.disabled = false
                this.loginType = 1
                this.loginInfo = {...this.loginInfoCopy}
                this.$nextTick(() => {
                    this.$refs.loginInfo.resetFields();
                });

            },
            register(){
                this.$refs.registerInfo.validate(async valid => {
                    if (!valid) return;
                    if(this.registerInfo.code === ''){
                        Message.warning("验证码不能为空");
                    }else if(this.registerInfo.name === '访客'){
                        Message.warning("使用非法用户名，请重新输入");
                    }else  {
                        service.request({
                            method: "post",
                            url: "/user",
                            data: this.registerInfo
                        }).then(res => {
                            Message.success('注册成功');
                            this.loginType = 1
                            clearTimeout(this.timerout)
                            this.timerout = null
                            this.disabled = false
                        })
                    }
                })
            },
            //发送验证之后，不允许重复点击验证二维码
            setInterval() {
                if (this.timerout == null) {
                    this.disabled = true
                    let count = 30
                    this.timerout = setInterval(() => {
                        this.disabled = true
                        count = count - 1
                        this.butName = count + 's后重新获取'
                        if (count === 0) {
                            clearTimeout(this.timerout)
                            this.timerout = null
                            this.butName = '获取验证码'
                            this.disabled = false
                        }
                    }, 1000)
                }
            },

        },
        mounted() {
            this.clientHeight = getClientHeight();
        }
    }
</script>

<style>
    #login{
        background:url('../../assets/img/login_back.jpg');
        width:100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .login-card{
        width:450px;
    }

    .input .el-input__inner{
        height:35px;
        width:300px
    }

    .auth_code .el-input__inner{
        height:35px;
        width:170px;
        float:left
    }


    .button{
        line-height: 10px;
        width: 400px;
    }

</style>