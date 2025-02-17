from utils import detector_utils as detector_utils
from utils import track_utils as track_utils
from utils import sort as sort
import cv2
import tensorflow as tf
import datetime
import argparse
import numpy as np

detection_graph, sess = detector_utils.load_inference_graph()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-sth',
        '--scorethreshold',
        dest='score_thresh',
        type=float,
        default=0.2,
        help='Score threshold for displaying bounding boxes')
    parser.add_argument(
        '-fps',
        '--fps',
        dest='fps',
        type=int,
        default=1,
        help='Show FPS on detection/display visualization')
    parser.add_argument(
        '-src',
        '--source',
        dest='video_source',
        default=0,
        help='Device index of the camera.')
    parser.add_argument(
        '-wd',
        '--width',
        dest='width',
        type=int,
        default=320,
        help='Width of the frames in the video stream.')
    parser.add_argument(
        '-ht',
        '--height',
        dest='height',
        type=int,
        default=180,
        help='Height of the frames in the video stream.')
    parser.add_argument(
        '-ds',
        '--display',
        dest='display',
        type=int,
        default=1,
        help='Display the detected images using OpenCV. This reduces FPS')
    parser.add_argument(
        '-num-w',
        '--num-workers',
        dest='num_workers',
        type=int,
        default=4,
        help='Number of workers.')
    parser.add_argument(
        '-q-size',
        '--queue-size',
        dest='queue_size',
        type=int,
        default=5,
        help='Size of the queue.')
    args = parser.parse_args()

    print('Input video is ',args.video_source)
    cap = cv2.VideoCapture(args.video_source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    start_time = datetime.datetime.now()
    num_frames = 0
    im_width, im_height = (cap.get(3), cap.get(4))
    # max number of hands we want to detect/track
    num_hands_detect = 4

    # cv2.namedWindow('Single-Threaded Detection', cv2.WINDOW_NORMAL)

    mot_tracker = sort.Sort()

    ret, image_np = cap.read()
    # image_np = cv2.flip(image_np, 1)

    while ret:
    #while num_frames < 10:
        try:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        except:
            print("Error converting to RGB")

        # Actual detection. Variable boxes contains the bounding box cordinates for hands detected,
        # while scores contains the confidence for each of these boxes.
        # Hint: If len(boxes) > 1 , you may assume you have found atleast one hand (within your score threshold)

        boxes, scores = detector_utils.detect_objects(image_np,
                                                      detection_graph, sess)

        # print('score threshold = ', args.score_thresh)
        # print('------ Detection boxes for frame ', num_frames, '------')
        # print(boxes)
        # print('------ Detection scores for frame ', num_frames, '------')
        # print(scores)
        # print('---')
        detection_category = np.ones(len(scores))

        #grouped_detections = track_utils.group_detections(boxes, scores, detection_category)
        grouped_detections = track_utils.group_detections_threshold(boxes, 
                                    scores, detection_category, args.score_thresh)
        # print('------ grouped detections for frame ', num_frames, '------')
        # print grouped_detections

        tracked_objects = mot_tracker.update(grouped_detections)
        # print('------ tracked objects for frame ', num_frames, '------')
        # print tracked_objects
        # draw bounding boxes on frame
        #detector_utils.draw_box_on_image(num_hands_detect, args.score_thresh,
        #                                 scores, boxes, im_width, im_height,
        #                                 image_np)
        # draw bounding boxes on frame
        detector_utils.draw_tracked_box_on_image(tracked_objects,
                                         im_width, im_height, image_np, args.score_thresh)

        # Calculate Frames per second (FPS)
        num_frames += 1
        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        fps = num_frames / elapsed_time

        if (args.display > 0):
            # Display FPS on frame
            if (args.fps > 0):
                detector_utils.draw_fps_on_image("FPS : " + str(int(fps)),
                                                 image_np)

            cv2.imwrite(args.video_source.replace(".mp4", '_' + str(num_frames).zfill(5) + '.jpg'), cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))

        else:
            print("frames processed: ", num_frames, "elapsed time: ",
                  elapsed_time, "fps: ", str(int(fps)))

        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        ret, image_np = cap.read()
        # image_np = cv2.flip(image_np, 1)

