#!/bin/sh
echo "If you don't want to install the requirements for RBSH, press Ctrl+C now, otherwise, press enter."
a=""
read a

pip3 install pyyaml
pip3 install prompt_toolkit
pip3 install pygments

echo "Done!"
