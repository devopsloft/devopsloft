ui = true

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 1
}

storage "file" {
  "path" = "/vault/data"
}

api_addr = "http://127.0.0.1:8200"
