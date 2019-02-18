# Configuration settings

This is a complete list of all settings that are used when defined in `lamia.config`.

## Required settings

These settings are required to configure core features, none should be left unset when running in production.

### `DB_DSN`

A fully qualified URL of the following shape:
`postgresql://username:password@hostname/database[:port]`
There is a default value, but it should not be relied on:
`postgresql://postgres@localhost/postgres:5432`

This url will be used to access the postgres server.

This option is an alternative to the following collection of arguments and their defaults, and overrides all of them.
- `DB_USER`: `postgres`
- `DB_PASSWORD`: Default is empty
- `DB_HOST`: `localhost`
- `DB_PORT`: `5432`
- `DB_DATABASE`: `postgres`

### `MAIL_DSN`

A fully qualified URL of the following shape:
`smtp://username[:password]@hostname[:port]`
Username must be a valid account to send emails from on the hostname smtp server.
Emails will be sent using this user to all users, for features such as email confirmations.

### `ADMIN_EMAIL`

An email address to specify as the administrator email.
At current time only one admin can be specified.

In the future this setting may also be used to specify the administrator account within the site interface.

### `SECRET_KEY`

This is the secret key for your server.  Used for a lot of important security features of lamia. It must be set and kept secret.

## Optional settings

These options do not have to be set, but may be useful to configure.

### `SITE_NAME`

A string containing the name for your site. It will be displayed throughout the site.

### `MAIL_WORKER_COUNT`

Number of mail workers to have running at once.
Normally this should not need changing.
Defaults to 10.

### `MAIL_JINJA_DIR`

A directory to find jinja template overrides, if you want the default templates to be changed.
If not specified, only the default templates stored at the module root will be used.

### `DB_SSL`

If set to true, enables ssl for the communication with the database. Defaults to false.

### `POOL_MAX_SIZE` and `POOL_MIN_SIZE`

These two settings configure the minimum and maximum number of database connections that can be alive in the database pool.

## Development settings

### `DEBUG`

Sets the server to run in development mode.

### `DEV_EMAIL`

A development setting.
Emails are not sent when the server is run in development mode unless this is enabled.

