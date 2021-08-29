<template>
    <div id="mySearch" style="float:left">
        <el-select v-model="selectInfo.value" filterable placeholder="请选择" size="small">
            <el-option v-for="item, index in selectInfo.options" :label="item.label" :key="index"
                       :value="item.value">
            </el-option>
        </el-select>
    </div>
</template>

<script>
    import { reactive, ref, watch, onMounted, provide } from '@vue/composition-api';

    export default {
        name: "mySearch",
        props: {
            selectInfo: Object
        },
        setup(props, {emit}) {
            function doQry(){
                emit("update:qryUserId", props.selectInfo.value);
            }
            return {doQry}
        }
    }
</script>

<style scoped>

</style>