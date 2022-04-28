SemGWT
======

Intro
-----

This is an attempt to approach the problem of extracting GWT RPC method information from generated JavaScript files with [Semgrep](https://semgrep.dev), without relying on regular expressions to parse complex JavaScript.

Design
------

At this point we try to provide standalone tools to implement different phases of the extraction process:

- The preprocessor extracts pure JavaScript code from static cache files provided by GWT applications
- Semgrep rules are used to extract RPC interface information from the preprocessed JavaScript
- Post-processing is needed to transform the extracted data to HTTP requests (or other formats useful for the user)

The simple structure of Semgrep rules should allow easy addition of support for different GWT versions and maintenance.

### Samples wanted!

One of the hurdles of GWT is the wide variety of cache file formats different versions produce. If you have any samples to share please open a PR or reach out on usual channels!

Performance
-----------

One weakness of Semgrep is that it can easily consume (almost) boundless memory. Because of this, rules must be created and tested carefully, and the process needs special parameters for larger files. 

In particular, defining code block patterns with ellipses inside (e.g. `function $FOO(){var $X; ...}`) can have a detrimental effect on performance, so you should try to avoid this and focus on sequences of statements.

Semgrep has both size and time limits by default. To analyze a 10MB JavaScript file, I had to disable timeouts, and set the size limit above the size of the file:

```
--timeout 0 \
--max-target-bytes 20 MB
```

Additionally, to prevent OOM Killer intervention (or system freeze...) it is recommended to set the memory limit. In the above case the `semgrep` process can easily consume 10 gigabytes of memory:

```
--max-memory 10240
```

File sizes are limited by default for a reason: memory requirement of parsing a single large file or orders of magnitude bigger than parsing the same code split into multiple files. It is highly recommended to split the input multiple files during preprocessing. The theoretical cost of this is losing inter-file references, but this shouldn't be a problem in the case of GWT.

Example
-------

### Split files

Run the preprocessor:

```
python3 preprocess.py path/to/HEX.cache.js
```

This will create a directory named `HEX` in the current directory with split JavaScript files in it.

Run the Semgrep rules on the files:

```
semgrep -c SemGWT.yaml --json split_files_dir/ > semgwt.out.json
```

Run post-processing on the generated JSON:

```
TODO
```

### Large files

```
semgrep -c SemGWT.yaml \
--max-target-bytes 20MB \
--timeout 0 \
--max-memory 10240 \
samples/clean
```

This can take more than 20mins to complete against the said 10MB test case (can't be included in the repo unfortunately for license reasons).

TODO
----

* Preprocessing of cache files to get raw JavaScript (in progress)
* Semgrep output processing to generate proper method signatures or even sample HTTP requests
* Multi-version support (samples needed!)
