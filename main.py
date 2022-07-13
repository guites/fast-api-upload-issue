from fastapi import FastAPI, UploadFile, File
import uvicorn
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def main():
    content = """
        <body>
            <form method="post">
                <input id="fileinput" name="file" type="file" multiple>
            </form>
            <script>
                const input = document.getElementById('fileinput');
                
                const upload = (file) => {
                const formData = new FormData();
                formData.append('file', file);
                fetch('/test', {
                    method: 'POST',
                    body: formData
                }).then(
                    response => response.json() // if the response is a JSON object
                ).then(
                    success => console.log(success) // Handle the success response object
                ).catch(
                    error => console.log(error) // Handle the error response object
                );
                };

                const onSelectFile = () => {
                    for (var i = 0; i < 100; i++) {
                        upload(input.files[0]);
                    }
                }

                input.addEventListener('change', onSelectFile, false);
            </script>
        </body>
    """
    return HTMLResponse(content=content)


@app.post("/test")
async def test_upload(file: UploadFile = File(...)):
    try:
        await file.read()
    except Exception as e:
        print(str(e))
    finally:
        await file.close()
    

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)