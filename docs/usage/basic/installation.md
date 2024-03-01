---
hide:
    - toc
---

# Installation

!!! info
    Pulsefire requires Python **3.12** or higher.

=== "with pip (recommended)"

    Pulsefire is published on PyPI and can be installed with `pip`, ideally by using a virtual environment. Open up a terminal and install Pulsefire with:

    ```sh
    pip install pulsefire -U
    ```

=== "with git (latest)"

    Pulsefire can be directly used from GitHub by cloning the repository into a subfolder of your project root which might be useful if you want to use the very latest version:

    ```sh
    git clone https://github.com/iann838/pulsefire.git
    ```

    Next, install its dependencies with:

    ```sh
    pip install -e pulsefire
    ```

## Typing packages

!!! info
    These packages are not required if you have pulsefire installed. They are available for developers who want to use pulsefire for typing purposes only. 

=== "with pip (python)"

    The python types package is published on PyPI and can be installed with `pip`, ideally by using a virtual environment. Open up a terminal and install Pulsefire with:

    ```sh
    pip install pulsefire-types -U
    ```

    Available subset modules:

    ```py
    from pulsefire.schemas import ...
    ```

=== "with yarn (typescript)"

    The typescript package is a transpiled version of `pulsefire-types`, it is published on NPM and can be installed with `yarn`. Open up a terminal and install Pulsefire with:

    ```sh
    yarn add pulsefire-types -D
    ```

    Available subset modules:

    ```ts
    import type { ... } from "pulsefire-types/schemas"
    ```