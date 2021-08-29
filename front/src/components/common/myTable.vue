<template>
    <div id="my-table">
        <el-table
                :data="tableInfo"
                border
                min-height="680px">
            <el-table-column v-for="(item, index) in tableTitle" :key="index"
                             :prop=item.prop
                             :label=item.label
                             :min-width=item.minWidth
                             align="center">
                <template  slot-scope="scope">
                                        <!-- tips悬浮提示 -->
                     <el-popover width="300" v-if="item.isPopOver" trigger="hover" placement="top"
                                 :content="scope.row[item.prop]" :disabled="scope.row[item.prop].length <= 36"
                     >
<!--                        <p v-if="scope.row[item.prop].length > 36" :style="`margin:3px`">{{scope.row[item.prop]}}</p>-->
                        <div slot="reference" class="name-wrapper">
                            <span class="myNote" v-if="scope.row[item.prop].length <= 36">{{scope.row[item.prop]}}</span>
                            <span class="myNote" v-if="scope.row[item.prop].length > 36">{{scope.row[item.prop]}} ...</span>
                        </div>
                    </el-popover>
                    <div v-else>
                        <div><span>{{ scope.row[item.prop] }}</span></div>
                        <div style="color:#409EFF; font-size:12px; cursor: pointer;">
                        <span @click="$emit('operate', {type:5, info:scope.row})"
                              v-if="item.prop === 'status_name'">
                        详细</span>
                        </div>
                    </div>

                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="40%" align="center">
                <template slot-scope="scope">
                    <el-button
                            :disabled='item.disabled ? item.disabled : false'
                            v-for="(item, index) in scope.row.operateButton" :key="index" class="el-operation"
                            type="text" size="mini" @click="$emit('operate', {type:item.operateType, info:scope.row})">
                        {{item.label}}
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>

    
</template>

<script>

    export default {
        name: "myTabel",
        props: {
            tableInfo: Array,
            tableTitle: Array,
            type:Number
        },
    }
</script>

<style>

.myNote{
  display:-webkit-box;
  text-overflow:ellipsis;
  overflow:hidden;
  -webkit-line-clamp: 2;
  -webkit-box-orient:vertical;
}

#my-table .el-popper{
    width:20%
}



</style>