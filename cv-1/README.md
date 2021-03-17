## Install opencv with nonfree-contrib
```
pip install opencv-python==3.4.2.16
pip install opencv-contrib-python==3.4.2.16
```

## Install opencv 4.5.1
```
pip install opencv-python==4.5.1.48
pip install opencv-contrib-python==4.5.1.48
```

## Rebuild opencv contrib with nonfree contribution
MAKEFLAGS=-j16 CMAKE_ARGS="-DOPENCV_ENABLE_NONFREE=ON" \
pip install --no-binary=opencv-contrib-python opencv-contrib-python

##

https://stackoverflow.com/questions/26228136/pip-build-option-to-use-multicore
https://github.com/opencv/opencv-python/issues/126


