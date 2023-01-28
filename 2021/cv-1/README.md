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
MAKEFLAGS=-j16 CMAKE_ARGS="-DOPENCV_ENABLE_NONFREE=ON -DBUILD_opencv_gapi=OFF" \
pip install --no-binary=opencv-contrib-python opencv-contrib-python


MAKEFLAGS=-j4 \
CMAKE_ARGS="-DOPENCV_ENABLE_NONFREE=ON" \
pip install --no-binary=opencv-contrib-python opencv-contrib-python

## Build opencv on Yard1
cmake -DENABLE_OPENCV_NONFREE=ON \
-DBUILD_NEW_PYTHON_SUPPORT=ON \
-DBUILD_opencv_python3=ON \
-DHAVE_opencv_python3=ON \
-DPYTHON3_INCLUDE_DIR=$HOME/.is/conda/envs/sony/include \
-DPYTHON3_LIBRARY=$HOME/.is/conda/envs/sony/lib/libpython3.so \
-DPYTHON3_EXECUTABLE=$HOME/.is/conda/envs/sony/bin/python \
-DPYTHON3_NUMPY_INCLUDE_DIRS=/home/admin/.is/conda/envs/sony/lib/python3.7/site-packages/numpy/core/include \
..


cmake -DENABLE_OPENCV_NONFREE=ON \
-DBUILD_NEW_PYTHON_SUPPORT=ON \
..



##

https://stackoverflow.com/questions/26228136/pip-build-option-to-use-multicore
https://github.com/opencv/opencv-python/issues/126


