<template>
    <div id="uppaper" style="margin:20px">
        <div>
            <span>{{title}}论文信息：</span>
            <hr align="left" class="title_hr" >
        </div>
        <el-form :model="paperInfo" :inline="true"  label-position="left" label-width="100px" ref="paperInfo" :rules="paperRules">
            <el-form-item class="info"  style="margin-bottom:0" label="会议名称:"  >
                <span>2021年传感器和仪器仪表国际学术会议(ICSI2012)</span>
                <hr class="hr">
            </el-form-item>
<!--            <el-form-item class="info" label="距离报名截至还有:">-->
<!--                <span style="color:#e6a23c">28天时分秒</span>-->
<!--                -->
<!--            </el-form-item>-->
            <el-form-item class="info" label="论文标题:" prop="name">
                <el-input class="h-input"  v-model="paperInfo.name" placeholder="请输入论文标题"></el-input>
            </el-form-item>
            <el-form-item class="info" label="关键字:" prop="key_word" >
                <el-input class="h-input"  v-model="paperInfo.key_word" placeholder="请输入关键字"></el-input>
            </el-form-item>
            <el-form-item class="info" label="摘要:" prop="abstract" >
                <el-input class="h-input" v-model="paperInfo.abstract" placeholder="请输入摘要"></el-input>
            </el-form-item>
            <el-form-item class="info" label="上传附件:" prop="path" style="margin-bottom:0">
                <el-row :gutter="24" style="height: 230px;">
                    <el-col style="text-align: center;" :span="10"><div class="grid-content bg-purple">
                        <my-upload :options="pdfOptions" :name.sync="paperInfo.pdf_name" :value.sync="paperInfo.pdf_path"></my-upload>
                    </div></el-col>
                    <el-col style="text-align: center;" :span="10"><div class="grid-content bg-purple">
                        <my-upload :options="wordOptions" :name.sync="paperInfo.word_name" :value.sync="paperInfo.word_path"></my-upload>
                    </div></el-col>
                </el-row>
            </el-form-item>

            <hr class="hr" style="height:7px">

            <div style="padding:20px 20px 0 0">
                <span>作者信息：</span>
                <span style="font-size:12px; color:#e6a23c">&nbsp * 请按论文中的作者顺序完善所有的信息，以确保录入通知无误</span>
                <hr align="left" class="title_hr">
            </div>
            <el-row v-for="(item, index) in paperInfo.author_list " v-if="authFlag">
                <el-col :span="1">
                    <div class="grid-content bg-purple" @click="delAuth(index)"><i
                            style="color:red; cursor:pointer;" class="el-icon-remove-outline"/></div>
                </el-col>
                <el-col :span="23">
                    <div class="grid-content bg-purple-light">
                        <el-form-item label="作者姓名:" :prop="'author_list.' + index + '.author_name'" :rules="paperRules.author_name">
                            <el-input class="h-input w-input" style="width:380px"
                                      v-model="item.author_name" placeholder="请输入姓名"></el-input>
                        </el-form-item>
                        <el-form-item label="联系地址：" :prop="'author_list.' + index + '.addr'" :rules="paperRules.addr">
                            <el-input v-model="item.addr" class="h-input" style="width:380px;"
                                      placeholder="请输入联系地址"></el-input>
                        </el-form-item>
                        <el-form-item label="学校/单位:" :prop="'author_list.' + index + '.org'" :rules="paperRules.org">
                            <el-input v-model="item.org" class="h-input" style="width:380px;"
                                      placeholder="请输入学校/单位名称"></el-input>
                        </el-form-item>
                        <el-form-item label="手机号：" :prop="'author_list.' + index + '.phone'" :rules="paperRules.phone">
                            <el-input v-model="item.phone" class="h-input" style="width:380px;"
                                      placeholder="请输入手机号"></el-input>
                        </el-form-item>
                        <el-form-item label="工作邮箱:"  :prop="'author_list.' + index + '.email'" :rules="paperRules.email">
                            <el-input v-model="item.email" class="h-input" style="width:380px;"
                                      placeholder="请输入工作邮箱"></el-input>
                        </el-form-item>
                        <el-form-item label="微信：" :prop="'author_list.' + index + '.wechat'" :rules="paperRules.wechat">
                            <el-input v-model="item.wechat" class="h-input" style="width:380px;"
                                      placeholder="请输入微信号"></el-input>
                        </el-form-item>
                        <el-form-item label="职称:"  :prop="'author_list.' + index + '.job_title'" :rules="paperRules.job_title">
                            <el-select v-model="item.job_title" clearable placeholder="请输入职称" >
                                <el-option
                                    v-for="item in jobs"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <hr class="hr">
                    </div>
                </el-col>
            </el-row>

            <div><i  @click="addAuth()" class="el-icon-circle-plus-outline" style="color:#409EFF;margin:20px; cursor:pointer;">
                <span style="font-size:13px; ">&nbsp增加作者</span></i></div>
            <hr class="hr" style="height:7px">
            <div style="padding:20px 20px 20px 0">
                <span>请选择您的订单联系作者：</span>
            </div>
            <el-form-item prop="manage_author_name" >
                <el-select  v-model="paperInfo.manage_author_name" placeholder="请选择" @change="manageSelect"
                            style="width:325px" v-if="selectFlag">
                    <el-option
                            v-for="item in paperInfo.author_list"
                            :key="item.author_name"
                            :label="item.author_name"
                            :value="item.author_name"
                    >
                    </el-option>
                </el-select>
            </el-form-item>
        </el-form>
        <el-button @click='commitPaper()' class="commit" type="primary">提交</el-button>

    </div>
    
</template>

<script>
    import _ from 'lodash'
    import myUpload from '../../common/myUpload'
    import {Message} from 'element-ui';
    import {getValueByKey} from '../../../utils/common'
    import service from "../../../utils/request";
    import {setCaCheAcc, setCaCheRuleType, setCaCheSession} from "../../../utils/localStorage";
    export default {
        name: "up_paper",
        components:{myUpload},
        props:{
            paperData:Object,
            title:String
        },
        data(){
            return{
                authFlag:true,
                paperInfo:{},
                jobs: [
                    {value: '教授',label: '教授'},
                    {value: '副教授',label: '副教授'},
                    {value: '研究员',label: '研究员'},
                    {value: '副研究员',label: '副研究员'},
                    {value: '助理研究员',label: '助理研究员'},
                    {value: '工程师',label: '工程师'},
                    {value: '讲师',label: '讲师'},
                    {value: '国内学生',label: '国内学生'},
                    {value: '留学生',label: '留学生'},
                    {value: '其他职称',label: '其他职称'}
                ],
                auths:{
                    index:'',
                    author_name: '',
                    english_name: 'english_name',
                    org: '',
                    email:'',
                    adddr:'',
                    job_title:'',
                    phone:'',
                    wechat:'',
                    manage:''
                },
                pdfOptions: {
                    urlPath: '/upload',
                    title: 'PDF',
                    accept: '.pdf,.pptx'
                },
                wordOptions: {
                    urlPath: '/upload',
                    title: 'WORD',
                    accept: 'doc,.docx'
                },
                sizeLimit: 5,
                value:'',
                index:0,
                paperRules: {
                    name: [
                        {required: true, message: '请输入论文标题', trigger: 'blur'},
                    ],
                    key_word: [
                        {required: true, message: '请输入关键字', trigger: 'blur'},
                    ],
                    abstract: [
                        {required: true, message: '请输入摘要', trigger: 'blur'},
                    ],
                    author_name: [
                        {required: true, message: '请输入姓名', trigger: 'blur'},
                    ],
                    english_name: [
                        {required: true, message: '请输入英文名', trigger: 'blur'},
                    ],
                    addr: [
                        {required: true, message: '请输入联系地址', trigger: 'blur'},
                    ],
                    org: [
                        {required: true, message: '请输入联系地址', trigger: 'blur'},
                    ],
                    phone: [
                        {required: true, message: '请输入联系地址', trigger: 'blur'},
                    ],
                    email: [
                        {required: true, message: '请输入工作邮箱', trigger: 'blur'},
                    ],
                    wechat: [
                        {required: true, message: '请输入微信号', trigger: 'blur'},
                    ],
                    job_title: [
                        {required: true, message: '请输入职称', trigger: 'blur'},
                    ],
                    manage_author_name:[
                        {required: true, message: '请选择你的订单联系作者', trigger: ['blur','change']},
                    ]
                },
                paperInfoCopy: {
                    manager:'',
                    name: '',
                    key_word: '',
                    abstract: '',
                    pdf_path: '',
                    word_path: '',
                    status: '',
                    comments: '',
                    money: '',
                    author_list: [{
                        index: 0,
                        author_name: '',
                        english_name: '',
                        org: '',
                        email: '',
                        addr: '',
                        job_title: '',
                        phone: '',
                        wechat: '',
                        manage: '',
                    }],
                },
                curAuth:{},
                selectFlag:true
            }
        },
        watch:{
            paperData:{
                handler(val) {
                    this.curAuth = _.cloneDeep(this.auths)
                    if (JSON.stringify(val) === "{}") {
                        this.paperInfo = _.cloneDeep(this.paperInfoCopy)
                        this.$refs.paperInfo.resetFields('manage_author_name');
                    } else {
                        this.paperInfo = _.cloneDeep(val)
                        this.curAuth =  getValueByKey(this.paperInfo.author_list, 'author_name', this.paperInfo.manage_author_name)
                    }
                }, immediate: true,
            },
            "curAuth.author_name":{
                handler(val){
                    this.paperInfo.manage_author_name = val
                },
                deep:true
            }

        },
        methods:{
            addAuth(){
                this.index += 1
                this.auths.index = this.index
                this.paperInfo.author_list.push(_.cloneDeep(this.auths))
            },
            delAuth(index){
                if(this.paperInfo.author_list.length===1){
                    Message.warning('请至少保留一位作者信息')
                }else{
                    this.authFlag = false
                    this.$nextTick(()=>{
                        if(this.curAuth.author_name === this.paperInfo.author_list[index].author_name){
                            Message.warning('当前作者已经被选择为“联系人”，请解绑后在删除')
                            // this.curAuth = {}
                            // this.paperInfo.manage_author_name = ''
                            // this.$refs.paperInfo.resetFields('manage_author_name');
                        }else {
                            this.paperInfo.author_list.splice(index, 1)
                        }
                        this.authFlag = true
                    })
                }
            },
            manageSelect(val){
                this.selectFlag = false
                this.$nextTick(() => {
                    this.paperInfo.manage_author_name = val
                    this.curAuth = getValueByKey(this.paperInfo.author_list, 'author_name', val)
                    this.selectFlag = true
                })
            },
            commitPaper() {
                let method = this.title === '新增' ? 'post' : 'put'
                this.$refs.paperInfo.validate(async valid => {
                    if (!valid) return;
                    if (!this.paperInfo.pdf_path || !this.paperInfo.word_path) { Message.warning('缺少PDF或者WORD文件');return}
                    if (!this.verifyAuthor()) { Message.warning('作者名称不能重复');return}
                    getValueByKey(this.paperInfo.author_list, 'author_name', this.paperInfo.manage_author_name).manage = '1'
                    service.request({
                        method: method,
                        url: "/paper",
                        data: this.paperInfo
                    }).then( async res => {
                        this.paperInfo = _.cloneDeep(this.paperInfoCopy)
                        this.$nextTick(() => {
                            this.$refs.paperInfo.resetFields();
                        });
                        let tip = this.title === '新增' ? '新增成功' : '修改成功'
                        Message.success(tip)
                        // if(this.title === '新增') {
                        //     const confirmResult = await this.$confirm(
                        //         '是否跳转到《我的论文》界面?',
                        //         '提示',
                        //         {
                        //             confirmButtonText: '确定',
                        //             cancelButtonText: '取消',
                        //             type: 'warning'
                        //         }
                        //     ).catch(err => err);
                        //     if (confirmResult !== 'confirm') return;
                        // }
                        this.$emit('update:title', '新增')
                        this.$emit('update:rCardType', 1)
                        this.$emit('back', true)
                    })
                })
            },
            verifyAuthor(){
                let authorNames = []
                for(var item in this.paperInfo.author_list){
                    if(authorNames.includes(this.paperInfo.author_list[item].author_name)){
                        return false
                    }else{
                        authorNames.push(this.paperInfo.author_list[item].author_name)
                    }
                }
                return true
            },
        },
        // mounted() {
        //     this.$refs.paperInfo.resetFields();
        // }
    }
</script>

<style>
    .h-input .el-input__inner{
        height:35px;
        line-height: 35px;
    }

    .el-select .el-input__inner{
        height:35px;
        line-height: 35px;
    }

    .hr{
        background: #efefef;
        height: 1px;
        border: none;
    }
    .title_hr{
        background: #409EFF;
        height: 2px;
        width:150px;
        border: none;
        margin:10px 0 10px 0

    }

    .auto-form .el-form-item{
        margin-right:40px !important
    }

    .commit {
        width: 200px;
        height: 50px;
        font-size: 25px;
    }

    .info{
        width:980px
    }

    .info .el-input__inner{
        width:850px
    }

    .info .el-form-item__content{
        width:850px;
    }
    .info .el-form-item__label{
        width:130px !important
    }
</style>