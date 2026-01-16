set -u
outfile=$1
hatch env show --json | jq 'to_entries | map(select(.key | startswith("test")))' | jq '{include: map({"hatch-env-name": .key, "python-version": .value.python})}' > $outfile

git diff --exit-code $outfile
if [ $? -ne 0 ]; then
    echo "Hatch environment matrix has changed. Please commit ${outfile}."
    exit 1
fi
