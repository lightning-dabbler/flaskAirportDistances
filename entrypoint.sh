#!/bin/bash

if [ -d "/build" ]
then
    cp /build/Pipfile.lock /build/Pipfile /us-airport-distance-calc \
    && rm -rf /build \
    && python app.py
else
    python app.py
fi
