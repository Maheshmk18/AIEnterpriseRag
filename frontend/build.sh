#!/bin/sh
# Vercel build script to work around permission issues

echo "Setting execute permissions for vite..."
chmod +x node_modules/.bin/vite

echo "Running vite build..."
node node_modules/vite/bin/vite.js build
