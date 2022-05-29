# syntax = docker/dockerfile:1.3
FROM archlinux:base

# sed -i '1 i\Server = https://mirrors.aliyun.com/archlinux/$repo/os/$arch' \


#RUN rm -fr /etc/pacman.d/gnupg \
#  && pacman-key --init \
#  && pacman-key --populate archlinux \
#  && pacman-key --refresh-keys

RUN \
 # --mount=type=cache,target=/var/cache/pacman \
 # --mount=type=cache,target=/var/lib/apt \
 sed -i '1 i\Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch' \
  /etc/pacman.d/mirrorlist && \
 pacman -Syy --noconfirm && \
 pacman -S --noconfirm ffmpeg python python-pip \
  git curl rsync openssh s3fs rclone && \
 curl -s -o /usr/bin/ossutil https://gosspublic.alicdn.com/ossutil/1.7.7/ossutil64 && \
 chmod a+x /usr/bin/ossutil && \
 echo "... step 1 ..."

RUN --mount=type=bind,source=setup/ffmpeg,target=/setup \
 /setup/pip
 
 
 

 
