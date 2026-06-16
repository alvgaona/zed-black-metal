default:
    just --list

# regenerate themes/black-metal.json from palettes/ + src/base.json
build:
    python3 scripts/generate.py

# fail if the committed theme is stale or invalid JSON
check: build
    git diff --exit-code themes/black-metal.json
    python3 -c "import json; json.load(open('themes/black-metal.json')); print('themes/black-metal.json is valid')"

# copy the generated theme into your local Zed config
install: build
    cp themes/black-metal.json ~/.config/zed/themes/black-metal.json

# tag a release (vX.Y.Z) and push it — triggers the publish workflow
release tag:
    git tag -a "{{ tag }}" -m "{{ tag }}"
    git push origin "{{ tag }}"

# remove generated output
clean:
    rm -f themes/black-metal.json
