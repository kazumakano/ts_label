if __name__ == "__main__":
    import argparse
    from script.database import DbHandler

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--src_result_dir", required=True, help="specify source predict result directory", metavar="PATH_TO_SRC_RESULT_DIR")
    parser.add_argument("-v", "--src_vid_dir", required=True, help="specify source video directory", metavar="PATH_TO_SRC_VID_DIR")
    parser.add_argument("-t", "--tgt_dir", required=True, help="specify target dataset directory", metavar="PATH_TO_TGT_DIR")
    parser.add_argument("--ver", default=0, type=int, help="specify source predict result version", metavar="VER")
    parser.add_argument("--host", default="0.0.0.0", help="specify server host", metavar="HOST")
    parser.add_argument("--port", default=5000, type=int, help="specify server port", metavar="PORT")
    args = parser.parse_args()

    DbHandler(args.src_result_dir, args.src_vid_dir, args.tgt_dir, args.ver).serve(args.host, args.port)
