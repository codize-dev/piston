#!/usr/bin/env bash
set -euo pipefail

curl -LO https://go.dev/dl/go1.25.5.linux-amd64.tar.gz
tar -xzf go1.25.5.linux-amd64.tar.gz
rm go1.25.5.linux-amd64.tar.gz

# Build GOCACHEPROG binary for read-only cache access
CGO_ENABLED=0 ./go/bin/go build -o cacheprog cacheprog.go

# Pre-build standard library cache
export GOCACHE="$PWD/cache"
mkdir -p "$GOCACHE"
CGO_ENABLED=0 ./go/bin/go build std

# Pre-download selected golang.org/x modules for offline builds.
export GOPATH="$PWD/gopath"
mkdir -p "$GOPATH"
CGO_ENABLED=0 ./go/bin/go mod download
