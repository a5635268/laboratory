package test

import (
	"github.com/spf13/cobra"
	"go-admin/database"
	"go-admin/global"
	"go-admin/models"
	"go-admin/pkg/logger"
	"go-admin/tools"
	"go-admin/tools/config"
)

var (
	configYml string
	port      string
	mode      string
	StartCmd  = &cobra.Command{
		Use:     "test",
		Short:   "用于测试语法的命令",
		Example: "go-admin test",
		PreRun: func(cmd *cobra.Command, args []string) {
			 setup()
		},
		RunE: func(cmd *cobra.Command, args []string) error {
			return run()
		},
	}
)

func init() {
	StartCmd.PersistentFlags().StringVarP(&configYml, "config", "c", "config/settings.yml", "Start server with provided configuration file")
	StartCmd.PersistentFlags().StringVarP(&port, "port", "p", "8000", "Tcp port server listening on")
	StartCmd.PersistentFlags().StringVarP(&mode, "mode", "m", "dev", "server mode ; eg:dev,test,prod")
}

func setup() {
	//1. 读取配置
	configYml := "config/settings.dev.yml"
	config.Setup(configYml)
	//2. 设置日志
	logger.Setup()
	//3. 初始化数据库链接
	database.Setup(config.DatabaseConfig.Driver)

	usageStr := `starting test`
	global.Logger.Debug(usageStr)

}

func run() error {
	return nil
}



func GetArticleList() {

}

func getArticle() {
	var data models.Article
	data.ArticleId = 1
	result, err := data.Get()
	tools.HasError(err, "抱歉未找到相关信息", -1)
	tools.Print(result)
}


