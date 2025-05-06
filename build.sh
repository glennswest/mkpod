./update_version.sh .version_mkpod
VERSION=`cat .version_mkpod`
git add .version_mkpod
sed -i "s/version = \".*\"/version = \"$VERSION\"/" pyproject.toml
python -m build
twine upload --config-file=.pypirc dist/*
