FROM tensorflow/tensorflow:latest-gpu

RUN mkdir -p /home/hands

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install git libsm6 libxrender1 libfontconfig1

WORKDIR /home/hands

RUN git clone https://github.com/pbarsic/handtracking.git

RUN pip install --upgrade pip

RUN pip install matplotlib numba scikit-image scikit-learn filterpy opencv-python opencv-contrib-python

RUN mkdir -p /home/hands/hostfiles

RUN chown -R 1000.1000 /home/hands

WORKDIR /home/hands/handtracking

# build like this:
#docker build -t pbarsic/handtracking:1.5 .

# and run like this:
# docker run -v /home/paul/Tutorials/motion_analysis/hands/hostfiles/:/home/hands/hostfiles -u $(id -u):$(id -g) --runtime=nvidia -it --rm pbarsic/handtracking:1.5

# The only restriction here is that the host folder cannot be the same folder from which the docker image was built.

# copy your source video into the hostfiles folder on the host machine
# python detect_hands_video.py --source /home/hands/hostfiles/[source video]--scorethreshold 0.4
# the output images will be placed in the hostfiles folder (and available outside Docker)
#
# If have ffmpeg installed, do this from the hostfiles folder on the host machine:
#
# ffmpeg -y -r 10000/1001. -i [source video with no .mp4]_%05d.jpg tracked.mp4
#
# this will make an annotated copy of the source video but at 1/3 speed

