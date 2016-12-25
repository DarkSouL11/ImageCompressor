#!/usr/bin/env

import tinify
import os
import sys


class Compressor(object):

    def __init__(self, API_KEY):
        tinify.key = API_KEY
        tinify.validate()

    def compress(self, image_path, replace=True, save_path=None):
        try:
            source = tinify.from_file(image_path)
            if replace:
                source.to_file(image_path)
            else:
                source.to_file(save_path)
        except tinify.errors.AccountError as err:
            print(err)
        except Exception as e:
            print(e)

    def url_compress(self, image_url, save_path):
        try:
            source = tinify.from_url(image_url)
            IMAGE = image_url.rsplit('/',1)[1]
            path = save_path + "/" + IMAGE
            source.to_file(path)
        except tinify.errors.AccountError as err:
            print(err)
        except Exception as e:
            print(e)

    def quota_left(self):
        return 500 - tinify.compression_count
