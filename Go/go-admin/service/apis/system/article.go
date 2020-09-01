package system

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"go-admin/tools/app"
	"net/http"
)

func GetArticleList(c *gin.Context) {

	var res app.Response
	res.Data = "hello world 2 ！"

	fmt.Println(res.Data)
	c.JSON(http.StatusOK, res.ReturnOK())
}
