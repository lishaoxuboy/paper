<template>
    <div id="paper">
        <multipane style="width: 100%">
            <div class="left-area" :style="`height:${clientHeight}px`" v-if="heightReset">
                <el-card style="width:98%; margin-top:20px; ">
                    <el-menu
                            :default-active="active"
                            class="el-menu-vertical-demo">
                        <el-menu-item index="1">
                            <i class="el-icon-document"></i>
                            <span slot="title">论文批准</span>
                        </el-menu-item>
                    </el-menu>
                </el-card>
            </div>
            <multipane-resizer/>
            <div class="right-area" :style="`height:${clientHeight}px`" v-if="heightReset">
                <el-card style="width:98%; margin-top:20px;overflow-y: auto; ">
                    <!--表格内容-->
                    <div>
<!--                        <el-button @click="doQuery" icon="el-icon-refresh" style="margin-bottom: 10px; padding: 10px;">刷新</el-button>-->
                        <my-table :tableInfo="paperInfos" :tableTitle="tableTitle" :operateButton="operateButton"
                                  @operate="butOperate" ></my-table>
                        <my-pagination  ref="pageInfo" :pageshow="pageshow" :total="total" :queryInfo.sync="queryInfo" @qry="doQuery"/>
                    </div>
                </el-card>
            </div>
        </multipane>

        <el-dialog
                title="论文信息"
                :visible.sync="paperDetailVisible"
                width="700px"
                custom-class="paper-detail"
                style="margin-top:7vh">
            <my-paper-detail :type='type' :paper="curPaper" :options="status" @toCommit="modifyPaper"/>
        </el-dialog>

    </div>
</template>

<script>
    import _ from 'lodash'
    import MySearch from '../../common/mySearch'
    import MyTable from '../../common/myTable'
    import MyForm from '../../common/myForm'
    import MyPaperDetail from '../../common/paperDetail'
    import MyPagination from '../../common/myPagination'
    import {Multipane, MultipaneResizer} from 'vue-multipane'
    import service from "../../../utils/request";
    import {options} from "../../../utils/config"
    import {getClientHeight, getValueByKey} from "../../../utils/common";
    import {Message} from 'element-ui';

    export default {
        components:
            {MySearch, MyTable, MyForm,Multipane, MultipaneResizer, MyPagination, MyPaperDetail},
        // 配置了只读的数据
        data() {
            return {
                // 表格展示头
                clientHeight:'',
                heightReset:true,
                // 表格展示头
                tableTitle: [
                    {prop: "id", label: "ID", minWidth: '20%', },
                    {prop: "name", label: "论文名称", minWidth: '60%',isPopOver:true},
                    {prop: "number", label: "论文编号", minWidth: '35%',},
                    {prop: "money", label: "订单金额(￥)", minWidth: '25%',},
                    {prop: "pay_mode", label: "支付方式",  minWidth: '25%',},
                    {prop: "status_name", label: "论文状态",  minWidth: '25%'},
                ],
                //表格展示操作按钮
                operateButton: [
                    {label: '去批注', operateType: 1},
                ],
                paperInfos:[],

                //分页显示区域配置信息
                queryInfo: {query: "", pagenum: 1, pagesize: 10},
                total: 0,
                pageshow: true,
                //根据类型判断右侧显示什么区域
                active:"1",
                paperDetailVisible:false,
                curPaper:'',
                options: options,
                status: [
                    {value: '2', label: '已审核'},
                    {value: '3', label: '拒稿'},
                    {value: '4', label: '已录用,待付款'},
                ],
                type:1

            }
        },
        methods: {
            // 去批注
            butOperate(val) {
                this.type = val.type === 5 ? 2 : 1
                this.curPaper = _.cloneDeep(val.info)
                this.paper = _.cloneDeep(val.info)
                let author = _.cloneDeep(getValueByKey(val.info["author_list"], val.info.manage_author_id))
                this.curPaper["author_name"] = author["author_name"]
                this.curPaper["addr"] = author["addr"]
                this.curPaper["phone"] = author["phone"]
                this.paperDetailVisible = true
             },

            doQuery() {
                let this_ = this
                service.request({
                    method: "get",
                    url: "/paper",
                    params: {pagenum: this.queryInfo.pagenum,  pagesize:this_.queryInfo.pagesize}
                }).then(res => {
                    this_.total = _.cloneDeep(res.data.total)
                    this_.paperInfos = _.cloneDeep(res.data.paperList)
                    this_.paperInfos.map((item, index) => {
                        // item.status = item.status === '1' ? '' : item.status
                        if (item.status === '1' || item.status === '2' || item.status === '3') {
                            item["operateButton"] = [{label: '去批注', operateType: 3}]
                        } else if (item.status === '5') {
                            item["operateButton"] = [{label: '去批注', operateType: 2, disabled: true}]
                        } else {
                            item["operateButton"] = this_.operateButton
                        }
                        item["status_name"] = getValueByKey(this_.options, 'value', item.status).label
                    })
                })
            },

            modifyPaper() {
                this.curPaper.status = this.curPaper.status === '0' ? '1' : this.curPaper.status
                if(this.curPaper.status === '4' && !this.curPaper.money){
                     Message.warning('录用之后,支付金额不能为空'); return
                }
                service.request({
                    method: "put",
                    url: "/paper",
                    data: this.curPaper
                }).then(res => {
                    Message.success('批注成功')
                    this.paperDetailVisible = false
                    this.doQuery();
                })
            }
        },
        mounted(){
            this.doQuery();
            this.clientHeight = getClientHeight() - 100
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

    .pay .el-dialog__body{
        text-align:center
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
