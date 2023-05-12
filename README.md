# `resotoappbundler`
Resoto Infrastructure Apps Bundler


## Table of contents

* [Overview](#overview)
* [Usage](#usage)
* [Contact](#contact)
* [License](#license)


## Overview
`resotoappbundler` Bundles Resoto Infrastructure Apps.
`resotoapprunner` Dry runs Resoto Infrastructure Apps.


## Usage of `resotoappbundler`

```bash
resotoappbundler --path resoto-apps/ --discover > index.json
```

This command discovers all apps in the current directory and writes the index to `index.json`. This file can then be uploaded to a http server like a CDN and used as an app index in Resoto.

```bash
usage: resotoappbundler [-h] [--machine-help] [--verbose | --trace | --quiet] --path APP_PATH [--discover]

Resoto Infrastructure Apps Bundler

options:
  -h, --help            show this help message and exit
  --machine-help        print machine readable help
  --verbose, -v         Verbose logging
  --trace               Trage logging
  --quiet               Only log errors
  --path APP_PATH, -p APP_PATH
                        Path to app bundle(s)
  --discover            Find all apps in the path
```

## Usage of `resotoapprunner`

```bash
resotoapprunner --path resoto-apps/tagvalidator/ --psk changeme --resotocore-uri https://localhost:8900
```

Note: Resoto Core is only required for apps that make use of the `search()` function.

```bash
usage: resotoapprunner [-h] [--machine-help] [--verbose | --trace | --quiet] --path APP_PATH [--ca-cert CA_CERT] [--cert CERT] [--cert-key CERT_KEY] [--cert-key-pass CERT_KEY_PASS]
                       [--no-verify-certs] [--resotocore-uri RESOTOCORE_URI] [--psk PSK] [--config CONFIG_PATH] [--subscriber-id SUBSCRIBER_ID]

Resoto Infrastructure Apps Runner

options:
  -h, --help            show this help message and exit
  --machine-help        print machine readable help
  --verbose, -v         Verbose logging
  --trace               Trage logging
  --quiet               Only log errors
  --path APP_PATH, -p APP_PATH
                        Path to app bundle(s)
  --ca-cert CA_CERT     Path to custom CA certificate file
  --cert CERT           Path to custom certificate file
  --cert-key CERT_KEY   Path to custom certificate key file
  --cert-key-pass CERT_KEY_PASS
                        Passphrase for certificate key file
  --no-verify-certs     Turn off certificate verification
  --resotocore-uri RESOTOCORE_URI
                        resotocore URI (default: https://localhost:8900)
  --psk PSK             Pre-shared key
  --config CONFIG_PATH  Path to app config
  --subscriber-id SUBSCRIBER_ID
                        Unique subscriber ID (default: resotoappbundler)```
```

## Contact
If you have any questions feel free to [join our Discord](https://discord.gg/someengineering) or [open a GitHub issue](https://github.com/someengineering/resoto/issues/new).


## License
```
Copyright 2022 Some Engineering Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
