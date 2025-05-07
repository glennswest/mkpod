./update_version.sh .version_mkpod
VERSION=`cat .version_mkpod`
git add .version_mkpod
python update_toml_version.py
rm dist/*
python -m build
twine upload --config-file=.pypirc dist/*
