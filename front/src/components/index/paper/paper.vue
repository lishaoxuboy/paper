<template>
    <div id="paper">
        <multipane style="width: 100%">
            <div class="left-area" :style="`height:${clientHeight}px`" v-if="heightReset">
                <el-card style="width:98%; margin-top:20px; overflow-y: auto; ">
                    <el-button @click="rCardType = 2; active='0'; paperData={}; title='新增'" icon="el-icon-edit-outline"
                               style="width:100%; margin-bottom:20px" type="danger" round>创作中心
                    </el-button>
                    <el-menu
                            :default-active="active"
                            class="el-menu-vertical-demo">
                        <el-menu-item index="1" @click="rCardType = 1">
                            <i class="el-icon-document"></i>
                            <span slot="title">我的论文</span>
                        </el-menu-item>
                        <el-menu-item index="2" @click="rCardType = 3">
                            <i class="el-icon-setting"></i>
                            <span slot="title">密码修改</span>
                        </el-menu-item>
                    </el-menu>
                </el-card>
            </div>
            <multipane-resizer/>
            <div class="right-area" :style="`height:${clientHeight}px`" v-if="heightReset">
                <el-card style="width:98%; margin-top:20px; overflow-y: auto; ">
                    <!--表格内容-->
                    <div v-if="rCardType === 1">
<!--                        <el-button @click="doQuery" icon="el-icon-refresh" style="margin-bottom: 10px; padding: 10px;">刷新</el-button>-->
                        <my-table :type=2 :tableInfo="paperInfos" :tableTitle="tableTitle"
                                  @operate="butOperate"></my-table>
                        <my-pagination :pageshow="pageshow" :total="total" :queryInfo.sync="queryInfo" @qry="doQuery"/>
                    </div>
                    <my-person v-if="rCardType === 3" :pwdType=1 />
                    <my-uppaper v-if="rCardType === 2" :paperData="paperData" :title.sync="title"
                                :rCardType.sync="rCardType" @back="doQuery"></my-uppaper>
                </el-card>
            </div>
        </multipane>

 <!--        论文的支付界面-->
        <el-dialog
                title="请选择您的支付方式"
                :visible.sync="payVisible"
                width="30%"
                custom-class="pay">
            <el-dialog
                    width="30%"
                    :title="payTypeName + '支付'"
                    class="wx"
                    :visible.sync="payTypeVisible"
                    append-to-body
                    height="320px"
                    @close="wxClose">
                <img style="width:200px; height:200px;" :src="payPath"/>
                <div style="margin:10px"><span >请使用{{payTypeName}}扫描二维码进行支付</span></div>
            </el-dialog>
            <ul>
                <li style="font-size:14px">请选择您的支付方式</li>
                 <li>
                     <el-button @click="payType(1)" icon="iconfont icon-weixinzhifu" style="margin-right:30px">&nbsp微信</el-button>
                     <el-button @click="payType(2)" icon="iconfont icon-zhifubao">&nbsp支付宝</el-button>
                 </li>
                <li>支付金额：<span style="color:#e6a23c;">￥</span><span style="color:#e6a23c; font-size:28px">{{payMoney}}</span></li>
            </ul>
        </el-dialog>

<!--        论文的详细信息界面-->
        <el-dialog
                title="论文信息"
                :visible.sync="paperDetailVisible"
                width="700px"
                custom-class="paper-detail"
                style="margin-top:7vh">
            <my-paper-detail :type=2 :paper="paper" :options="options" @postil="getPostil"/>
        </el-dialog>
    </div>
</template>

<script>
    import _ from 'lodash'
    import MySearch from '../../common/mySearch'
    import MyTable from '../../common/myTable'
    import MyForm from '../../common/myForm'
    import MyPagination from '../../common/myPagination'
    import {Multipane, MultipaneResizer} from 'vue-multipane'
    import myPerson from '../../common/person'
    import myUppaper from './upPaper'
    import service from "../../../utils/request";
    import {getClientHeight, getValueByKey} from "../../../utils/common";
    import MyPaperDetail from '../../common/paperDetail'
    import {Message} from 'element-ui';
    import {options} from "../../../utils/config"

    export default {

        components: {
            MySearch,
            MyTable,
            MyForm,
            Multipane,
            MultipaneResizer,
            MyPagination,
            myPerson,
            myUppaper,
            MyPaperDetail
        },
        // 配置了只读的数据
        data() {
            return {
                clientHeight:'',
                heightReset:true,
                // 表格展示头
                tableTitle: [
                    {prop: "id", label: "ID", minWidth: '20%', },
                    {prop: "name", label: "论文名称", minWidth: '60%',isPopOver:true},
                    {prop: "number", label: "论文编号", minWidth: '35%',},
                    {prop: "money", label: "订单金额(￥)", operateButton:[], minWidth: '25%',},
                    {prop: "pay_mode", label: "支付方式", operateButton:[], minWidth: '25%',},
                    {prop: "status_name", label: "论文状态", operateButton:[], minWidth: '25%'},
                ],
                //表格展示操作按钮
                operateButton: [
                    {label: '去付款', operateType: 1},
                ],
                title:'新增',
                //添加/修改机构信息验证规则
                formRules: {
                    name: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {max: 32, message: '长度不能超过32个字符', trigger: 'blur'}
                    ],
                    uuid: [
                        {required: true, message: '请输入唯一标识', trigger: 'blur'},
                        {max: 32, message: '长度不能超过32个字符', trigger: 'blur'}
                    ],
                },
                paperData: {},
                paperInfos:[],

                //分页显示区域配置信息
                queryInfo: {query: "", pagenum: 1, pagesize: 10},
                total: 0,
                pageshow: true,
                //根据类型判断右侧显示什么区域
                // 1:论文列表， 2：上传论文， 3：个人中心
                rCardType:1,
                active:"1",
                payVisible:false,
                payTypeVisible:false,
                payTypeName:'',
                payMoney:'',

                paperDetailVisible:false,
                payInfo:{},
                payPath:'',
                paper:{},
                timer: null,
                options: options

            }
        },
        methods: {

            //表格信息操作按钮的映射 3代表编辑, 1代表去支付, 其他代表点击详细信息
            butOperate(val) {
                if (val.type === 3) {
                    this.rCardType = 2
                    this.paperData = _.cloneDeep(val.info)
                    this.title = '编辑'
                } else if (val.type === 1) {
                    this.payMoney = val.info.money
                    this.payVisible = true
                    this.payInfo = {
                        money: val.info.money,
                        title: val.info.name,
                        number: val.info.number,
                    }
                }else if (val.type === 2) {return}
                else {
                    this.paper = _.cloneDeep(val.info)
                    let author = _.cloneDeep(getValueByKey(val.info["author_list"], val.info.manage_author_id))
                    this.paper["author_name"] = author["author_name"]
                    this.paper["addr"] = author["addr"]
                    this.paper["phone"] = author["phone"]
                    this.paperDetailVisible = true
                }
            },

            doQuery() {
                service.request({
                    method: "get",
                    url: "/paper",
                    params: {pagenum: this.queryInfo.pagenum,  pagesize:this.queryInfo.pagesize}
                }).then(res => {
                    this.total = _.cloneDeep(res.data.total)
                    this.paperInfos = _.cloneDeep(res.data.paperList)
                    this.paperInfos.map((item, index) => {
                        if (item.status === '1' || item.status === '2' || item.status === '3') {
                            item["operateButton"] = [{label: '编辑', operateType: 3}]
                        } else if(item.status === '5') {
                            item["operateButton"] = [{label: '开发票', operateType: 2}]
                        }else{
                            item["operateButton"] = this.operateButton
                        }
                        item["status_name"] = getValueByKey(this.options, 'value', item.status).label

                        item.author_list.map(author => {
                            author.manage = ''
                        })
                    })
                })
            },

            payType(type){
                this.payTypeVisible = true
                if(type === 1){
                    this.payTypeName='微信'
                    this.wechatpay()
                }
                if(type === 2){
                    this.payTypeName='支付宝'
                    this.zfbPay()
                }
            },

            zfbPay(){
                service.request({
                    method: "put",
                    url: "/alipay",
                    data: this.payInfo
                }).then(res=>{
                    this.payPath = res.data
                    this.setToTimer()
                })
            },

            wechatpay(){
                service.request({
                    method: "put",
                    url: "/wechatpay",
                    data: this.payInfo
                }).then(res=>{
                    this.payPath = res.data
                    this.setToTimer()
                })
            },

            //定制定时器轮询后台，判断是否支付成功
            setToTimer() {
                if (this.timer == null) {
                    this.timer = setInterval(() => {
                        service.request({
                            method: "get",
                            url: "/order_status",
                            params: this.payInfo
                        }).then(res => {
                            if (res.data) {
                                Message.success('支付成功')
                                this.payTypeVisible = false
                                this.payVisible = false
                                this.wxClose()
                                this.doQuery()
                            }
                        })
                    }, 3000)
                }
            },

            //支付关闭之后,清除定时器
            wxClose(){
                 clearInterval(this.timer)
                 this.timer = null
            },

            getPostil(){}

        },
        mounted(){
            if(this.$store.getUserName === ""){
                Message.warnning('没有登录，请登录之后访问')
            }
            this.doQuery()
            this.clientHeight = getClientHeight() - 100
            // window.onresize = (e) => {
            //     this.heightReset = false;
            //     this.$nextTick(() => {
            //         this.clientHeight = getClientHeight() - 100
            //         this.heightReset = true
            //     })
            // };
        }
    }


</script>

<style>
    #paper{
        width:80%;
        margin-top:60px
    }
        .right-area {
        display:flex;
        justify-content: center;
        text-align: left;
        width: 80%;
        overflow-y: auto;
        overflow-x: hidden;
    }

    /* 左侧属性 */
    .left-area {
        display:flex;
        justify-content: center;
        width: 20%;
        overflow-y: auto;
        overflow-x: hidden;
    }

    .left-area .el-menu-item:hover {
        background-color:white !important;
        color: #409EFF !important;
    }

    .left-area .el-menu-item:focus{
        background-color:white !important;
    }

    .pay  .el-dialog__body{
        text-align:center !important
    }

    .wx .el-dialog__body{
        text-align:center !important
    }

    .pay ul{
        list-style:none
    }
    .pay li{
        margin:20px;
        font-size:18px
    }

    .wx .el-dialog__header, .zfb .el-dialog__header{
        background: rgb(94,173,184);
        padding:10px 20px 10px;
    }

    .wx .el-dialog__headerbtn .el-dialog__close, .zfb .el-dialog__headerbtn .el-dialog__close{
        color:black
    }

    .wx .el-dialog__headerbtn .el-dialog__close:hover, .zfb .el-dialog__headerbtn .el-dialog__close:hover{
        color:white
    }

</style>
