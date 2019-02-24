# Changelog
A human readable summary of important changes.

### 0.1.0 We Are Muffins, Yes - [Unreleased]
#### Added
- Created basic readme with basic documentation
- Setup basic project structure
- Added basic jinja2 templating
- Added [gino](https://github.com/fantix/gino) utility class
- Added gino models for activitypub, features, moderation, administration, and oauth
- Cleaned up and bug fixed jinja2 templating - [@TheHottestPotato](https://cybre.space/@TheHottestPotato)
- Added lamia version.py file with current lamia version
- Added config.py module for lamia.config file reading (wraps Starlette Config)
- Email utility for sending mail and tests - [@TheHottestPotato](https://cybre.space/@TheHottestPotato)
- Added httpsigs module for signing and verifying headers (including tests)
- Added schema, fields, tests, validation, and context for json-ld handling
- Added implementation of webfinger client
- Added utilities for get_request_base_url and get_site_stats (just a stub)
- Corrected original documentation - [@TheHottestPotato](https://cybre.space/@TheHottestPotato)
- Added configuration.md to documentation - [@TheHottestPotato](https://cybre.space/@TheHottestPotato)
- Added CONTRIBUTING.md to documentation - [@TheHottestPotato](https://cybre.space/@TheHottestPotato)
- Babel configuration and setup current code with translation - [@TheHottestPotato](https://cybre.space/@TheHottestPotato)
- Setup coveralls and travis ci for coverage in the main branch
- Setup general framework for graphql api implementation
- Created graphql query and mutation for user registration

## Please use the following format for entries

###  0.0.0 - YYYY-MM-DD
#### [Added/Changed/Deprecated/Removed/Fixed/Security]
* List
* of
* Changes

#### [Added/Changed/Deprecated/Removed/Fixed/Security]
* List
* of
* Changes