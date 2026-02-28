# Repository Guideline

## Project Overview

Piston is a high-performance, high-security code execution engine supporting 90+ programming languages. It enables safe code execution via an API server and operates in a sandboxed environment using Linux Isolate (namespaces + chroot + cgroup).

## Development Commands

### Starting and Stopping the Environment

```bash
./piston select dev          # Select development environment (first time only)
./piston start               # Start
./piston stop                # Stop
./piston restart             # Restart
./piston logs                # Show logs
./piston bash                # Open container shell
./piston rebuild             # Build and restart
```

### Code Formatting (Lint)

```bash
./piston lint                # Format all files with Prettier
npx prettier --write <path>  # Format specific files only
```

### Package Management

```bash
./piston list-pkgs                    # List available packages
./piston build-pkg <pkg> <ver>        # Build package
./piston clean-pkgs                   # Clean build artifacts
```

### CLI Setup

```bash
cd cli && npm i && cd -
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Docker Container                       │
├─────────────────────────────────────────────────────────────┤
│  api/                          cli/                          │
│  ├─ Express Server             ├─ yargs CLI                  │
│  ├─ Routes (api/v2.js)         └─ commands/                  │
│  ├─ Job Manager (job.js)           ├─ execute.js             │
│  ├─ Runtime Manager                └─ ppman.js               │
│  └─ Package Manager                                          │
├─────────────────────────────────────────────────────────────┤
│                    Isolate Sandbox                           │
│  (Linux namespaces + chroot + cgroup)                        │
├─────────────────────────────────────────────────────────────┤
│  packages/                                                   │
│  └─ <lang>/<version>/                                        │
│      ├─ metadata.json  (language info, aliases)              │
│      ├─ build.sh       (build script)                        │
│      ├─ run            (execution script)                    │
│      └─ environment    (environment variables)               │
└─────────────────────────────────────────────────────────────┘
```

### Main Components

| File | Role |
|---------|------|
| `api/src/index.js` | Express server initialization |
| `api/src/api/v2.js` | API endpoint definitions |
| `api/src/job.js` | Job execution management (READY → PRIMED → EXECUTED) |
| `api/src/runtime.js` | Language runtime management |
| `api/src/package.js` | Package installation and management |
| `api/src/config.js` | Configuration management via environment variables |

### API Endpoints

| Method | Path | Purpose |
|---------|------|------|
| GET | `/api/v2/runtimes` | List installed languages |
| POST | `/api/v2/execute` | Execute code |
| WebSocket | `/api/v2/connect` | Interactive execution |

## Configuration (Environment Variables)

Main environment variables (`PISTON_` prefix):

| Variable | Default | Description |
|-----|---------|------|
| `PISTON_LOG_LEVEL` | INFO | Log level |
| `PISTON_BIND_ADDRESS` | 0.0.0.0:2000 | API bind address |
| `PISTON_DISABLE_NETWORKING` | true | Disable networking |
| `PISTON_COMPILE_TIMEOUT` | 10000 | Compile timeout (ms) |
| `PISTON_RUN_TIMEOUT` | 3000 | Execution timeout (ms) |
| `PISTON_MAX_PROCESS_COUNT` | 64 | Maximum process count |
| `PISTON_OUTPUT_MAX_SIZE` | 1024 | Maximum output size |

See `docs/configuration.md` for details.

## Testing

Security tests are located in `/tests/`. Use the `test-runner` subagent (`.claude/agents/test-runner.md`) to run and verify results.

```bash
codize run --json tests/fork.py                # Fork bomb test
codize run --json tests/fallocate.py           # Disk fill attack test
codize run --json tests/network.py             # Network access test
codize run --json tests/runaway_output.py      # Infinite output test
codize run --json tests/file_persistance.py    # File persistence test (run twice)
codize run --json tests/mqueue_persistance.py  # Mqueue persistence test (run twice)
codize run --json tests/memory_exhaustion.py   # Memory exhaustion test
codize run --json tests/inode_exhaustion.py    # Inode exhaustion test
codize run --json tests/symlink_escape.py      # Symlink escape test
codize run --json tests/privilege_escalation.py # Privilege escalation test
codize run --json tests/device_access.py       # Device access test
codize run --json tests/stderr_flood.py        # Stderr flood test
codize run --json tests/cpu_exhaustion.py      # CPU exhaustion test
codize run --json tests/env_leakage.py         # Environment variable leakage test
codize run --json tests/rlimit_override.py     # Resource limit override test
codize run --json tests/signal_resistance.py   # Signal resistance test
codize run --json tests/readonly_write.py      # Read-only filesystem write test
codize run --json tests/proc_info_leak.py      # /proc information leakage test
```

Package tests are automatically executed via GitHub Actions (`package-pr.yaml`).

## Adding Language Packages

1. Create `packages/<lang>/<version>/` directory
2. Create required files:
   - `metadata.json` - Language name, version, aliases
   - `build.sh` - Build script
   - `run` - Execution script
3. Build with `./piston build-pkg <lang> <version>`
4. Add badge to README.md

## Code Style

Prettier configuration (`.prettierrc.yaml`):
- Use single quotes
- Tab width: 4
- Omit arrow function parentheses

### Commit Messages

- **Do not use Conventional Commits** (no need for prefixes like `fix:`, `feat:`)
- Write in normal format with concise description of changes

## GitHub Actions

### permissions Configuration

Workflows using ghcr.io or GitHub Releases require explicit permissions configuration:

```yaml
jobs:
    job_name:
        runs-on: ubuntu-latest
        permissions:
            contents: write    # When uploading to releases
            packages: write    # When pushing to ghcr.io
            packages: read     # When pulling from ghcr.io
```

### Docker Image Workflows

| Workflow | Purpose | Trigger Path |
|-------------|------|-------------|
| `api-push.yaml` | API image | `api/**` |
| `repo-push.yaml` | Repo Builder image | `repo/**` |
| `package-push.yaml` | Package build | `packages/**` |

## Prerequisites

- Docker & Docker Compose
- cgroup v2 enabled (cgroup v1 disabled)
- Node.js >= 15 (for CLI development)
