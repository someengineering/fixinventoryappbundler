# `fixinventoryappbundler` / `fixinventoryapprunner`
Fix Inventory Infrastructure Apps Bundler and Runner


## Table of contents

* [Overview](#overview)
* [Usage](#usage)
* [Contact](#contact)
* [License](#license)


## Overview
`fixinventoryappbundler` Bundles Fix Inventory Infrastructure Apps.

`fixinventoryapprunner` Dry runs Fix Inventory Infrastructure Apps.


Check [the Fix Inventory Infrastructure Apps repo](https://github.com/someengineering/fixinventory-apps) for details.

## Usage of `fixinventoryappbundler`

```bash
fixinventoryappbundler --path fixinventory-apps/ --discover > index.json
```

This command discovers all apps in the current directory and writes the index to `index.json`. This file can then be uploaded to a http server like a CDN and used as an app index in Fix Inventory.

```bash
usage: fixinventoryappbundler [-h] [--machine-help] [--verbose | --trace | --quiet] --path APP_PATH [--discover]

Fix Inventory Infrastructure Apps Bundler

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

## Usage of `fixinventoryapprunner`

```bash
fixinventoryapprunner --path fixinventory-apps/tagvalidator/ --psk changeme --fixcore-uri https://localhost:8900
```

Note: Fix Inventory Core is only required for apps that make use of the `search()` function.

```bash
usage: fixinventoryapprunner [-h] [--machine-help] [--verbose | --trace | --quiet] --path APP_PATH [--ca-cert CA_CERT] [--cert CERT] [--cert-key CERT_KEY] [--cert-key-pass CERT_KEY_PASS]
                       [--no-verify-certs] [--fixcore-uri FIXCORE_URI] [--psk PSK] [--config CONFIG_PATH] [--subscriber-id SUBSCRIBER_ID]

Fix Inventory Infrastructure Apps Runner

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
  --fixcore-uri FIXCORE_URI
                        fixcore URI (default: https://localhost:8900)
  --psk PSK             Pre-shared key
  --config CONFIG_PATH  Path to app config
  --subscriber-id SUBSCRIBER_ID
                        Unique subscriber ID (default: fixinventoryappbundler)
```

## Contact
If you have any questions feel free to [join our Discord](https://discord.gg/someengineering) or [open a GitHub issue](https://github.com/someengineering/fixinventory/issues/new).


## License
```
Copyright 2024 Some Engineering Inc.

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
