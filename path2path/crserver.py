import argparse
from time import time
import logging
import sys
import traceback
import json
from flask import Flask, make_response, request
from flask_restful import Resource, Api
import numpy as np
import scipy.interpolate as interp
import rdp
import tensorflow as tf
from magenta.models.sketch_rnn.sketch_rnn_train import reset_graph, load_checkpoint, load_model
from magenta.models.sketch_rnn.model import Model, sample
from magenta.models.sketch_rnn.utils import to_big_strokes, to_normal_strokes
from path2path.package import version

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt


def bspline(cv, n=100, degree=3, periodic=False):
    """ Calculate n samples on a bspline

        cv :      Array ov control vertices
        n  :      Number of samples to return
        degree:   Curve degree
        periodic: True - Curve is closed
                  False - Curve is open
    """

    # If periodic, extend the point array by count+degree+1
    cv = np.asarray(cv)
    count = len(cv)

    if periodic:
        factor, fraction = divmod(count+degree+1, count)
        cv = np.concatenate((cv,) * factor + (cv[:fraction],))
        count = len(cv)
        degree = np.clip(degree, 1, degree)

    # If opened, prevent degree from exceeding count-1
    else:
        degree = np.clip(degree, 1, count-1)

    # Calculate knot vector
    if periodic:
        kv = np.arange(0-degree, count+degree+degree-1, dtype='int')
    else:
        # kv = np.array([0]*degree + range(count-degree+1) + [count-degree]*degree ,dtype='int')
        kv = np.concatenate((
            np.zeros(degree), np.arange(count-degree+1), (count-degree)*np.ones(degree)))
    # Calculate query range
    u = np.linspace(periodic, count-degree, n)

    # Calculate result
    arange = np.arange(len(u))
    points = np.zeros((len(u), cv.shape[1]))
    for i in range(cv.shape[1]):
        points[arange, i] = interp.splev(u, (kv, cv[:, i], degree))

    return points


def vec3_to_paths(vec3):
    accum = np.cumsum(vec3[:, :2], axis=0)
    endpoints = np.concatenate(([-1], np.sort(np.where(vec3[:, 2] == 1)[0])))
    paths = []
    for endpoint_n in range(1, endpoints.size):
        start_n = endpoints[endpoint_n - 1] + 1
        end_n = endpoints[endpoint_n] + 1
        cur_path = accum[start_n:end_n]
        paths.append(cur_path)

    return paths


def paths_to_vec3(arg):
    assert isinstance(arg, list)
    total_len = 0
    for path in arg:
        total_len += path.shape[0] - 1
    vec3 = np.zeros((total_len, 3))

    start_n = 0
    for path in arg:
        end_n = start_n + path.shape[0] - 2
        vec3[start_n:end_n + 1, :2] = path[1:] - path[:-1]
        vec3[end_n, 2] = 1.0
        start_n = end_n

    return vec3


def main():
    parser = argparse.ArgumentParser(description='Launch generation server.')
    parser.add_argument('model_dir', help='exported model directory')
    parser.add_argument('--port', default=5000, help='http server port', type=int)
    parser.add_argument('--log_level', default='INFO', help='logging level')
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger('crserver')

    logger.info('launching path2path crserver version: ' + version)

    [_, eval_hps_model, sample_hps_model] = load_model(args.model_dir)

    # construct the sketch-rnn model here:
    reset_graph()
    eval_model = Model(eval_hps_model)
    sample_model = Model(sample_hps_model, reuse=True)

    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())

    # loads the weights from checkpoint into our model
    load_checkpoint(sess, args.model_dir)

    def encode(input_strokes):
        strokes = to_big_strokes(input_strokes, max_len=133).tolist()
        strokes.insert(0, [0, 0, 1, 0, 0])
        seq_len = [len(input_strokes)]
        return sess.run(eval_model.batch_z,
                        feed_dict={eval_model.input_data: [strokes], eval_model.sequence_lengths: seq_len})[0]

    def decode(z_input=None, temperature=0.1):
        z = None
        if z_input is not None:
            z = [z_input]
        sample_strokes, m = sample(sess, sample_model, seq_len=eval_model.hps.max_seq_len, temperature=temperature, z=z)
        strokes = to_normal_strokes(sample_strokes)
        return strokes

    app = Flask(__name__)
    api = Api(app)

    class TFGen(Resource):
        def post(self):
            def error_response(e):
                logger.exception(e)
                e_type, e_value, e_traceback = sys.exc_info()
                e_traceback = traceback.format_tb(e_traceback)

                e_dict = {'error_type': str(e_type),
                          'error_value': str(e_value),
                          'error_traceback': ''.join(e_traceback)}
                error_json = json.dumps(e_dict, ensure_ascii=False).encode('utf8')
                response = make_response(error_json)
                response.headers['content-type'] = 'application/json; charset=utf-8'
                return response

            try:
                # parse JSON post and encode as vector
                t0 = time()
                logger.debug(f'received POST with header:\n{request.headers}')
                posted = json.load(request.stream)
                duration = posted['Duration']
                timestamp = []
                x = []
                y = []
                x_filtered = []
                y_filtered = []
                for elem in posted['Data']:
                    timestamp.append(elem['timestamp'])
                    x.append(elem['uv']['x'])
                    y.append(elem['uv']['y'])
                    x_filtered.append(elem['uv_filtered']['x'])
                    y_filtered.append(elem['uv_filtered']['y'])
                timestamp = np.array(timestamp)
                x_filtered = np.array(x_filtered)
                y_filtered = np.array(y_filtered)
                pos = np.column_stack((x_filtered, y_filtered))

                delta = pos[1:] - pos[:-1]
                path_length = np.sum(np.sqrt(np.sum(np.square(delta), axis=1)))
                ave_speed = path_length/duration
                ave_sample_period = np.mean(timestamp[1:] - timestamp[:-1])

                t1 = time()
                logger.debug(f'Parsing JSON took {t1-t0:.2e}s.')
            except KeyError or json.decoder.JSONDecodeError as err:
                return error_response(err)

            try:
                t0 = time()
                reduced = rdp.rdp(pos, epsilon=0.1)
                t1 = time()
                logger.debug(f'Executing RDP took {t1-t0:.2e}s')
            except ValueError or IndexError as err:
                return error_response(err)

            try:
                t0 = time()
                v3 = paths_to_vec3([reduced])
                bad_response = True
                response_paths = []
                response_count = 0
                while bad_response:
                    encoded = encode(v3)
                    decoded = decode(z_input=encoded)
                    response_paths = vec3_to_paths(decoded)
                    response_count += 1
                    if 5 <= len(response_paths) <= 15:
                        bad_response = False
                    if response_count > 5:
                        bad_response = False
                t1 = time()
                logger.debug(f'Generating path took {t1-t0:.2e}s')
            except ValueError or IndexError as err:
                return error_response(err)

            try:
                t0 = time()
                data = []
                path_timer = 0
                for path in response_paths:
                    path_length = np.sum(np.sqrt(np.sum(np.square(path[1:] - path[:-1]), axis=1)))
                    path_time = path_length/ave_speed
                    # TODO: tune number of samples to modulate output speed
                    path_samples = int((path_time/ave_sample_period)//10)

                    interpolated = bspline(path, n=path_samples, degree=2)
                    cur_path = []
                    for uv in interpolated:
                        cur_path.append({
                            'timestamp': path_timer,
                            'uv': {'x': uv[0], 'y': uv[1]}
                        })
                        path_timer += ave_sample_period
                    data.append(cur_path)
                    plt.plot(interpolated[:, 0], interpolated[:, 1])
                    plt.scatter(path[:, 0], path[:, 1])
                plt.show()

                j = json.dumps({'Data': data}, ensure_ascii=False).encode('utf8')
                r = make_response(j)
                r.headers['content-type'] = 'application/json; charset=utf-8'
                t1 = time()
                logger.debug(f'Converting to JSON took {t1-t0:.2e}s')
                return r
            except IndexError or ValueError as err:
                return error_response(err)

    api.add_resource(TFGen, '/tfgen')

    app.run(port=args.port)


if __name__ == '__main__':
    main()
