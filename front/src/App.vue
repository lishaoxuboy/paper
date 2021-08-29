<template>
  <div id="app"
       v-loading.fullscreen.lock="fullscreenLoading"
       :element-loading-text="loadingInfo"
       element-loading-background="rgba(0, 0, 0, 0.8)">
    <router-view/>
  </div>
</template>

<script>

  import {getCaCheRoleType, getCaCheName}  from './utils/localStorage'
export default {
    name: 'App',
    data() {
      return {
        loadingInfo: '正在上传论文原件，请稍后',
        fullscreenLoading: false,

      }
    },
    computed: {
      loading: function () {
        return this.$store.getters.getLoading
      }
    },
    watch: {
      loading: function (val) {
        this.fullscreenLoading = val
      }
    },
    methods: {
      saveState() {
          this.$store.commit("setUserName", getCaCheName());
         this.$store.commit("setRoleType", getCaCheRoleType());
      }
    },
    created() {
      this.saveState();
    },
  }
</script>


<style>

  #app .fl {
    float: left;
  }

  #app .fr {
    float: right;
    margin: 5px
  }

  #app .fm {
    float: left;
    margin: 5px
  }

  #app .el-table td, #app.el-table th{
      padding: 8px 0 !important;
  }

</style>
