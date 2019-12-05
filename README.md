## Language documentation corpus validation scripts

This repository contains a series of scripts that can be used to validate and investigate the structural coherence of a language documentation corpus that has been stored as ELAN files. This is work in progress, so there is the possibility that something doesn't work at all as intended.

The scripts have been built to work with the structure of ELAN tier template used in several research projects, including [IKDP](https://langdoc.github.io/IKDP/), in the continuation project of which, [IKDP-2](https://langdoc.github.io/IKDP-2/) this work has been carried out. It is not clear if the tests in their current form are really useful for other projects, but in our project they have been practical in checking the errors in connection to archiving process.

[This notebook](./elan_tests.ipynb) illustrates how the scripts can be used. Eventually some example should be taken from unit testing in software, which would make it easier to use continuous integration and other tools.
 
To our knowledge some other projects have also developed similar tools, and archives also have their own validation methods. Some similar resources are also in GitHub, i.e. [MattBrownUCL/test-eafs](https://github.com/MattBrownUCL/test-eafs). What possibly makes our approach to stand out is the attempt to connect in validation ELAN files and metadata content.

We are happy to receive feedback about these tests, and also encourage other projects to extend from our work.

In case you find the work useful or reuse it, it can be cited as:

> Niko Partanen. (2019, December 5). langdoc/elan-tests: Language documentation corpus validation scripts (Version v0.1). Zenodo. http://doi.org/10.5281/zenodo.3564012
