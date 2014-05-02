#!/usr/bin/python
from model import Model
from layers.layer import MockSource, FCL, BiasL, TanhL, SigmL, ChrSource
from layers.cost import SoftmaxC
from layers.bundle import FCB, SoftmaxBC
import sys

# XXX: if things won't work better then check if backroll is not scrued up.

def penn_data():
   source = ChrSource
   params = {'name': 'pennchr', 'unroll': 20, 'backroll': 5}
   return source, params

def mock_data():
  source = MockSource
  classes = 4
  params = {'freq': 2, 'classes': classes, 'batch_size': 10, 'unroll': 5, 'backroll': 4}
  return source, params

def mock(source):
  model = Model(name="mock", n_epochs=1)
  model.set_source(source[0], source[1]) \
    .attach(FCL, {'out_len': 50, 'hiddens' : ['qqq']}) \
    .attach(BiasL, {}) \
    .attach(SigmL, {}) \
    .add_hidden('qqq') \
    .attach(FCL, {'out_len': 256}) \
    .attach(BiasL, {}) \
    .attach(SoftmaxC, {})
  return model

def pennchr(source, hid):
  model = Model(name="pennchr%d" % hid, n_epochs=10000, momentum=0.5, lr=1)
  model.set_source(source[0], source[1]) \
    .attach(FCL, {'out_len': hid, 'hiddens' : ['qqq']}) \
    .attach(BiasL, {}) \
    .attach(SigmL, {}) \
    .add_hidden('qqq') \
    .attach(FCL, {'out_len': 256}) \
    .attach(BiasL, {}) \
    .attach(SoftmaxC, {})
  return model

def pennchr1000(source):
  return pennchr(source, 1000)

def pennchr600(source):
  return pennchr(source, 600)

def pennchr800(source):
  return pennchr(source, 800)

def main():
  options = {'1': ('mock_data', 'mock'), '2':('penn_data', 'pennchr600'), '3':('penn_data', 'pennchr800')}
  option = '3'
  if len(sys.argv) > 1:
    option = sys.argv[1]
  source_name, fun = options[option]
  source = eval(source_name + '()')
  model = eval(fun + '(source)')
  model.name = fun
  model.init()
  model.train()
  model.test()

if __name__ == '__main__':
  main()
