## Overview

### Foundations, Requirements and Values

Universal Cake Foundations, Metrics and Audits go here

The content in the pipeline generally goes from left to right in this flow:

```bash
SAT -> Publishing Vector -> Publishing Target
```

## Source Archive Tools Requirements

### OS Agnostic Tools (OSAT)

In order to ensure that SAT and other utilities function on "all" major operating systems, Python was selected as the primary language as it has excellent cross platform support.

The tools required to run SAT are installed in cross platform ways in order to ensure that SAT runs on most major operating systems. Currently these are referred to as **OS Agnostic Tools (OSAT)** but the naming will shift in order to better reflect what these actually do.

In addition to installing tools they also allow you to manage the installed tools, install new versions or tools, remove tools or switch between tool versions.

In order to install SAT and other utilities on "all" operating systems, Python was selected as it has excellent cross platform support. Ironically, this does not include Python installers themselves so I created a sort of unified approach that ensures for a user space Python on Linux, MacOS and Windows that allows users to install a standard, versioned, sand-boxed Python in the user space without requiring administrative permissions.

#### Examples of OSAT Tool Mangers

##### Publishing Vector Support

Static Site Generator Vector Hugo

* [hugo-tool](https://github.com/steelcj/hugo-tool)

##### Other OSAT tool managers

* [osat-fluent-python-tool](https://github.com/steelcj/osat-fluent-python-tool/blob/main/docs/en/README.md) enables OSAT tool installs like:
  * [osat-fluent-restic-tool](https://github.com/steelcj/osat-fluent-restic-tool) - backup tool

## Source Archive Tools (SAT)

#### Resources

* [Source Archive Tools (SAT)](https://github.com/steelcj/sat)

The source archive tools (SAT) is made up of on or more managed collections of content language archives.

In this very basic example the managed collection is called vishpala.com and English and French content is stored in one or more directories and subdirectories in each language's archive. 

```yaml
collections/vishpala.com/
  en-ca/<content>
  fr-ca/<content>
```

