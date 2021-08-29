<template>
    <div id="myForm">
        <el-form-item v-for="(item, idx) in fieldList" :key="idx" :label="item.label" :prop="item.value"
                      :style = "`display:${item.display ? item.display : 'inline-block' }`"
        >
            <el-input v-if="item.type === 'input'" v-model="formData[item.value]"
                      :disabled="item.disabled" :style="`width:${item.width ? item.width : '250px'}`"
            ></el-input>
            <el-input v-if="item.type === 'num-input'" v-model.number="formData[item.value]"
                      :disabled="item.disabled" :style="`width:${item.width ? item.width : '250px'}`"
            ></el-input>
            <el-input type="textarea" v-if="item.type === 'textarea'" v-model="formData[item.value]"
                      :disabled="item.disabled" :style="`width:${item.width ? item.width : '250px'}`"
            ></el-input>
            <el-select v-if="item.type === 'select'" v-model="formData[item.value]" :placeholder="item.placeholder"
                       :style="`width:${item.width ? item.width : '250px'}`">
                <el-option :label="i.name" :value="i.id" v-for="i in item.sINFO"></el-option>
            </el-select>
            <el-checkbox-group :style="`width:${item.width}`" v-if="item.type === 'checkbox'"
                               v-model="formData[item.value]">
                <el-checkbox v-for="j in item.sINFO"  :label="j.value">{{j.lb}}</el-checkbox>
            </el-checkbox-group>
            <my-upload v-if="item.type === 'upload'" :options="item.options" :value.sync="formData[item.value]"/>
        </el-form-item>
    </div>
</template>

<script>
    import MyUpload from './myUpload'
    export default {
        name: "myForm",
        components: {MyUpload},
        props:{
            formData:Object,
            fieldList:Array,
        }
    }
</script>

<style scoped>

</style>