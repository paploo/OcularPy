OcularPy
(c) 2021, Jeff Reinecke

Visualization of properties of telescopes and libraries of eyepieces

# Install Notes

Make sure pyenv is installed via brew.

Using pyenv, ensure a virtual environment, e.g.
```
pyenv virtualenv 3.9.10 scipy-python-3.9.10
```

Verify it is properly selected with
```
pyenv version
```

Upgrade pip
```
pyenv exec pip intall --upgrade pip
```

Install the needed dependencies
```
pyenv exec pip install numpy scipy matplotlib ipython jupyter pandas sympy nose
```
