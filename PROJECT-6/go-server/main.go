package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"

	"github.com/kataras/iris/v12"
)

func main() {
	app := iris.New()

	app.Post("/compare", func(ctx iris.Context) {
		// Upload true_csv
		log.Println("Api hit")
		trueFile, trueHeader, err := ctx.FormFile("true_csv")
		if err != nil {
			ctx.StopWithStatus(400)
			return
		}
		defer trueFile.Close()

		// Upload test_csv
		testFile, testHeader, err := ctx.FormFile("test_csv")
		if err != nil {
			ctx.StopWithStatus(400)
			return
		}
		defer testFile.Close()

		// Save both files to temp directory
		os.MkdirAll("uploads", 0755)
		truePath := filepath.Join("uploads", trueHeader.Filename)
		testPath := filepath.Join("uploads", testHeader.Filename)
		out1, _ := os.Create(truePath)
		defer out1.Close()
		_, _ = trueFile.Seek(0, 0)
		_, _ = out1.ReadFrom(trueFile)

		out2, _ := os.Create(testPath)
		defer out2.Close()
		_, _ = testFile.Seek(0, 0)
		_, _ = out2.ReadFrom(testFile)

		// Output path
		outputPath := "output_translations.csv"

		// Call the Python script
		log.Println("Calling Python script...")
		log.Println(truePath, testPath, outputPath)
		cmd := exec.Command("python3", "main.py", truePath, testPath, outputPath)
		output, err := cmd.CombinedOutput()
		if err != nil {
			ctx.StatusCode(500)
			ctx.WriteString(fmt.Sprintf("Python error: %s", string(output)))
			return
		}

		// Send the output CSV as response
		ctx.SendFile(outputPath, "output_translations.csv")

		// Clean up
		defer os.Remove(truePath)
		defer os.Remove(testPath)
		defer os.Remove(outputPath)
	})

	app.Listen(":3000")
}
