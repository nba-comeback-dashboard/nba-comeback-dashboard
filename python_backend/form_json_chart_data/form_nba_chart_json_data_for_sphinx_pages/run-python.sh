#!/bin/bash

for file in $(find . -name "*.py"); do
  echo "Running $file..."
  python-main "$file"
done
