# A script to automatically create and test source and wheel
# distributions of Beautiful Soup.

# Recommend you run these steps one at a time rather than just running
# the script.

# If you screwed up on the test server and have to create a "a" or "b"
# release the second time, add the '--pre' argument to pip install to
# find the 'prerelease'.

# Make sure tests pass
./test-all-versions

# Make sure nothing broke on 2.6
source ../virtualenv-2.6/bin/activate
nosetests
deactivate

rm -rf dist

# Create the 2.x source distro and wheel
python setup.py sdist bdist_wheel

# Create the 3.x wheel
source ../virtualenv-3/bin/activate
python setup.py bdist_wheel
deactivate

# Upload to pypi test
python setup.py register -r test
python setup.py sdist bdist_wheel upload -r test

source ../virtualenv-3/bin/activate
python setup.py bdist_wheel upload -r test
deactivate

# Try 2.x install from pypi test
rm -rf ../py2-install-test-virtualenv
virtualenv -p /usr/bin/python2.7 ../py2-install-test-virtualenv
source ../py2-install-test-virtualenv/bin/activate
pip install -i https://testpypi.python.org/pypi beautifulsoup4
echo "EXPECT HTML ON LINE BELOW"
(cd .. && python -c "from bs4 import _s; print(_s('<a>foo', 'html.parser'))")
# That should print '<a>foo</a>'
deactivate
rm -rf ../py2-install-test-virtualenv

# Try 3.x install from pypi test
rm -rf ../py3-install-test-virtualenv
virtualenv -p /usr/bin/python3 ../py3-install-test-virtualenv
source ../py3-install-test-virtualenv/bin/activate
pip install -i https://testpypi.python.org/pypi beautifulsoup4
echo "EXPECT HTML ON LINE BELOW"
(cd .. && python -c "from bs4 import _s; print(_s('<a>foo', 'html.parser'))")
# That should print '<a>foo</a>'
deactivate
rm -rf ../py3-install-test-virtualenv



# Make sure setup.py works on 2.x
rm -rf ../py2-install-test-virtualenv
virtualenv -p /usr/bin/python2.7 ../py2-install-test-virtualenv
source ../py2-install-test-virtualenv/bin/activate
python setup.py install
echo "EXPECT HTML ON LINE BELOW"
(cd .. && python -c "from bs4 import _s; print(_s('<a>foo', 'html.parser'))")
# That should print '<a>foo</a>'
deactivate
rm -rf ../py2-install-test-virtualenv
echo

# Make sure setup.py works on 3.x
rm -rf ../py3-install-test-virtualenv
virtualenv -p /usr/bin/python3 ../py3-install-test-virtualenv
source ../py3-install-test-virtualenv/bin/activate
python setup.py install
echo "EXPECT HTML ON LINE BELOW"
(cd .. && python -c "from bs4 import _s; print(_s('<a>foo', 'html.parser'))")
# That should print '<a>foo</a>'
deactivate
rm -rf ../py3-install-test-virtualenv
echo

# Make sure the 2.x wheel installs properly
rm -rf ../py2-install-test-virtualenv
virtualenv -p /usr/bin/python2.7 ../py2-install-test-virtualenv
source ../py2-install-test-virtualenv/bin/activate
pip install dist/beautifulsoup4-4.*-py2-none-any.whl -e .[html5lib]
echo "EXPECT HTML ON LINE BELOW"
(cd .. && python -c "from bs4 import _s; print(_s('<a>foo', 'html5lib'))")
# That should print '<html><head></head><body><a>foo</a></body></html>'
deactivate
rm -rf ../py2-install-test-virtualenv

echo
# Make sure the 3.x wheel installs properly
rm -rf ../py3-install-test-virtualenv
virtualenv -p /usr/bin/python3 ../py3-install-test-virtualenv
source ../py3-install-test-virtualenv/bin/activate
pip install dist/beautifulsoup4-4.*-py3-none-any.whl -e .[html5lib]
echo "EXPECT HTML ON LINE BELOW"
(cd .. && python -c "from bs4 import _s; print(_s('<a>foo', 'html5lib'))")
# That should print '<html><head></head><body><a>foo</a></body></html>'
deactivate
rm -rf ../py3-install-test-virtualenv

################

To test, after release:

rm -rf ../py2-install-test-virtualenv
virtualenv -p /usr/bin/python2.7 ../py2-install-test-virtualenv
source ../py2-install-test-virtualenv/bin/activate
pip install beautifulsoup4
echo "EXPECT HTML ON LINE BELOW"
(cd .. && python -c "from bs4 import _s; print(_s('<a>foo', 'html.parser'))")
# That should print '<a>foo</a>'
deactivate
rm -rf ../py2-install-test-virtualenv


rm -rf ../py3-install-test-virtualenv
virtualenv -p /usr/bin/python3 ../py3-install-test-virtualenv
source ../py3-install-test-virtualenv/bin/activate
pip install beautifulsoup4
echo "EXPECT HTML ON LINE BELOW"
(cd .. && python -c "from bs4 import _s; print(_s('<a>foo', 'html.parser'))")
# That should print '<a>foo</a>'
deactivate
rm -rf ../py3-install-test-virtualenv
