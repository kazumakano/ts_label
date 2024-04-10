if __name__ == "__main__":
    import argparse
    from script.database import DbHandler

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--result_dir", required=True, help="specify predict result directory", metavar="PATH_TO_RESULT_DIR")
    parser.add_argument("-v", "--vid_dir", required=True, help="specify video directory", metavar="PATH_TO_VID_DIR")
    parser.add_argument("--ver", default=0, type=int, help="specify predict result version", metavar="VER")
    parser.add_argument("--host", default="0.0.0.0", help="specify server host", metavar="HOST")
    parser.add_argument("--port", default=5000, type=int, help="specify server port", metavar="PORT")
    args = parser.parse_args()

    DbHandler(args.result_dir, args.vid_dir, args.ver).serve(args.host, args.port)
