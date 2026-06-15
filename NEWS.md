## Next Release

### Features

### Changes

### Fixes

### Other

---

## v0.5.36

### Changes

- **Dependency Update**: Upgraded c7n to 0.9.50 and c7n-left to 0.3.36
- **Dependency Update**: Bumped boto3/botocore to 1.42.59 to stay in sync with c7n's pinned versions

---

## v0.5.35

### Changes

- **Dependency Update**: Upgraded all dependencies to pull in CVE fixes

### Other

- **Supply Chain Security**: Hardened the build and release pipeline to reduce supply-chain risk in published artifacts

---

## v0.5.34

### Changes

- **Dependency Update**: Updated to c7n 0.9.48

### Fixes

- **JMESPath Error**: Fixed c7n-left usage to resolve JMESPath errors

### Other

- **GitHub Actions**: Bumped GitHub Actions dependencies and migrated to SHA pinning over tags for improved security
- **Build System**: Migrated from poetry to uv for dependency management
- **Requirements**: Added requirements.txt file for Dependabot tracking

---

## v0.5.33

### Changes

- **Dependency Update**: Updated to c7n 0.9.48

### Other

- Updated codecov-cli version
- Cleaned up justfile, removing unused targets

---

## v0.5.32

### Other

- Updated codecov-cli version
- Cleaned up justfile, removing unused targets

---

## v0.5.30

### Changes

- **Dependency Update**: Updated c7n to 0.9.44

### Other

- Updated tools and their versions

---

## v0.5.0

### Changes

- **Dependency Update**: Updated c7n-left to 0.3.28

### Fixes

- **Debug Flag**: Added global debug flag to suppress traceback unless -d/--debug is specified

### Other

- Cleaned up dependency version for c7n-left

---

## v0.4.0

### Features

- **CI Environment Support**: Added support for grabbing CI information from the environment

### Fixes

- **Metadata Handling**: Added error handling for lack of metadata

### Other

- Updated c7n-left dependency versions
- Moved global options to CLI only

---

## v0.3.0

### Fixes

- **Dependency Pinning**: Explicit pin of upstream c7n-left version

### Other

- Updated to latest sigstore action

---

## v0.2.7

### Fixes

- **Project Name Parameter**: Fixed project name parameter for run command

### Other

- Updated c7n-left and other dependencies

---

## v0.2.6

### Features

- **Auto-Authentication**: Added auto-auth support with project or organization credentials
- **Credential Management**: Added support for revoking project and organization credentials
- **Default Policy Collections**: Added support for is_default flag on policy collections
- **Critical Severity**: Added support for critical severity level

### Fixes

- **Backend Output**: Fixed issue where sinistral backend output doesn't override run CLI output selections
- **Case-Sensitive Severity**: Fixed case-sensitive severity handling
- **Severity Regex**: Fixed policy severity regex

### Other

- Added Python 3.11 support to CI

---

## v0.2.4

### Features

- **Project & Organization Auth**: Added project and organization authentication flow
- **Local Policy Execution**: Added support for local policy execution
- **Run Command**: Added run command for policy execution

### Changes

### Fixes

- **Scan Upload**: Fixed support for scan upload with array resource type policy
- **Policy Severity**: Allowed lowercase policy severity

### Other

- Improved CLI command interface
- Updated c7n-left dependencies
- Added client generator from OpenAPI spec

---

## Initial Release

### Features

- **SSO Login**: Added SSO login support
- **Basic Commands**: Initial CLI commands for Sinistral platform interaction

### Other

- Initial repository setup

---
