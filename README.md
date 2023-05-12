# `resotoappbundler`
Resoto Infrastructure Apps Bundler


## Table of contents

* [Overview](#overview)
* [Usage](#usage)
* [Contact](#contact)
* [License](#license)


## Overview
`resotoappbundler` bundles Resoto Infrastructure Apps.


## Usage of `resotoappbundler`

```bash
resotoappbundler --discover --path . > index.json
```

This command discovers all apps in the current directory and writes the index to `index.json`. This file can then be uploaded to a http server like a CDN and used as an app index in Resoto.


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
