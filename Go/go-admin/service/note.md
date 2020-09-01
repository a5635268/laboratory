## 代码阅读

1. 分析CURD [ok]
2. 分析命令行执行并实现 [ok]
3. 模拟一个CURD,熟悉Gorm
4. 

~~~
// 命令注册：cmd/cobra.go:42

// 全局变量： global/adm.go:10

// 获取配置
viper.GetString("settings.application.mode")

// 组件加载
// tools/config->cmd/api/server.go:54

// 日志使用
global.Logger.
~~~
