# Interactive Electrochemistry - Equivalent Circuit 'R0-p(R1,C1)'

An easily executable `Panel` and `Pyscript` based interactive simulation of Equivalent Circuit 'R0-p(R1,C1)' targeted towards 'Electrochemistry' learners. The simulation itself is a `.html` file, and can be opened in any browser without need for installation of new python environments or special python package installation on the device.

### How to use?

- For offline users, download the `src` folder, the files within it and `pyscript-local.html` file. Open `pyscript-local.html` and enjoy learning!

- For online users, download the `pyscript-remote.html` file. Open `pyscript-local.html` and enjoy learning!


### How was the `.html` file created?

`script.py` is first made with the help of `jupyter`. Then, the `script.py` is then transformed to `.html` file using `panel convert script.py --to pyscript --out`. This creates a `script.html` file in the current folder (here known as `pyscript-remote.html`.

However, this `pyscript-remote.html` file uses remotely stored `.js` files for the `.html` file execution. This is corrected for by downloading and storing the `.js` files in a folder called `src`, and the raw `pyscript-remote.html` is edited manually in a script editor to (`pyscript-local.html`) use locally stored `.js` files from `src` folder.


### References
<a id="1">[1]</a>
T.F. Fuller, J.N. Harb, Electrochemical Engineering, John Wiley & Sons, Hoboken, 2018.

<a id="1">[2]</a>
Electrochemical Impedance Spectroscopy and its Applications, A. Lasia, Springer 2014

<a id="1">[3]</a>
Electrochemical Impedance Spectroscopy, M.E. Orazem, B. Tribollet, John Wiley & Sons, Inc., 2008

<a id="1">[4]</a>
[impedance.py](<https://impedancepy.readthedocs.io/en/latest/getting-started.html> "Impedance.Py") (a Python package for simulation and fitting of impedance data)
