FROM node:alpine3.15

ARG USERNAME=oces

ENV HOME=/home/$USERNAME

RUN set -xe && \
    apk add --update sudo && \
    adduser -D $USERNAME && \
    echo "$USERNAME ALL=(root) NOPASSWD: ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

WORKDIR $HOME/app

COPY ./package.json .

RUN npm install

COPY . .

EXPOSE 5000

USER $USERNAME

CMD ["npm","start"]