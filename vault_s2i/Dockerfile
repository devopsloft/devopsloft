FROM python:3-stretch

COPY . /
ARG VAULT_GUEST_PORT
RUN pip3 install --upgrade pip && \
    pip install -r /requirements.txt && \
    export VAULT_GUEST_PORT=$VAULT_GUEST_PORT && \
    j2 /config.hcl.j2 -o /config.hcl

FROM vault:1.1.2

COPY --from=0 /config.hcl /vault/config/config.hcl
