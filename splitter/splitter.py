__author__ = 'davide'

import pathlib
import configparser
from math import ceil
import argparse
import sys


def _write_part_file(input_file, dst_file, part_size, bufsize):
    """
    Writes part_size bytes from input_file to dst_path.

    @param input_file: The input file-like object.
    @param dst_file: Destination file
    @param part_size: The size of the part_file
    @param bufsize: The size of the buffer
    """

    read_bytes = 0
    while read_bytes < part_size:
        size = min(part_size - read_bytes, bufsize)
        buffer = input_file.read(size)
        if not buffer:
            break
        read_bytes += len(buffer)
        dst_file.write(buffer)
    assert read_bytes <= part_size


def _create_conf(path, folder, parts):
    """
    Creates the configuration file.

    @param path: The path of the original file.
    @param folder: The folder where to write the conf file.
    @param parts: The number of the parts.
    """
    split_file = folder / "{}.conf".format(path.name)
    config = configparser.ConfigParser()
    config["SETTINGS"] = {"name": path.name, "parts": parts}
    with split_file.open("wt") as param_file:
        config.write(param_file)


def split(path, out_folder, parts, bufsize):
    """
    Splits the file at path into parts files, stored
    in out_folder.

    @param path: The input_file path.
    @param out_folder: The destination folder.
    @param parts: The number of parts.
    @param bufsize: The size of the buffer.
    """
    folder, filename = path.parent, path.name

    _create_conf(path, out_folder, parts)

    part_size = int(ceil(path.stat().st_size / float(parts)))
    with path.open("rb") as input_file:
        for index in range(parts):
            try:
                dst_name = "{}.part{}".format(filename, index)
                dst_path = out_folder / dst_name
                with dst_path.open("wb") as dst_file:
                    _write_part_file(input_file, dst_file, part_size, bufsize)
            except OSError as e:
                print("Errore {}: {}".format(e.errno, e), file=sys.stderr)
                remove_files(index, out_folder, filename)


def remove_files(last, out_folder, filename):
    """
    Removes the files from out_folder from last-1 to 0.
    """
    for index in range(last - 1, -1, -1):
        try:
            name = "{}.part{}".format(filename, index)
            path = out_folder / name
            path.unlink()
        except OSError:
            pass


def _read_conf(path):
    """
    Reads the conf_file.
    """
    config = configparser.ConfigParser()
    with path.open("rt") as param_file:
        config.read_file(param_file)
    return config["SETTINGS"]["name"], int(config["SETTINGS"]["parts"])


def _read_part_file(src_path, out_file, bufsize):
    """
    Reads a part file and stores it into out_file.
    @param src_path:
    @param out_file:
    @param bufsize:
    @return:
    """
    with src_path.open("rb") as input_file:
        buffer = input_file.read(bufsize)
        while buffer:
            out_file.write(buffer)
            buffer = input_file.read(bufsize)


def unsplit(path, out_folder, bufsize):
    filename, parts = _read_conf(path)
    dst = out_folder / filename
    error = False
    with dst.open("wb") as output:
        for index in range(parts):
            try:
                ext = "{}.part{}".format(filename, index)
                src_part = path.parent / ext
                _read_part_file(src_part, output, bufsize)
            except OSError as e:
                print("Errore {}: {}".format(e.errno, e), file=sys.stderr)
                break
    if error:
        try:
            dst.unlink()
        except OSError:
            pass


def parseArgs():
    handler = argparse.ArgumentParser(description="Splitter")
    handler.add_argument('-s', '--splitfile', help="File to split",
                         default="", dest="splitfile")
    handler.add_argument('-n', '--number', help="Number", dest="n", type=int, default=3)
    handler.add_argument('-u', '--unsplit', help="Unsplit file from conf",
                         default="", dest="unsplit")
    handler.add_argument('-o', '--outfolder', help="Output folder",
                         default=None, dest="out_folder")
    handler.add_argument('-b', '--bufsize', help="Buffer Size",
                         default=512, dest="buf_size", type=int)
    return handler.parse_args()


if __name__ == '__main__':
    args = parseArgs()
    if args.splitfile and args.unsplit:
        sys.exit("Error: too many parameters specified")

    if args.unsplit:
        input_file = pathlib.Path(args.unsplit)
    elif args.splitfile:
        input_file = pathlib.Path(args.splitfile)
    else:
        sys.exit("Error: missing parameters")

    if not input_file.exists() or not input_file.is_file():
        sys.exit("{} inesistente o non e' un file!".format(input_file))

    if args.out_folder is None:
        out_folder = input_file.parent
    else:
        out_folder = pathlib.Path(args.out_folder)
        try:
            if not out_folder.exists():
                out_folder.mkdir()
            elif not out_folder.is_dir():
                sys.exit("Error: {} exists and is not a directory".format(out_folder))
        except OSError as e:
            sys.exit("Errore {}: {}".format(e.errno, e))

    if args.unsplit:
        unsplit(input_file, out_folder, args.buf_size)
    else:
        split(input_file, out_folder, args.n, args.buf_size)