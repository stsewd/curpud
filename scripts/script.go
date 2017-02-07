package main

import (
	"bufio"
	"fmt"
	"github.com/gocarina/gocsv"
	"github.com/namsral/flag"
	"golang.org/x/net/html"
	"log"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"
	"sync"
)

type Model struct {
	SortName string `csv:"ShortName"`
	LongName string `csv:"LongName"`
	Issn     string `csv:"Issn"`
}

func GetDataKnowledge(url string) (knowledge []Model) {
	resp, _ := http.Get(url)

	parser := html.NewTokenizer(resp.Body)
	for {
		tokenType := parser.Next()
		if tokenType == html.ErrorToken {
			break
		}

		valid := regexp.MustCompile(`^\d*\. (.*)`)
		short_name := valid.FindStringSubmatch(string(parser.Raw()))

		if len(short_name) != 0 {
			for index := 0; index < 3; index++ {
				tokenType = parser.Next()
			}
			valid1 := regexp.MustCompile(`ISSN: (.*)`)
			issn := valid1.FindStringSubmatch(string(parser.Raw()))

			for index := 0; index < 3; index++ {
				tokenType = parser.Next()
			}

			knowledge = append(knowledge, Model{
				SortName: short_name[1],
				LongName: string(parser.Raw()),
				Issn:     issn[1],
			})
		} else {
			continue
		}

	}
	fmt.Println(url)
	return
}
func InitKnowledge() (knowledge []Model) {
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

func GetDataEbsco(url string) (ebsco []Model) {

	resp, _ := http.Get(url)
	parser := html.NewTokenizer(resp.Body)

	for {
		tokenType := parser.Next()
		if tokenType == html.ErrorToken {
			break
		}
		valid := regexp.MustCompile(`^<a.*JournalID=\d*'>`)
		tag_a := valid.MatchString(string(parser.Raw()))

		if tag_a {
			tokenType = parser.Next()
			sortName := string(parser.Raw())

			for a := 0; a < 15; a++ {
				tokenType = parser.Next()
			}
			logName := string(parser.Raw())[1:]

			for a := 0; a < 5; a++ {
				tokenType = parser.Next()
			}
			issn := strings.Join(strings.Fields(string(parser.Raw())), "")

			ebsco = append(ebsco, Model{
				Issn:     issn,
				LongName: logName,
				SortName: sortName,
			})

		} else {
			continue
		}
	}
	fmt.Println(url)
	return
}

func InitEbsco() (ebsco []Model) {

	var wg sync.WaitGroup
	url := "http://ejournals.ebsco.com/info/EJSTitles.asp?PageNo="
	wg.Add(323)
	for a := 1; a < 324; a++ {
		urlTem := url + strconv.Itoa(a)

		go func(urlTem string) {
			defer wg.Done()
			ebsco = append(ebsco, GetDataEbsco(urlTem)...)
		}(urlTem)

	}
	wg.Wait()
	return
}

func GetDataEmerald(url string) (emerald []Model) {
	file, err := os.Open(url)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		var model Model

		model.LongName = scanner.Text()
		scanner.Scan()
		model.Issn = scanner.Text()
		scanner.Scan()

		emerald = append(emerald, model)

	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return
}

func SaveData(nameFile string, data interface{}) {
	nameFile = "output/" + nameFile + ".csv"
	file, err := os.OpenFile(nameFile, os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	gocsv.MarshalFile(data, file)
}

func main() {
	var name string

	flag.StringVar(&name, "name", "", "get data base")
	flag.Parse()

	switch name {
	case "knowledge":
		SaveData("knowledge", InitKnowledge())
	case "ebsco":
		SaveData("ebsco", InitEbsco())

	case "emerald":
		SaveData("emerald", GetDataEmerald("input/emerald.txt"))
	default:
		fmt.Println("option no valida")
	}

}
