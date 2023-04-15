import React, { useState } from "react"
import Dropzone, { DropzoneState } from "react-dropzone"
import styles from "./App.module.scss"
import "destyle.css"

function App() {
  const [pdfFile, setPdfFile] = useState<File | undefined>(undefined)
  const [isChatReady, setIsChatReady] = useState<boolean>(false)
  const [question, setQuestion] = useState<string>("")
  const [answer, setAnswer] = useState<string>()

  const handleDrop = (acceptedFiles: File[]) => {
    console.log(acceptedFiles[0])
    setPdfFile(acceptedFiles[0])
  }

  const handleUpload = () => {
    console.log("upload button clicked")

    if (pdfFile) {
      const formData = new FormData()
      formData.append("pdfFile", pdfFile)

      fetch(process.env.REACT_APP_API_URL + "/bots", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          console.log(response)
          setIsChatReady(true)
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuestion(event.target.value)
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    if (question) {
      fetch(process.env.REACT_APP_API_URL + `/bots?question=${question}`).then(
        (response) => {
          response.json().then((data) => {
            setAnswer(data.answer)
          })
        }
      )
    }
    // setQuestion("")
  }

  return (
    <>
      <Dropzone onDrop={handleDrop} accept={{ "application/pdf": [".pdf"] }}>
        {({ getRootProps, getInputProps }: DropzoneState) => (
          <div {...getRootProps()} className={styles.dragArea}>
            <input {...getInputProps()} />
            <p>
              PDFファイルをドラッグアンドドロップするか、ここをクリックして選択してください。
            </p>
            <em>(Only *.pdf file will be accepted)</em>
          </div>
        )}
      </Dropzone>
      {pdfFile && (
        <div className={styles.uploadArea}>
          <div className={styles.selectedFile}>
            <p>選択されたPDFファイル: {pdfFile.name}</p>
          </div>
          <button className={styles.uploadBtn} onClick={handleUpload}>
            Upload
          </button>
        </div>
      )}
      {isChatReady && (
        <div>
          <form onSubmit={handleSubmit} className={styles.form}>
            <label>
              <span className={styles.labelText}>Enter Text:</span>
              <input
                type="text"
                value={question}
                onChange={handleChange}
                className={styles.input}
              />
            </label>
            <button type="submit" className={styles.button}>
              Send
            </button>
          </form>
          {answer && <p className={styles.answer}>{answer}</p>}
        </div>
      )}
    </>
  )
}
export default App
