************
INTRODUCTION
************

A collection of text processing script. Following function will be implemented.

* Format Converter  : convert corpus between different format [fin]
* Sampler           : sample [fin]
* Filter            : filter corpus by certain rule
* Spliter           : split corpus into train, devolop and test set
* Evaluator         : evaluate p, r and f score between gold and predicate result [fin]

*****
USAGE
*****
Suppose you are in root dir of the project, you can run format converter in the
following command:

__Format Converter__

> python ./bin/format_conv.py --from=postag --to=segment ./data/postag_sample.dat

__Sampler__

> python ./bin/sample.py --format=segment --mode=number --number=2 ./data/segment_sample.dat

__Evaluator__

> python ./bin/eval.py --format=segment --mode=segment --eval=./data/segment_output_sample.dat --gold=./data/segment_sample.dat -a


