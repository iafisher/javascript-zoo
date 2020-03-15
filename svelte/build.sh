#!/bin/bash

set -e

# Bundle the JS and CSS using Rollup.
rollup -c

# Copy the bundled assets into a directory that Django knows about.
cp public/build/bundle.css ../backend/ui/static/ui/svelte.css
cp public/build/bundle.css.map ../backend/ui/static/ui/svelte.css.map.map
cp public/build/bundle.js ../backend/ui/static/ui/svelte.js
cp public/build/bundle.js.map ../backend/ui/static/ui/svelte.js.map

# Fix the references to the source maps in the static file.
sed -i 's/bundle.js.map/svelte.js.map/g' ../backend/ui/static/ui/svelte.js
sed -i 's/bundle.css.map/svelte.css.map/g' ../backend/ui/static/ui/svelte.css
