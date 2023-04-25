FROM python:3.10

RUN apt update
RUN pip install Flask \
                flask-cors \
                langchain \
                python-dotenv \
                pypdf \
                chromadb \
                tiktoken

WORKDIR /backend

CMD [ "bash" ]
