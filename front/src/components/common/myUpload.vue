<template>
    <div id="upload">
        <span>上传{{options.title}}格式文档<span style="font-size:12px; color:#e6a23c">(必传)</span></span>
        <el-upload
                ref="upload"
                :multiple="false"
                 list-type="picture-card"
                :action="options.urlPath"
                :on-success="handleSuccess"
                :before-upload="handleUpload"
                :accept="options.accept"
                :show-file-list="false"
                :limit="1">
            <img v-if="fileExt === 'pdf'" src="../../assets/img/PDF.jpg" class="avatar">
            <img v-else-if="fileExt === 'docx'" src="../../assets/img/WORD.jpg" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
        <div v-if="fileName !== ''">{{fileName}}</div>
<!--        <span style=" transform: translate(160px, -75px);display: block;color:#409EFF"><i class="el-icon-refresh"></i>上传文件</span>-->


    </div>
</template>

<script>
    import {Message} from 'element-ui';

    import axios from "axios";
    import _ from "lodash";

    export default {
        name: "mat-upload",
        props: {
            options: Object,
            value: String,
            name:String,
        },
        data(){
            return{
                fileExt:'',
                fileName:''
            }
        },
        watch: {
            name: {
                handler(val) {
                    if(val !== '' && typeof(val) != "undefined") {
                        this.fileExt = val.replace(/.+\./, "")
                        this.fileName = val
                    }else{
                        this.fileExt = ''
                        this.fileName = ''
                    }
                },immediate: true,
            },

        },
        methods:{
            handleUpload(file) {
                this.$store.commit("setLoading", true)

            },

            handleSuccess(res, file) {
                this.$store.commit("setLoading", false)
                this.fileExt = file.name.replace(/.+\./, "");
                this.fileName = res.data.old_name
                this.$refs.upload.clearFiles()
                this.$emit('update:value', res.data.save_path)
                this.$emit('update:name', res.data.old_name)
            }
        }
    }
</script>

<style>
    .upload-warn {
        color: red;
    }

    .upload-tip {
        line-height: 25px;
        font-size: 14px;
        color: black;
    }

    .box-card {
        margin-bottom: 20px;
    }

    .avatar {
        transform: translate(-2px, -2px);
    }

</style>