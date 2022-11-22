# fast-api-upload-issue

This repo contains the minimum necessary code to reproduce a bug(see https://github.com/tiangolo/fastapi/issues/5141) with fastAPI upload, in which sending multiple paralel requests to an endpoint using `uploadFile` causes some requests to hang, as in they don't complete nor error out.

This repo constains a docker-compose and Dockerfile, and can be used with VSCode's devcontainer.

## Steps to reproduce

clone the repo: `git clone git@github.com:guites/fast-api-upload-issue.git`

Using VS Code's devcontainer:

- Open the directory with VS Code.
- Click on View -> Command Palette and select "Dev Containers: Reopen in Container"
- install dependencies `pip3 install -r requirements.txt`
- start the server by running `python3 main.py`

Using Docker:

- Build an image from the Dockerfile: `docker build . -t bug-repro-fastapi`
- Run that image, mapping to a port: `docker run -p 8000:8000 bug-repro-fastapi`

Then, access http://localhost:8000 and, using the file input, select a file bigger than ~60kb. The javascript code will automatically attempt to POST the file 100 times to the file upload endpoint, which will cause the hanging.

To check that the bug is indeed happening, open the developer tools' networking tab before starting the uploads:

![hang_requests](https://user-images.githubusercontent.com/71985299/178988390-f5e2060b-50e7-4328-8a22-fd635799cbf2.png)

You can then verify the error on the python process by going to the terminal and pressing `Ctrl + c`, which will output the following log:


>    INFO: 127.0.0.1:42746 - "POST /test HTTP/1.1" 200 OK
    ^CINFO: Shutting down
    INFO: Waiting for connections to close. (CTRL+C to force quit)
    ^CINFO: Finished server process [16982]
    ERROR: Traceback (most recent call last):
    File "/home/vscode/.local/lib/python3.9/site-packages/starlette/routing.py", line 638, in lifespan
    await receive()
    File "/home/vscode/.local/lib/python3.9/site-packages/uvicorn/lifespan/on.py", line 137, in receive
    return await self.receive_queue.get()
    File "/usr/local/lib/python3.9/asyncio/queues.py", line 166, in get
    await getter
    asyncio.exceptions.CancelledError
>
>    ERROR: Exception in ASGI application
    Traceback (most recent call last):
    File "/home/vscode/.local/lib/python3.9/site-packages/uvicorn/protocols/http/h11_impl.py", line 403, in run_asgi
    result = await app(self.scope, self.receive, self.send)
    File "/home/vscode/.local/lib/python3.9/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in call
    return await self.app(scope, receive, send)
    File "/home/vscode/.local/lib/python3.9/site-packages/fastapi/applications.py", line 269, in call
    await super().call(scope, receive, send)
    File "/home/vscode/.local/lib/python3.9/site-packages/starlette/applications.py", line 124, in call
    await self.middleware_stack(scope, receive, send)
    File "/home/vscode/.local/lib/python3.9/site-packages/starlette/middleware/errors.py", line 162, in call
    await self.app(scope, receive, _send)
    File "/home/vscode/.local/lib/python3.9/site-packages/starlette/exceptions.py", line 82, in call
    await self.app(scope, receive, sender)
    File "/home/vscode/.local/lib/python3.9/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in call
    await self.app(scope, receive, send)
    File "/home/vscode/.local/lib/python3.9/site-packages/starlette/routing.py", line 670, in call
    await route.handle(scope, receive, send)
    File "/home/vscode/.local/lib/python3.9/site-packages/starlette/routing.py", line 266, in handle
    await self.app(scope, receive, send)
    File "/home/vscode/.local/lib/python3.9/site-packages/starlette/routing.py", line 65, in app
    response = await func(request)
    File "/home/vscode/.local/lib/python3.9/site-packages/fastapi/routing.py", line 192, in app
    body = await request.form()
    File "/home/vscode/.local/lib/python3.9/site-packages/starlette/requests.py", line 254, in form
    self._form = await multipart_parser.parse()
    File "/home/vscode/.local/lib/python3.9/site-packages/starlette/formparsers.py", line 190, in parse
    async for chunk in self.stream:
    File "/home/vscode/.local/lib/python3.9/site-packages/starlette/requests.py", line 219, in stream
    message = await self._receive()
    File "/home/vscode/.local/lib/python3.9/site-packages/uvicorn/protocols/http/h11_impl.py", line 540, in receive
    await self.message_event.wait()
    File "/usr/local/lib/python3.9/asyncio/locks.py", line 226, in wait
    await fut
    asyncio.exceptions.CancelledError
    INFO: 127.0.0.1:42752 - "POST /test HTTP/1.1" 500 Internal Server Error
