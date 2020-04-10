#!/bin/bash

set -e

# Bundle the JS and CSS using Rollup.
rollup -c

# Copy the bundled assets into a directory that Django knows about.
cp public/build/bundle.css ../backend/public/css/svelte.css
cp public/build/bundle.css.map ../backend/public/css/svelte.css.map
cp public/build/bundle.js ../backend/public/js/svelte.js
cp public/build/bundle.js.map ../backend/public/js/svelte.js.map

# Fix the references to the source maps in the static file.
sed -i 's/bundle.js.map/svelte.js.map/g' ../backend/public/js/svelte.js
sed -i 's/bundle.css.map/svelte.css.map/g' ../backend/public/css/svelte.css
