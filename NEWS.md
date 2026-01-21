## Next Release

### Features

### Changes

- **Dependency Update**: Updated to c7n 0.9.48

### Fixes

- **JMESPath Error**: Fixed c7n_left usage to resolve JMESPath errors

### Other

- **GitHub Actions**: Bumped GitHub Actions dependencies and migrated to SHA pinning over tags for improved security
- **Build System**: Migrated from poetry to uv for dependency management
- **Requirements**: Added requirements.txt file for Dependabot tracking

---

## v0.5.32

### Features

### Changes

### Fixes

### Other

- Updated codecov-cli version
- Cleaned up justfile, removing unused targets

---

## v0.5.30

### Features

### Changes

- **Dependency Update**: Updated c7n to 0.9.44

### Fixes

### Other

- Updated tools and their versions

---

## v0.5.0

### Features

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

### Changes

### Fixes

- **Metadata Handling**: Added error handling for lack of metadata

### Other

- Updated c7n-left dependency versions
- Moved global options to CLI only

---

## v0.3.0

### Features

### Changes

### Fixes

- **Dependency Pinning**: Explicit pin of upstream c7n-left version

### Other

- Updated to latest sigstore action

---

## v0.2.7

### Features

### Changes

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

### Changes

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

### Changes

### Fixes

### Other

- Initial repository setup

---
