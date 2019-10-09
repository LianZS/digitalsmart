class Hander_File:
    @staticmethod
    def hander_file(file):
        try:
            for chunk in file.chunks(chunk_size=64):  # djiango自带的文件类型
                yield chunk
        except Exception:
            while 1:  # python内置的file类型
                chunk = file.read(64)
                if not chunk:
                    break
                yield chunk
