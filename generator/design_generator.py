import os
import re
import argparse
import math

from generate_other_blocks import *
from generate_adder_tree import *
from generate_max_tree import *
from generate_softmax import *

# ###############################################################
# Top-level design generator class. Calls methods from other generators.
# ###############################################################
class design_generator:
  def __init__(self):
    self.parse_args()
    self.print_it()

  def parse_args(self):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p",
                        "--parallelism",
                        action='store',
                        default=8,
                        type=int,
                        help='Value of parallelism knob - a power-of-2 - 1,2,4,8,...')
    parser.add_argument("-s",
                        "--storage",
                        action='store',
                        default='mem',
                        type=str,
                        help='Value of the storage knob - mem or reg')
    parser.add_argument("-r",
                        "--precision",
                        action='store',
                        default='float16',
                        type=str,
                        help='Value of the precision knob - float16 or fixed32')
    parser.add_argument("-a",
                        "--accuracy",
                        action='store',
                        default='lut',
                        type=str,
                        help='Value of the accuracy knob - lut or dw')
    parser.add_argument("-f",
                        "--template_file",
                        action='store',
                        default="../design_template.v",
                        help='Path+Name of the top level template file')
    parser.add_argument("-v",
                        "--num_inp_vals",
                        action='store',
                        default=8,
                        type=int,
                        help='Number of input values to be handled by the softmax block')
    parser.add_argument("-b",
                        "--num_blank_locations",
                        action='store',
                        default=2,
                        type=int,
                        help='Number of blank locations in the memory before actual data starts')
    args = parser.parse_args()
    self.parallelism = args.parallelism
    self.storage = args.storage
    self.precision = args.precision
    self.accuracy = args.accuracy
    self.template_file = args.template_file
    self.num_inp_vals = args.num_inp_vals
    self.num_blank_locations = args.num_blank_locations

  def print_it(self):
    generate_defines(self.parallelism, self.precision, self.num_inp_vals, self.num_blank_locations)
    generate_includes(self.accuracy, self.precision)
    generate_softmax(self.template_file, self.parallelism, self.accuracy, self.storage)
    generate_max_tree(self.parallelism, self.precision)
    generate_sub("mode2_sub", self.parallelism, self.precision)
    generate_exp("mode3_exp", self.parallelism, self.accuracy, self.precision)
    generate_addertree(self.parallelism, self.precision)
    generate_ln("mode5_ln", self.parallelism, self.accuracy, self.precision)
    generate_sub("mode6_sub", self.parallelism, self.precision)
    generate_exp("mode7_exp", self.parallelism, self.accuracy, self.precision)

# ###############################################################
# main()
# ###############################################################
if __name__ == "__main__":
  design_generator()
