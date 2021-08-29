module.exports = {
    devServer: {
        open: false, //配置自动启动浏览器
        proxy: "http://192.168.1.13:1122"
    },
    lintOnSave: false,
    chainWebpack: config => {
        config.module.rule('md')
            .test(/\.md/)
            .use('vue-loader')
            .loader('vue-loader')
            .end()
            .use('vue-markdown-loader')
            .loader('vue-markdown-loader/lib/markdown-compiler')
            .options({
                raw: true
            })
    }
}
