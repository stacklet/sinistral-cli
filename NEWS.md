## Next Release

### Features

### Changes

### Fixes

### Other

---

## v0.5.36

### Changes

- **Dependency Update**: Upgraded c7n to 0.9.50 and c7n-left to 0.3.36 ([#75](https://github.com/stacklet/sinistral-cli/pull/75))
- **Dependency Update**: Bumped boto3/botocore to 1.42.59 to stay in sync with c7n's pinned versions ([#75](https://github.com/stacklet/sinistral-cli/pull/75))

### Other

- **GitHub Actions**: Bumped GitHub Actions dependencies ([#76](https://github.com/stacklet/sinistral-cli/pull/76), [#77](https://github.com/stacklet/sinistral-cli/pull/77))

---

## v0.5.35

### Changes

- **Dependency Update**: Upgraded all dependencies to pull in CVE fixes ([#73](https://github.com/stacklet/sinistral-cli/pull/73))

### Other

- **Supply Chain Security**: Hardened the build and release pipeline to reduce supply-chain risk in published artifacts ([#73](https://github.com/stacklet/sinistral-cli/pull/73))

---

## v0.5.34

### Changes

- **Dependency Update**: Updated to c7n 0.9.48 ([#68](https://github.com/stacklet/sinistral-cli/pull/68))

### Fixes

- **JMESPath Error**: Fixed c7n-left usage to resolve JMESPath errors ([#69](https://github.com/stacklet/sinistral-cli/pull/69))

### Other

- **GitHub Actions**: Bumped GitHub Actions dependencies and migrated to SHA pinning over tags for improved security ([#65](https://github.com/stacklet/sinistral-cli/pull/65), [#66](https://github.com/stacklet/sinistral-cli/pull/66), [#67](https://github.com/stacklet/sinistral-cli/pull/67), [#71](https://github.com/stacklet/sinistral-cli/pull/71))

---

## v0.5.33

### Changes

- **Dependency Update**: Upgraded to c7n 0.9.47 ([#64](https://github.com/stacklet/sinistral-cli/pull/64))

### Other

- **Build System**: Migrated from poetry to uv for dependency management ([#62](https://github.com/stacklet/sinistral-cli/pull/62))
- **Requirements**: Added requirements.txt file for Dependabot tracking ([#63](https://github.com/stacklet/sinistral-cli/pull/63))

---

## v0.5.32

### Other

- Updated codecov-cli version ([#61](https://github.com/stacklet/sinistral-cli/pull/61))
- Cleaned up justfile, removing unused targets ([#60](https://github.com/stacklet/sinistral-cli/pull/60))

---

## v0.5.30

### Changes

- **Dependency Update**: Updated c7n to 0.9.44 ([#56](https://github.com/stacklet/sinistral-cli/pull/56))

### Other

- Updated tools and their versions ([#57](https://github.com/stacklet/sinistral-cli/pull/57))

---

## v0.5.0

### Changes

- **Dependency Update**: Updated c7n-left to 0.3.28 ([#52](https://github.com/stacklet/sinistral-cli/pull/52))

### Fixes

- **Debug Flag**: Added global debug flag to suppress traceback unless -d/--debug is specified ([#54](https://github.com/stacklet/sinistral-cli/pull/54))

### Other

- Cleaned up dependency version for c7n-left ([#53](https://github.com/stacklet/sinistral-cli/pull/53))

---

## v0.4.0

### Features

- **CI Environment Support**: Added support for grabbing CI information from the environment ([#49](https://github.com/stacklet/sinistral-cli/pull/49))

### Fixes

- **Metadata Handling**: Added error handling for lack of metadata ([#46](https://github.com/stacklet/sinistral-cli/pull/46))

### Other

- Updated c7n-left dependency versions ([#47](https://github.com/stacklet/sinistral-cli/pull/47))
- Moved global options to CLI only ([#45](https://github.com/stacklet/sinistral-cli/pull/45))

---

## v0.3.0

### Fixes

- **Dependency Pinning**: Explicit pin of upstream c7n-left version ([#44](https://github.com/stacklet/sinistral-cli/pull/44))

### Other

- Updated to latest sigstore action ([#48](https://github.com/stacklet/sinistral-cli/pull/48))

---

## v0.2.7

### Fixes

- **Project Name Parameter**: Fixed project name parameter for run command ([#38](https://github.com/stacklet/sinistral-cli/pull/38))

### Other

- Updated c7n-left and other dependencies ([#33](https://github.com/stacklet/sinistral-cli/pull/33))

---

## v0.2.6

### Features

- **Auto-Authentication**: Added auto-auth support with project or organization credentials ([#32](https://github.com/stacklet/sinistral-cli/pull/32))
- **Credential Management**: Added support for revoking project and organization credentials ([#30](https://github.com/stacklet/sinistral-cli/pull/30))
- **Default Policy Collections**: Added support for is_default flag on policy collections ([#34](https://github.com/stacklet/sinistral-cli/pull/34))
- **Critical Severity**: Added support for critical severity level ([#40](https://github.com/stacklet/sinistral-cli/pull/40))

### Fixes

- **Backend Output**: Fixed issue where sinistral backend output doesn't override run CLI output selections ([#37](https://github.com/stacklet/sinistral-cli/pull/37))
- **Case-Sensitive Severity**: Fixed case-sensitive severity handling ([#39](https://github.com/stacklet/sinistral-cli/pull/39))
- **Severity Regex**: Fixed policy severity regex ([#25](https://github.com/stacklet/sinistral-cli/pull/25))

### Other

- Added Python 3.11 support to CI ([#25](https://github.com/stacklet/sinistral-cli/pull/25))

---

## v0.2.4

### Features

- **Project & Organization Auth**: Added project and organization authentication flow ([#28](https://github.com/stacklet/sinistral-cli/pull/28))
- **Local Policy Execution**: Added support for local policy execution ([#7](https://github.com/stacklet/sinistral-cli/pull/7))
- **Run Command**: Added run command for policy execution ([#2](https://github.com/stacklet/sinistral-cli/pull/2))

### Changes

### Fixes

- **Scan Upload**: Fixed support for scan upload with array resource type policy ([#27](https://github.com/stacklet/sinistral-cli/pull/27))
- **Policy Severity**: Allowed lowercase policy severity ([#20](https://github.com/stacklet/sinistral-cli/pull/20))

### Other

- Improved CLI command interface ([#9](https://github.com/stacklet/sinistral-cli/pull/9))
- Updated c7n-left dependencies ([#21](https://github.com/stacklet/sinistral-cli/pull/21))
- Added client generator from OpenAPI spec ([#3](https://github.com/stacklet/sinistral-cli/pull/3))

---

## Initial Release

### Features

- **SSO Login**: Added SSO login support ([#1](https://github.com/stacklet/sinistral-cli/pull/1))
- **Basic Commands**: Initial CLI commands for Sinistral platform interaction

### Other

- Initial repository setup

---
