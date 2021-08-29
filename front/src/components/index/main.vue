<template>
    <div class="index">
        <div class="banner">
            <swiper :options="swiperOptions1" ref="mySwiper1">
                <swiper-slide style="width: 100%">
                    <img class="slide_img" src="../../assets/img/banner_1.jpg">
                </swiper-slide>
                <swiper-slide>
                    <img class="slide_img" src="../../assets/img/banner_2.jpg">
                </swiper-slide>
                <div class="swiper-pagination"></div>
                <div class="swiper-button-prev" slot="button-prev"></div>
                <div class="swiper-button-next" slot="button-next"></div>
            </swiper>
        </div>
        <div class="info">
            <el-card>
                <router-view/>
            </el-card>
        </div>

    </div>
</template>


<script>
    import axios from 'axios'
    import {getClientHeight} from '../../utils/common.js'
    import myMarkdown from '../../assets/img/cfp/index.md'
    import {Swiper, SwiperSlide, directive} from 'vue-awesome-swiper'

    export default {
        name: "index",
        data(){
            return{
                htmlMD:'',
                swiperOptions1: {
                    pagination:{
                        el:'.swiper-pagination',
                        clickable:true,
                    },
                    slidePreView:1,
                    autoplay:{
                        autoplay:false,
                        delay:2000,
                        disableOnInteraction:false
                    },
                    spaceBetween:0,
                    loop:true,
                    pagination: '.swiper-pagination',
                    navigation: {
                        nextEl: '.swiper-button-next',
                        prevEl: '.swiper-button-prev'
                    },

                },
            }
        },
        components: { myMarkdown, Swiper, SwiperSlide, directive },
        methods:{
            // get_mark_data() {
            //     axios.get("/index/index.md").then((response) => {
            //         this.htmlMD = response.data;
            //     });
            // }
        },
    }
</script>

<style scoped>
    .banner{
        border-top: solid 4px #007944;
    }
    .el-card{
        transition: all .5s;
    }
    .el-card:hover {
         box-shadow: 0px 2px 10px 0px rgb(16 16 16 / 0.4);;
	    -webkit-box-shadow: 0px 2px 10px 0px rgb(16 16 16 / 0.4);;
	    -moz-box-shadow: 0px 2px 10px 0px rgb(16 16 16 / 0.4);;
    }
    .index{
        width: 100%;
    }
    .info{
        width:80%; margin-left:10%; margin-top:30px
    }
    .right-area {
        display:flex;
        justify-content: center;
        background:white;
        text-align: left;
        width: 70%;
        overflow-y: auto;
        overflow-x: hidden;
    }

    /* 左侧属性 */
    .left-area {
        display:flex;
        justify-content: center;
        background:white;
        width: 30%;
        overflow-y: auto;
        overflow-x: hidden;
    }

    .md-title{
        font-size:18px
    }

        .slide_img{
        width:100%;
        cursor: pointer;
        transition: all 0.4s;
    }

    .slide_img:hover{
        transform: scale(1.05);
    }

    .banner{
        margin-top:60px;
        overflow:hidden
    }

</style>