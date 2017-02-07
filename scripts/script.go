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
	"github.com/astaxie/beego/orm"
	_ "github.com/go-sql-driver/mysql"
)


type Sjr struct{
	Title string
	Issn string `orm:"pk"`
	Sjr string
	Index_sjr string
	Cites string
}


type Model struct {
	SortName string `csv:"ShortName"`
	LongName string `csv:"LongName"`
	Issn     string `csv:"Issn"`
	Sjr string `csv:"Sjr"`
	Index string `csv:"Index"`
}


const AliasName string = "default"
const NameDriver string = "mysql"
const Name string = "root"
const Pass string = "12345"
const NameDB string = "trivialbox"

const UrlDB string = Name + ":" + Pass + "@/" + NameDB + "?charset=utf8"

func init() {
	orm.RegisterDriver(
		NameDriver,
		orm.DRMySQL,
	)

	orm.RegisterModel(
		new(Sjr),
	)

	orm.RegisterDataBase(
		AliasName,
		NameDriver,
		UrlDB,
		100,
	)
}

func ORM() orm.Ormer {
	o := orm.NewOrm()
	o.Using(AliasName)
	return o
}

func GetSjr(isnn string) Sjr {
	sjr := Sjr{
		Issn:isnn,
	}
	err := ORM().Read(&sjr)
	if err == orm.ErrNoRows {
		fmt.Println("No result found.")
	} else if err == orm.ErrMissPK {
		fmt.Println("No primary key found.")
	}
	return sjr
}

func ReformarIssn(issn string) string{
	var issnFinal string
	for _, char := range strings.Split(issn,""){
		if (char != "-"){
			issnFinal+=char
		}
	}

	return "ISSN " + issnFinal
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
			sjr := GetSjr(ReformarIssn(issn[1]))
			knowledge = append(knowledge, Model{
				SortName: short_name[1],
				LongName: string(parser.Raw()),
				Issn:     issn[1],
				Sjr:sjr.Sjr,
				Index:sjr.Index_sjr,

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
