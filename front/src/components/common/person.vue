<template>
    <div id="person"  style="width: 410px;">
        <div style="line-height:30px; margin-bottom:20px;text-align: center; ">{{pwdType === 1 ? '修改登录密码' : '找回登录密码'}}</div>
        <el-form :model="userInfo" label-width="90px" ref="userInfo" :rules="userRules">
            <el-form-item label="邮箱地址:" prop="email_addr">
                <el-input class="input" v-model="userInfo.email_addr" :disabled="emailDisabled" placeholder="请输入邮箱地址"></el-input>
            </el-form-item>
            <el-form-item label="验证码:" prop="code" >
                <el-input @keyup.enter.native="register" class="auth_code" style="width:50%" v-model="userInfo.code"
                          placeholder="请输入接收到验证码" ></el-input>
                <el-button :disabled="disabled" style="float:right;height:35px;width: 120px;margin-right: 20px;" @click="getAuthCode">
                    {{ butName }}
                </el-button>
            </el-form-item>
            <el-form-item label="老密码:" prop="old_pwd" :style="`display: ${pwdType===1 ? 'block-inline' : 'none'}`"  v-if="pwdType===1">
                <el-input type="password" class="input" v-model="userInfo.old_pwd" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item label="新密码:" prop="new_pwd">
                <el-input  type="password" class="input" v-model="userInfo.new_pwd" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item label="确认密码:" prop="verify_pwd">
                <el-input  type="password" @keyup.enter.native="modify" class="input" v-model="userInfo.verify_pwd" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-button class="button" type="primary" round @click="modify">确认</el-button>
            <el-button v-if="pwdType===2"  type="text" @click="$emit('update:loginType', 1)" >返回登陆</el-button>

        </el-form>
    </div>

</template>

<script>
    import service from "../../utils/request";
    import {Message} from 'element-ui';
    import {emailVerify} from "../../utils/common";
    import {getCaCheEmail} from "../../utils/localStorage";


    export default {
        name: "person",
        props:{
          pwdType:Number
        },
        data(){
            let validatePass2 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                } else if (value !== this.userInfo.new_pwd) {
                    callback(new Error('两次输入密码不一致!'));
                } else {
                    callback();
                }
            };
            let validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入密码'));
                } else {
                    if (this.userInfo.verify_pwd !== '') {
                        this.$refs.userInfo.validateField('verify_pwd');
                    }
                    callback();
                }
            };
            return{
                userRules: {
                    email_addr: [
                        {required: true, message: '请输入邮箱', trigger: 'blur'},
                    ],
                    code: [
                        {required: true, message: '请输入邮箱验证码', trigger: 'blur'},
                    ],
                    old_pwd: [
                        {required: true, message: '请输入密码', trigger: 'blur'},
                    ],
                    new_pwd: [
                        {validator: validatePass, trigger: 'blur'},
                        {required: true, message: '请输入密码', trigger: 'blur'},
                    ],
                    verify_pwd: [
                        {validator: validatePass2, trigger: 'blur'},
                        {required: true, message: '重复新密码不能为空', trigger: 'blur'},
                    ],
                 },
                userInfo:{
                    old_pwd:'',
                    new_pwd:'',
                    type:1,
                    code:'',
                    email_addr:''
                },
                checkEmailInfo:{
                    name:'',
                    account:'',
                    email_addr:'',
                    type:2
                },
                timerout:null,
                disabled:false,
                butName:'获取验证码',
                emailDisabled:false
            }
        },
        watch:{
            pwdType:{
                handler(val){
                    if (val === 1) {
                        this.userInfo.email_addr = getCaCheEmail()
                        this.emailDisabled = true
                    }else{
                         this.emailDisabled = false
                    }
                },
                immediate:true
            }

        },
        methods:{
            modify() {
                this.userInfo.type = this.pwdType
                this.$refs.userInfo.validate(async valid => {
                    if (!valid) return;
                    if (emailVerify(this.userInfo.email_addr)) {
                        service.request({
                            method: "put",
                            url: "/user",
                            data: this.userInfo
                        }).then(res => {
                            Message.success('修改成功');
                            this.userInfo = {
                                old_pwd: '',
                                new_pwd: '',
                                verify_pwd: '',
                                type: 1,
                                code: '',
                                email_addr: getCaCheEmail()
                            }
                        })
                    }else{
                         Message.warning('登录邮箱为空或者登录邮箱格式不正确');
                    }
                })
            },

            getAuthCode() {
                this.checkEmailInfo.type = 2
                this.checkEmailInfo.email_addr = this.userInfo.email_addr
                if (emailVerify(this.userInfo.email_addr)) {
                    service.request({
                        method: "post",
                        url: "/verification",
                        data: this.checkEmailInfo
                    }).then(res => {
                        this.setInterval()
                        Message.success('发送验证码成功，请登录邮箱查收');
                    })
                } else {
                    Message.warning('登录邮箱为空或者登录邮箱格式不正确');
                }
            },

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
        }
    }
</script>

<style >
#person .el-form-item__content{
    line-height: 1px !important;
}

</style>