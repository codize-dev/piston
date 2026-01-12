package main

import (
	"bufio"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

type Request struct {
	ID       int64  `json:"ID"`
	Command  string `json:"Command"`
	ActionID []byte `json:"ActionID,omitempty"`
}

type Response struct {
	ID            int64    `json:"ID"`
	KnownCommands []string `json:"KnownCommands,omitempty"`
	Miss          bool     `json:"Miss,omitempty"`
	OutputID      []byte   `json:"OutputID,omitempty"`
	Size          int64    `json:"Size,omitempty"`
	DiskPath      string   `json:"DiskPath,omitempty"`
}

func main() {
	if len(os.Args) < 2 {
		os.Exit(1)
	}
	cacheDir := os.Args[1]

	enc := json.NewEncoder(os.Stdout)
	enc.Encode(Response{ID: 0, KnownCommands: []string{"get", "close"}})

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		var req Request
		if err := json.Unmarshal(scanner.Bytes(), &req); err != nil {
			continue
		}

		switch req.Command {
		case "get":
			enc.Encode(handleGet(cacheDir, req))
		case "close":
			enc.Encode(Response{ID: req.ID})
			return
		}
	}
}

func handleGet(cacheDir string, req Request) Response {
	actionHex := hex.EncodeToString(req.ActionID)
	if len(actionHex) < 2 {
		return Response{ID: req.ID, Miss: true}
	}

	actionPath := filepath.Join(cacheDir, actionHex[:2], actionHex+"-a")
	data, err := os.ReadFile(actionPath)
	if err != nil {
		return Response{ID: req.ID, Miss: true}
	}

	outputID, size, err := parseActionEntry(data)
	if err != nil {
		return Response{ID: req.ID, Miss: true}
	}

	outputHex := hex.EncodeToString(outputID)
	dataPath := filepath.Join(cacheDir, outputHex[:2], outputHex+"-d")
	if _, err := os.Stat(dataPath); err != nil {
		return Response{ID: req.ID, Miss: true}
	}

	return Response{
		ID:       req.ID,
		OutputID: outputID,
		Size:     size,
		DiskPath: dataPath,
	}
}

// parseActionEntry parses: "v1 <actionHex> <outputHex> <size> <time>\n"
func parseActionEntry(data []byte) ([]byte, int64, error) {
	line := strings.TrimSpace(string(data))
	fields := strings.Fields(line)
	if len(fields) < 4 || fields[0] != "v1" {
		return nil, 0, os.ErrInvalid
	}

	outputID, err := hex.DecodeString(fields[2])
	if err != nil {
		return nil, 0, err
	}

	size, err := strconv.ParseInt(fields[3], 10, 64)
	if err != nil {
		return nil, 0, err
	}

	return outputID, size, nil
}
