INTRODUCTION
============

A collection of text processing script. Following function will be implemented.

* Format Converter  : convert corpus between different format
* Sampler           : sample 
* Filter            : filter corpus by certain rule
* Spliter           : split corpus into train, devolop and test set
* Evaluator         : evaluate p, r and f score between gold and predicate result

EXAMPLES
========
__Format Converter__

Suppose you are in root dir of the project, you can run format converter in the
following command:

`python ./bin/format_conv.py --from=postag --to=segment ./data/postag_sample.dat`
