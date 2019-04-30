FROM vault:1.1.2

COPY . /

ARG VAULT_GUEST_PORT
RUN apk add --no-cache python3 && \
    pip3 install -r /requirements.txt && \
    export VAULT_GUEST_PORT=$VAULT_GUEST_PORT && \
    j2 /config.hcl.j2 -o /vault/config/config.hcl
