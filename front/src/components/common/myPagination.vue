<template>
    <div id="pagination">
        <el-pagination
                v-if="pageshow"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page.sync="queryInfo.pagenum"
                :page-sizes="[5, 10, 20, 100]"
                :page-size="queryInfo.pagesize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total"
                style="margin-top:10px"
        >
        </el-pagination>
    </div>

</template>

<script>
    export default {
        name: "pagination",
        props:{
            queryInfo:Object,
            total:Number,
            pageshow:Boolean,
        },
        data(){
            return{

            }
        },
        methods:{
            handleSizeChange(newSize) {
                this.queryInfo.pagesize = newSize;
                this.$emit("updata:queryInfo", this.queryInfo);
                this.$emit('qry', true)
            },
            handleCurrentChange(newPage) {
                this.queryInfo.pagenum = newPage;
                this.$emit("updata:queryInfo", this.queryInfo);
                this.$emit('qry', true)
            },
        }
    }
</script>

<style scoped>

</style>
