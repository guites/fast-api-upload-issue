FROM mcr.microsoft.com/vscode/devcontainers/python:3.9

WORKDIR /workspace

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py" ]