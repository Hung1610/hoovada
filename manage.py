import argparse

from app import create_app


def parse_args():
    parser = argparse.ArgumentParser(
        description='Arguments parsing for hoovada.')
    group = parser.add_argument_group('Arguments')
    group.add_argument('-m', '--mode', required=False, type=str,
                       help='Mode to run app. Mode can be dev or prod')
    group.add_argument('-i', '--ip', required=False, type=str,
                       help='The IP address')
    group.add_argument('-p', '--port', required=False, type=str,
                       help='The port to run app')
    arguments = parser.parse_args()
    return arguments


def main(args):
    mode = 'dev'
    if args.mode is not None:
        mode = args.mode
    ip = '0.0.0.0'
    if args.ip is not None:
        ip = args.ip
    port = '5001'
    if args.port is not None:
        port = args.port
    if mode == 'dev':
        debug = True
    else:
        debug = False

    app = create_app(mode)
    app.run(debug=debug, host=ip, port=port)


# now we just run command to start server, without params like other python code. It might be attended later

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5001)
    args = parse_args()
    main(args)
