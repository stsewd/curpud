package main

import (
	"net/http"
	"golang.org/x/net/html"
	"regexp"
	"github.com/gocarina/gocsv"
	"os"
	"strconv"
	"fmt"
	"sync"
)

type Knowledge struct {
	SortName string `csv:"ShortName"`
	LongName string `csv:"LongName"`
	Issn string     `csv:"Issn"`
}

func GetDataKnowledge(url string) (knowledge []Knowledge) {
	resp, _ := http.Get(url)

	parser := html.NewTokenizer(resp.Body)
	for {
		tokenType := parser.Next()
		if tokenType == html.ErrorToken {
			break
		}

		valid := regexp.MustCompile(`^\d*\. (.*)`)
		short_name := valid.FindStringSubmatch(string(parser.Raw()))

		if len(short_name) != 0  {
			for index:=0; index < 3 ;index++  {
				tokenType = parser.Next()
			}
			valid1 := regexp.MustCompile(`ISSN: (.*)`)
			issn := valid1.FindStringSubmatch(string(parser.Raw()))

			for index := 0; index < 3; index++{
				tokenType = parser.Next()
			}

			knowledge = append(knowledge, Knowledge{
				SortName:short_name[1],
				LongName:string(parser.Raw()),
				Issn:issn[1],
			})
		}else {
			continue
		}

	}
	fmt.Println(url)
	return
}
func InitKnowledge() (knowledge []Knowledge) {
	var wg sync.WaitGroup

	url := "http://ip-science.thomsonreuters.com" +
		"/cgi-bin/jrnlst/jlresults.cgi?PC=MASTER&mode=print&Page="
	wg.Add(46)
	for index := 1; index < 47; index++ {
		urlTem := url + strconv.Itoa(index)
		go func(urlTem string) {
			defer wg.Done()
			knowledge = append(knowledge, GetDataKnowledge(urlTem)...)
		}(urlTem)
	}
	wg.Wait()
	return

}

func SaveData(nameFile string, data interface{}) {
	nameFile = nameFile + ".csv"
	file, err := os.OpenFile(nameFile, os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	gocsv.MarshalFile(data, file)
}

func main() {
	
	SaveData("knowledge",InitKnowledge())


}

