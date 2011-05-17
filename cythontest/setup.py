from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("cythonversion", ["cythonversion.pyx"]), Extension("foo", ["foo.pyx"])]

setup(
  name='Hello world app',
  cmdclass={'build_ext': build_ext},
  ext_modules=ext_modules
)
