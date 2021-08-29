<template>
        <div class="paper">
            <ul>
                <li class="fl tw">论文名称：</li>
                <li style="display: flow-root;" >{{paper.name}}</li>
            </ul>
            <ul>
                <li class="fl tw">联系作者姓名：</li>
                <li class="fl" style="width:200px; display: flow-root;">{{paper.author_name}}</li>
                <li class="fl tw" style="width:60px">手机：</li>
                <li class="fl" style="display: flow-root;" >{{paper.phone}}</li>
            </ul>
            <ul>
                <li class="fl tw">论文邮件地址：</li>
                <li style="display: flow-root;">{{paper.addr}}</li>
            </ul>
            <ul>
                <li class="fl tw">论文附件：</li>
                <li class="fl" style="width:500px;">
                    <el-button icon="iconfont icon-pdf" @click="down(1)" class="but-paper" style="margin-left:10px">
                        <img style="width:40px" alt="">
                        {{paper.pdf_name}}
                    </el-button>
                    <el-button icon="iconfont icon-word" @click="down(2)" class="but-paper" > {{paper.word_name}}</el-button>
                </li>
            </ul>
            <ul>
                <li class="fl tw">论文编号：</li>
                <li style="display: flow-root;">{{paper.number}}</li>
            </ul>
            <ul>
                <li class="fl tw">订单号：</li>
                <li style="display: flow-root;">{{paper.number}}</li>
            </ul>

            <div v-if="type === 1">
                <hr class="hr" style="height:7px">
                <ul>
                    <li class="fl tw">论文批注：</li>
                    <li class="fl">
                        <el-select style="width:200px" v-model="paper.status" placeholder="请选择">
                            <el-option
                                    v-for="item in options"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </li>
                    <li class="fl wt" style="margin-left:20px">支付价格(￥)：</li>
                    <li><el-input class="input_1" style="width:200px" step="1" v-model.number="paper.money" placeholder="请输入论文价格" /></li>
                </ul>
                <ul>
                    <li class="fl tw">备注：</li>
                    <li ><el-input type="textarea" style="width:512px" v-model="paper.comments" placeholder="请输入审核信息" /></li>
                </ul>
                <el-button style="width: 100px;margin-top: 10px;float:right" class="button" type="primary" round @click="$emit('toCommit', true)">确认</el-button>
            </div>

            <div v-else>
                <ul>
                    <li class="fl tw">论文状态：</li>
                    <li class="fl" style="width:200px">{{paper.status_name}}</li>
                    <li class="fl wt" style="margin-left:20px">支付价格(￥)：</li>
                    <li><span style="width:200px">{{paper.money}}</span></li>
                </ul>
                <ul>
                    <li class="fl tw">备注：</li>
                    <li><span style="width:512px; display: flow-root">{{paper.comments}}</span></li>
                </ul>
            </div>

        </div>
</template>

<script>
    export default {
        name: "paperDetail",
        props:{
            paper: Object,
            type:Number,
            options:Array
        },
        data(){
            return {
                postil:{
                    money:'',
                    comments:'',
                    status:''
                }
            }
        },
        methods:{
            down(val){
                let file_name = val === 1 ? this.paper.pdf_name : this.paper.word_name
                let file_path = val === 1 ? this.paper.pdf_path : this.paper.word_path
                let link = document.createElement('a');
                link.href = file_path
                link.setAttribute('download', file_name)
                document.body.appendChild(link)
                link.click()
            }
        }
    }
</script>

<style>
    .paper{
        color:#606266;
        font-size:14px
    }
    .paper ul {
        width: 650px;
        list-style: none;
        height:30px;
        line-height:30px;
        text-alient:left;
        display:inline-table;
        margin: 5px 0 5px 0;
        padding-left: 10px;
    }
    .paper ul li {
        border:1px soild black
    }

    .paper .tw {
        width: 110px;
        font-size: 14px;
        color: #99a9bf;
    }

    .paper .info {
        width: 500px
    }

    .but-paper{
        width:500px;
        height:65px;
        white-space: normal !important;
        margin:10px !important
    }

    .paper-detail{
        margin:auto !important;
    }

    .paper-detail .el-dialog__footer{
        padding:0 20px 20px
    }

    .paper-detail .el-dialog__body{
        padding:10px 20px 60px 20px;
    }

    .paper-detail .el-dialog__header{
            border-bottom: 1px #f1eded solid;
    }
    .input_1 .el-input__inner{
        height: 35px !important;
        line-height: 35px !important;
    }


</style>