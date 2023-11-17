FROM alpine:latest

RUN apk update && apk add bash git apache-ant

RUN git clone --branch version20.0.0 https://github.com/jindrapetrik/jpexs-decompiler.git

RUN cd jpexs-decompiler && ant build && chmod +x dist/ffdec.sh

WORKDIR /jpexs-decompiler/dist

ENTRYPOINT [ "./ffdec.sh" ]
