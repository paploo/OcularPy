OcularPy
(c) 2021, Jeff Reinecke

Visualization of properties of telescopes and libraries of eyepieces

# Install Notes

The usualy route for me is:
```
pip install numpy scipy matplotlib ipython jupyter pandas sympy nose
```

## 3.9.7 Woes (on Apple Silicon)

With python 3.9.7 I'm having troubles compiling scipy:

```
ERROR: Failed building wheel for numpy
  Failed to build numpy
  ERROR: Could not build wheels for numpy which use PEP 517 and cannot be installed directly
```

My first step was to try upgrading pip:

```
pip install --upgrade pip
```

This got me the error:

```
    ERROR: Failed building wheel for numpy
  Failed to build numpy
  ERROR: Could not build wheels for numpy, which is required to install pyproject.toml-based projects
  ```

I then tried:

```
pip install --upgrade pip setuptools wheel
```

But this still failed with:

# 3.8.12 (on Apple Silicon)

This time I started with
```
pip install --upgrade pip setuptools wheel
```

But then installation of numpy was failing on each version of source it tried with a HUGE set of clang errors, ending in:
```
clang: error: the clang compiler does not support 'faltivec', please use -maltivec and include altivec.h explicitly
```
and a summary of
```
Command errored out with exit status 1: /Users/paploo/.pyenv/versions/3.8.12/envs/scipy-python-3.8.12/bin/python3.8 -u -c 'import io, os, sys, setuptools, tokenize; sys.argv[0] = '"'"'/private/var/folders/wt/vht2nqz51w572rgml9j3_4240000gn/T/pip-install-v5lxwytg/numpy_26f051c9078744258761311b5747a1c8/setup.py'"'"'; __file__='"'"'/private/var/folders/wt/vht2nqz51w572rgml9j3_4240000gn/T/pip-install-v5lxwytg/numpy_26f051c9078744258761311b5747a1c8/setup.py'"'"';f = getattr(tokenize, '"'"'open'"'"', open)(__file__) if os.path.exists(__file__) else io.StringIO('"'"'from setuptools import setup; setup()'"'"');code = f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' install --record /private/var/folders/wt/vht2nqz51w572rgml9j3_4240000gn/T/pip-record-b05r2q07/install-record.txt --single-version-externally-managed --prefix /private/var/folders/wt/vht2nqz51w572rgml9j3_4240000gn/T/pip-build-env-ot3degzm/overlay --compile --install-headers /private/var/folders/wt/vht2nqz51w572rgml9j3_4240000gn/T/pip-build-env-ot3degzm/overlay/include/site/python3.8/numpy Check the logs for full command output.
```

## What to do?

This link had s rather drawn-out possible solution:

https://stackoverflow.com/questions/65745683/how-to-install-scipy-on-apple-silicon-arm-m1

And this one has a possible solution, but in the end it sounds like M1 support
isn't there yet:

https://github.com/artisan-roaster-scope/artisan/issues/670